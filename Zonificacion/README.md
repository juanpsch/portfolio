# 🚀 Modelo de Clasificación posicional por zonas o recintos de componentes de una planta nuclear

![Python Badge](https://img.shields.io/badge/Python-3.9%2B-blue)

## 💡 Resumen Ejecutivo (El Elevator Pitch)

Este proyecto aborda el desafío de **Sectorizar componentes de una Planta Nuclearcon información extaída de software PLM y diseño 3D**. El objetivo principal es **identificar la ubicación por recinto**, asistiendo a ingenieros, proyectistas, sus decisiones de diseño, planes de montaje y mantenimiento.

## ✨ Características Principales

* **Fase previa - Extracción de datos:** Extracción de más datos de componentes desde el sistema PLM. En primer lugar datos de posicionamiento respecto del origen de coordenadas. Además datos relevantes de cada componente.

* **Definición de bounding boxes:** Se definen las zonas en las cuales se debe clasificar a los componentes

* **Procesamiento de datos y asignación de zona a compoente:** Procesos determinísticos que ubican a cada compoente en su zona / recinto.

* **Post-Procesamiento:** Se incluye informacióna adicional para agregar, como pesos de componentes o volumen. Esto permite obtener el peso o volumen en diferentes
opciones de agregación de los datos.


## 📐 Arquitectura y Flujo de Trabajo



1. **Ingesta de Datos (GIS):** Obtención y limpieza de datasets geográficos clave.

2. **Preprocesamiento y Feature Engineering:** Transformación de coordenadas, cálculo de distancias geodésicas y agregación espacial de variables.

3. **Output:** Generación del dataset en el cual cada componente tiene asignado su zona además de todos sus datos de diseño

## 📊 Resultados y Evaluación (¡Métricas!)


## ⚙️ Cómo Ejecutar el Proyecto

