import spacy
from langdetect import detect, LangDetectException
from collections import defaultdict, Counter

# Cargar modelos de SpaCy para español e inglés
nlp_es = spacy.load("es_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

def extract_entities(comments):
    """Extraer entidades nombradas y calcular distribución."""
    all_entities = []  # Lista para guardar las entidades de cada comentario
    entity_counter = Counter()  # Contador para la distribución por tipo de entidad

    for comment in comments:
        try:
            # Detectar el idioma del comentario
            lang = detect(comment)
        except LangDetectException:
            lang = 'es'  # Asumir español por defecto

        # Seleccionar el modelo adecuado
        nlp = nlp_en if lang == 'en' else nlp_es

        # Procesar el comentario con el modelo de SpaCy
        doc = nlp(comment)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Agregar las entidades del comentario a la lista general
        all_entities.append(entities)

        # Actualizar el contador con los tipos de entidades detectadas
        for _, label in entities:
            entity_counter[label] += 1

    return all_entities, entity_counter


