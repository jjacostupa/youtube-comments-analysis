# data_processing/clean_data.py
import re
from nltk.corpus import stopwords
from langdetect import detect, LangDetectException
import nltk

# Descargar stopwords
nltk.download('stopwords')

# Cargar stopwords en inglés y español
stop_words_en = set(stopwords.words('english'))
stop_words_es = set(stopwords.words('spanish'))

def preprocess(comments):
    cleaned = []
    cleaned_status = []  # Lista para guardar el estado de cada comentario
    detected_languages = []  # Lista para guardar los idiomas detectados

    for comment in comments:
        # Eliminar URLs y caracteres especiales
        original_comment = comment  # Guarda el comentario original
        comment = re.sub(r"http\S+|www\S+|https\S+", '', comment) # Eliminamos urls
        comment = re.sub(r'\W+', ' ', comment).lower().strip() # Eliminamos caracteres que no sean alfanumericos 

        # Verificar si el comentario está vacío después de la limpieza
        if not comment:  # Si el comentario está vacío después de la limpieza
            cleaned_status.append(f"Comentario eliminado (vacío)")
            cleaned.append("")  # Agregar una entrada vacía
            detected_languages.append('N/A')  # No hay idioma
            continue  # No añadir comentarios vacíos

        try:
            # Detectar el idioma del comentario
            lang = detect(comment)
            detected_languages.append(lang)  # Guardar el idioma detectado

            # Seleccionar las stopwords adecuadas
            stop_words = stop_words_en if lang == 'en' else stop_words_es

        except LangDetectException:
            # Si no se detecta idioma, asumimos español
            lang = 'es'
            detected_languages.append(lang)
            stop_words = stop_words_es

        # Eliminar stopwords
        filtered_comment = ' '.join([word for word in comment.split() if word not in stop_words])

        if filtered_comment:  # Evitar comentarios vacíos
            cleaned.append(filtered_comment)
            cleaned_status.append("Comentario limpio")  # Cambiado para no incluir el comentario limpio
        else:
            cleaned_status.append(f"Comentario eliminado (solo stopwords)")
            cleaned.append("")  # Agregar una entrada vacía
            detected_languages.append(lang)  # Guardar el idioma detectado

    return cleaned, cleaned_status, detected_languages  # Devolver también el idioma detectado

