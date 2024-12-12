from collections import Counter
from langdetect import detect, LangDetectException
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import pandas as pd
from transformers import pipeline
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)


def group_entities(entities):
    if not entities:
        return []

    # Ordenar entidades por inicio
    ordered_entities = sorted(entities, key=lambda x: x['start'])

    # Lista para almacenar entidades agrupadas
    grouped_entities = []

    # Variable para mantener la entidad actual en proceso
    current_entity = ordered_entities[0].copy()

    for entity in ordered_entities[1:]:
        # Verificar si la entidad actual y la siguiente son del mismo tipo
        # y están consecutivas o casi consecutivas
        if (entity['entity_group'] == current_entity['entity_group'] and
            entity['start'] <= current_entity['end'] + 1):
            # Combinar las entidades
            current_entity['word'] += entity['word'].replace('##', '')
            current_entity['end'] = entity['end']
            current_entity['score'] = max(current_entity['score'], entity['score'])
        elif entity['start'] == current_entity['end']:
            # Combinar las entidades
            current_entity['word'] += entity['word'].replace('##', '')
            current_entity['end'] = entity['end']
            current_entity['score'] = max(current_entity['score'], entity['score'])
        else:
            # Eliminar prefijos de tokens subpalabra
            current_entity['word'] = current_entity['word'].replace('##', '')

            # Agregar la entidad anterior al resultado
            grouped_entities.append(current_entity)

            # Comenzar una nueva entidad actual
            current_entity = entity.copy()

    # Agregar la última entidad
    current_entity['word'] = current_entity['word'].replace('##', '')
    grouped_entities.append(current_entity)

    return grouped_entities

def extract_entities(comments):
    agg_entities = []
    all_entities = []
    entity_counter = Counter()
    MAX_TOKENS = 256

    nlp_multi = pipeline(
        "ner",
        model=AutoModelForTokenClassification.from_pretrained("dslim/distilbert-NER"),
        tokenizer=AutoTokenizer.from_pretrained("dslim/distilbert-NER"),
        aggregation_strategy="simple",  # Agrupa tokens consecutivos de la misma entidad
        batch_size=8
    )

    nlp_es = pipeline(
        "ner",
        model=AutoModelForTokenClassification.from_pretrained("mrm8488/bert-spanish-cased-finetuned-ner"),
        tokenizer=AutoTokenizer.from_pretrained("mrm8488/bert-spanish-cased-finetuned-ner"),
        aggregation_strategy="simple",  # Agrupa tokens consecutivos de la misma entidad
        batch_size=8
    )

    for comment in comments:
        comment = comment[:MAX_TOKENS]
        try:
            # Detectar el idioma del comentario
            lang = detect(comment)
        except LangDetectException:
            lang = 'es' # Asumir español por defecto

        # Seleccionar el modelo adecuado
        if lang == 'es':
            doc = nlp_es(comment)
        else:
            doc = nlp_multi(comment)

        agg_entities += group_entities([x for x in doc if len(x['word'])>2])
        all_entities.append(group_entities([x for x in doc if len(x['word'])>2]))

    # Actualizar el contador con los tipos de entidades detectadas
    for ent in agg_entities:
        entity_counter[ent['word']] += 1

    return all_entities, entity_counter


# Cargar modelos de SpaCy para español e inglés
# nlp_es = spacy.load("es_core_news_sm")
# nlp_en = spacy.load("en_core_web_sm") 

# def extract_entities(comments):
#     """Extraer entidades nombradas y calcular distribución."""
#     all_entities = []  # Lista para guardar las entidades de cada comentario
#     entity_counter = Counter()  # Contador para la distribución por tipo de entidad

#     for comment in comments:
#         try:
#             # Detectar el idioma del comentario
#             lang = detect(comment)
#         except LangDetectException:
#             lang = 'es'  # Asumir español por defecto

#         # Seleccionar el modelo adecuado
#         nlp = nlp_en if lang == 'en' else nlp_es

#         # Procesar el comentario con el modelo de SpaCy
#         doc = nlp(comment)
#         entities = [(ent.text, ent.label_) for ent in doc.ents]

#         # Agregar las entidades del comentario a la lista general
#         all_entities.append(entities)

#         # Actualizar el contador con los tipos de entidades detectadas
#         for _, label in entities:
#             entity_counter[label] += 1

#     return all_entities, entity_counter


