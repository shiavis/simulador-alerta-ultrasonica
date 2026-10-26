# Versión Streamlit

Esta carpeta contiene una versión Python del simulador de alerta ultrasónica. Conserva la escena animada del canal, el sensor US-01, el pulso ultrasónico, el eco de retorno, el nivel de agua y los estados de alerta.

## Ejecución local

```bash
cd streamlit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Luego abre la dirección local que muestre Streamlit, normalmente `http://localhost:8501`.

La aplicación usa Python/Streamlit para los controles y cálculos, y un componente HTML/JavaScript embebido para conservar la animación fluida del canal. Esta versión es educativa y no sustituye un sistema certificado de Protección Civil.
