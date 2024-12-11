# YouTube Comment Analysis Project

Este proyecto realiza un análisis de comentarios en videos y transmisiones en vivo de YouTube. Proporciona funcionalidades como preprocesamiento, análisis de sentimientos, modelado de tópicos y reconocimiento de entidades. Además, permite la visualización de los resultados de manera clara y detallada.

---

## Requisitos

### Instalación en un entorno local (Windows con WSL2)

1. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

2. **Actualizar pip e instalar dependencias:**
   ```bash
   python3 -m pip install --upgrade pip
   python -m pip install pip-tools
   pip-compile requirements.in
   pip install -r requirements.txt
   ```

3. **Descargar modelos de SpaCy:**
   ```bash
   python -m spacy download es_core_news_sm
   python -m spacy download en_core_web_sm
   ```

4. **Desactivar el entorno virtual:**
   ```bash
   deactivate
   ```

---

## Configuración de la API de YouTube

1. **Crear un proyecto en Google Cloud Platform (GCP):**
   - Inicia sesión en [Google Cloud Console](https://console.cloud.google.com/).
   - Crea un nuevo proyecto.
   - Habilita la API: “YouTube Data API v3”.

2. **Crear credenciales para la API:**
   - Ve a la sección “Credenciales” del proyecto.
   - Genera una clave de API.
   - Copia la clave generada.

3. **Configurar `config.ini`:**
   - Abre el archivo `config.ini` y agrega tu clave API:
     ```ini
     [YouTube]
     API_KEY = PONER-SU-API-KEY-QUE-SE-DESCARGA-DE-GOOGLE-CLOUD
     ```

---

## Comandos disponibles

### Análisis de comentarios en videos

- **Análisis básico:**
  ```bash
  python -m main --video_id <VIDEO_ID>
  ```
  Ejemplo:
  ```bash
  python -m main --video_id ewOPQZZn4SY
  ```

- **Especificar máximo de comentarios:**
  ```bash
  python -m main --video_id <VIDEO_ID> --max_comments <MAX>
  ```
  Ejemplo:
  ```bash
  python -m main --video_id ewOPQZZn4SY --max_comments 2000
  ```

### Análisis de comentarios en transmisiones en vivo

- **Análisis básico:**
  ```bash
  python -m main --video_id <LIVE_VIDEO_ID>
  ```
  Ejemplo:
  ```bash
  python -m main --video_id 9ut3S5aLu4s
  ```

- **Especificar máximo de comentarios:**
  ```bash
  python -m main --video_id <LIVE_VIDEO_ID> --max_comments <MAX>
  ```
  Ejemplo:
  ```bash
  python -m main --video_id PiDMMoqrqRc --max_comments 100
  ```

---

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar su mantenimiento y escalabilidad:

- **`requirements.in`**: Archivo con las dependencias necesarias para el proyecto.
- **`main.py`**: Punto de entrada principal para ejecutar el análisis.
- **`config.ini`**: Archivo de configuración para las claves de API.

### Módulos

1. **`data_collection/youtube_api.py`**:
   - Conexión con la YouTube Data API.
   - Obtención de comentarios (de videos o transmisiones en vivo).

2. **`data_processing/clean_data.py`**:
   - Realiza preprocesamiento de los comentarios.

3. **`sentiment_analysis/sentiment.py`**:
   - Análisis de sentimientos (español e inglés).

4. **`topic_modeling/lda_model.py`**:
   - Modelado de tópicos usando LDA.

5. **`entity_recognition/ner.py`**:
   - Reconocimiento de entidades con SpaCy.

6. **`visualization/plot_results.py`**:
   - Visualización de resultados con matplotlib.

---

## Notas importantes

- Asegúrate de tener configurado correctamente el archivo `config.ini` antes de ejecutar cualquier comando.
- Si encuentras problemas al instalar dependencias o configurar el entorno, consulta la documentación oficial de las herramientas utilizadas:
  - [Google Cloud Platform](https://cloud.google.com/)
  - [Hugging Face Transformers](https://huggingface.co/transformers/)
  - [SpaCy](https://spacy.io/)

---

## Contribuciones

Las contribuciones son bienvenidas. Si deseas agregar nuevas funcionalidades o corregir errores, realiza un fork del repositorio y envía un pull request.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

