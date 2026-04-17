# 📌 TP #1 - Stack Frame (Índice GINI)

## 🧾 Descripción

Este trabajo práctico consiste en el diseño e implementación de una interfaz que permita obtener y mostrar el índice GINI de distintos países a partir de datos del Banco Mundial.

La arquitectura del sistema se divide en varias capas:

* **Capa superior (Python)**: consulta la API del Banco Mundial.
* **Capa intermedia (C)**: recibe los datos procesados.
* **Capa de bajo nivel (Ensamblador)**: realiza conversiones y cálculos utilizando el stack.

---

## 🌐 Fuente de datos

https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22

---

## ⚙️ Funcionamiento

1. Python realiza una consulta a la API.
2. Los datos obtenidos se envían a un programa en C.
3. El programa en C invoca rutinas en ensamblador que:

   * Convierten valores de **float a enteros**.
   * Calculan el índice GINI de un país (sumando +1).
4. Se devuelve el resultado a C o Python para su visualización final.
