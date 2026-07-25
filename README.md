# 💱 Calculadora y Monitor Cambiario (BCV vs Binance)

Una aplicación web desarrollada en Python con Streamlit diseñada para consultar en tiempo real y analizar la brecha cambiaria entre la tasa oficial del Banco Central de Venezuela (BCV) y el mercado paralelo (Binance P2P). 

Esta herramienta facilita la toma de decisiones financieras rápidas al convertir montos, calcular el impacto del diferencial en el poder adquisitivo y permitir la distribución ágil de los resultados.

## 🚀 Características Principales

* **Monitor en Tiempo Real:** Conexión directa a APIs públicas (DolarAPI y Binance P2P) para extraer las tasas actualizadas del USD y EUR.
* **Conversor Rápido de Divisas:** Cálculo instantáneo de dólares a bolívares mostrando la equivalencia simultánea en ambas tasas referenciales.
* **Análisis de Brecha Cambiaria:** Cálculo automático del diferencial porcentual (%), la brecha absoluta en bolívares por dólar y la pérdida real de valor.
* **Escenarios de Poder Adquisitivo:** Tabla comparativa que proyecta las diferencias de costos para montos estándar ($10, $50, $100).
* **Botón de Compartir (Click-to-Chat):** Integración nativa con WhatsApp Web/Móvil para generar un reporte de texto preformateado con las tasas del día y enviarlo con un solo clic.

## 🏥 Casos de Uso Prácticos

Esta aplicación es ideal para comercios, profesionales independientes y gestión de presupuestos. Por ejemplo, facilita enormemente a las personas el cálculo rápido y transparente del equivalente en bolívares, garantizando que el usuario tenga el monto exacto según la tasa de su preferencia antes de realizar la transacción.

## 🛠️ Tecnologías Utilizadas

* **[Python 3.x](https://www.python.org/):** Lógica del backend.
* **[Streamlit](https://streamlit.io/):** Framework para la interfaz de usuario web y renderizado responsivo.
* **[Pandas](https://pandas.pydata.org/):** Estructuración de datos para la tabla de escenarios.
* **[Requests](https://pypi.org/project/requests/):** Consumo de APIs RESTful.

## 📦 Instalación y Ejecución Local

Si deseas correr este proyecto en tu entorno local:

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/RigelVarela/TasaCambio.git](https://github.com/RigelVarela/TasaCambio.git)
   cd TasaCambio
