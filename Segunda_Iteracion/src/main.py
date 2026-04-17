from flask import Flask, render_template_string, jsonify
import requests
import numpy as np
import ctypes
import os
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)
lib_path = os.path.join(os.path.dirname(__file__), 'main.so')
main_c = ctypes.CDLL(lib_path)

main_c.convertion.argtypes = (
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int
)
main_c.convertion.restype = ctypes.c_void_p

def get_data(country_code:str) -> tuple:
    """
    Consulta datos del índice GINI para un país específico.

    Args:
        country_code (str): Código ISO del país (ej: 'ARG', 'BR', etc.)

    Returns:
        Tuple[np.ndarray, np.ndarray]: años y valores GINI
    """
    url = f"https://api.worldbank.org/v2/en/country/{country_code}/indicator/SI.POV.GINI"
    params = {"format": "json", "date": "2000:2025"}

    response = requests.get(url, params=params)
    
    if response.ok:
        try:
            data = response.json()
            results = data[1]

            year = []
            value = []
            for entry in results:
                year.append(entry['date'])
                value.append(entry['value'] if entry['value'] is not None else 0)

            year = np.flip(np.array(year, dtype=float))
            value = np.flip(np.array(value, dtype=float))
            return year, value
        except Exception as e:
            print("Error parsing data:", e)
            return None, None
    else:
        return None, None

def convertion(input:ctypes.Array, output:ctypes.Array, length:int) -> None:
    """
    Llama a la función `convertion` definida en la biblioteca C/ASM.

    Esta función envía un arreglo de valores flotantes (float) al 
    código nativo, que realiza la conversión a enteros y almacena 
    los resultados en un arreglo de salida.

    Args:
        input (ctypes array): Arreglo de entrada con valores float.
        output (ctypes array): Arreglo de salida para valores int.
        length (int): Cantidad de elementos a procesar.

    Returns:
        None
    """
    main_c.convertion(input, output, length)

def convert_with_c(values:np.ndarray) -> np.ndarray:
    """
    Convierte un array de floats a enteros usando la biblioteca en C.
    
    Args:
        values (np.ndarray): arreglo de valores float
    
    Returns:
        np.ndarray: arreglo convertido a int (vía ASM/C)
    """
    length = len(values)
    input_array = (ctypes.c_float * length)(*values)
    output_array = (ctypes.c_int * length)()
    convertion(input_array, output_array, length)
    return np.ctypeslib.as_array(output_array)

def create_plot(years:np.ndarray, values_converted:np.ndarray, is_null:np.ndarray, country_code:str) -> str:
    """
    Genera el gráfico interactivo con Plotly para los valores GINI.

    Args:
        years (np.ndarray): Años
        values_converted (np.ndarray): Valores GINI convertidos (enteros)
        is_null (np.ndarray): Máscara booleana de valores nulos
        country_code (str): Código del país

    Returns:
        str: HTML con el gráfico embebido
    """
    values_clean = [v if not null else None for v, null in zip(values_converted, is_null)]

    trace_main = go.Scatter(
        x=years,
        y=values_clean,
        mode='lines+markers',
        name='GINI disponible',
        marker=dict(size=8),
        line=dict(shape='linear')
    )

    trace_nulls = go.Scatter(
        x=years[is_null],
        y=values_converted[is_null],
        mode='markers',
        name='Dato no disponible',
        marker=dict(size=10, color='red', symbol='x'),
        hovertext=["Dato original nulo"] * np.count_nonzero(is_null),
        hoverinfo='text'
    )

    layout = go.Layout(
        title=dict(
            text=f'Índice GINI en {country_code.upper()}',
            x=0.5,
            xanchor='center',
            font=dict(size=24, color='black')
        ),
        xaxis=dict(
            title=dict(text='Año', font=dict(size=16)),
            tickfont=dict(size=12),
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)',
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text='GINI', font=dict(size=16)),
            tickfont=dict(size=12),
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)',
            zeroline=False,
            range=[30, 60]
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        )
    )

    fig = go.Figure(data=[trace_main, trace_nulls], layout=layout)
    return pyo.plot(fig, output_type='div', include_plotlyjs='cdn')

def render_html_plot(plot_html: str, country_code: str) -> str:
    """
    Retorna el HTML con el gráfico embebido.

    Args:
        plot_html (str): Div generado por Plotly
        country_code (str): Código del país

    Returns:
        str: Página HTML lista para renderizar
    """
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GINI Plot {country_code.upper()}</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; }}
            .button {{
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #2ecc71;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 16px;
                display: inline-block;
                transition: background-color 0.3s ease;
            }}
            .button:hover {{
                background-color: #27ae60;
            }}
        </style>
    </head>
    <body>
        {plot_html}
        <br>
        <a href="/" class="button">🔙 Volver a Inicio</a>
    </body>
    </html>
    """)

@app.route('/gini/<country_code>')
def gini_json(country_code:str):
    """
    Devuelve en formato JSON el índice GINI para un país específico.

    Esta ruta consulta los datos del World Bank API para el país indicado,
    convierte los valores de GINI usando una biblioteca en C/ASM, y retorna 
    los resultados en una respuesta JSON.

    Args:
        country_code (str): Código ISO 3166-1 alpha-3 del país (ej. 'ARG', 'BRA', 'MEX').

    Returns:
        Response: Objeto JSON con las claves:
            - "country": código del país
            - "years": lista de años (float)
            - "values": lista de valores GINI convertidos (int)
        o bien un error HTTP 404 si no se encuentran datos.
    """
    year, value = get_data(country_code)
    
    if year is None:
        return jsonify({'error': f"No se encontraron datos para '{country_code.upper()}'"}), 404

    value_c = convert_with_c(value)

    return jsonify({
        'country': country_code.upper(),
        'years': year.tolist(),
        'values': value_c.tolist()
    })

@app.route('/gini/<country_code>/plot')
def gini_plot(country_code:str) -> str:
    """
    Genera una visualización interactiva del índice GINI para un país dado.

    Esta ruta consulta el índice GINI desde el Banco Mundial, lo procesa 
    con una biblioteca compartida en C (que incluye lógica en ensamblador),
    y luego genera un gráfico interactivo usando Plotly.

    Args:
        country_code (str): Código del país en formato ISO-3166 alpha-3 (ej. 'ARG', 'BRA', 'ESP').

    Returns:
        str: Página HTML con el gráfico embebido si hay datos.
        Response: Código HTTP 404 si no se encuentran datos para el país solicitado.
    """
    year, value = get_data(country_code)
    if year is None:
        return f"<h2>Error: No se encontraron datos para el país '{country_code.upper()}'</h2>", 404

    value_c = convert_with_c(value)
    is_null = value_c == 1
    plot_html = create_plot(year, value_c, is_null, country_code)
    return render_html_plot(plot_html, country_code)

@app.route('/')
def index() -> str:
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculadora GINI 🌎</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #2c3e50; }
            .button {
                display: inline-block;
                margin: 10px;
                padding: 12px 24px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                text-decoration: none;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <h1>Calculadora de Índice GINI 🌍</h1>
        <p>Elegí un país para ver su gráfico:</p>
        <a href="/gini/ARG/plot" class="button">🇦🇷 Argentina</a>
        <a href="/gini/USA/plot" class="button">🇺🇸 Estados Unidos</a>
        <a href="/gini/BRA/plot" class="button">🇧🇷 Brasil</a>
        <a href="/gini/DEU/plot" class="button">🇩🇪 Alemania</a>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
