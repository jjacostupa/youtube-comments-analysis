from transformers import pipeline

def analyze_sentiment(comments, model_name="pysentimiento/robertuito-sentiment-analysis"):
    MODEL_TOKEN_LIMITS = {
        "pysentimiento/robertuito-sentiment-analysis": 128,
        "distilbert/distilbert-base-uncased-finetuned-sst-2-english": 512
    }
    max_tokens = MODEL_TOKEN_LIMITS[model_name]
    sentiment_analyzer = pipeline(
        task="sentiment-analysis", 
        model=model_name
    )

    sentiments = []
    for comment in comments:
        comment = comment[:max_tokens]
        analysis = sentiment_analyzer(comment)[0]  # Analizar cada comentario
        sentiments.append({
            'label': analysis['label'], # ('POS', 'NEG', 'NEU')
            'score': analysis['score']  # Probabilidad asociada
        })

    return sentiments

### Codigo con logica de idioma, pero demora. 
# from transformers import pipeline
# from langdetect import detect, LangDetectException

# def analyze_sentiment(comments, model_name_en="distilbert/distilbert-base-uncased-finetuned-sst-2-english", model_name_es="pysentimiento/robertuito-sentiment-analysis"):
    
#     # Función para detectar el idioma y seleccionar el modelo adecuado
#     def get_model_and_lang(comment):
#         try:
#             lang = detect(comment)
#         except LangDetectException:
#             lang = 'en'  # Asumimos ingles por defecto si hay un error en la detección
            
#         # Selecciona el modelo y el límite de tokens según el idioma
#         if lang == 'en':
#             return model_name_en, 512
#         else:
#             return model_name_es, 128

#     sentiments = []
    
#     for comment in comments:
#         # Obtener el modelo y el límite de tokens según el idioma
#         model_name, max_tokens = get_model_and_lang(comment)
        
#         # Recortar el comentario al límite de tokens del modelo
#         comment = comment[:max_tokens]
        
#         # Crear el pipeline de análisis de sentimiento
#         sentiment_analyzer = pipeline(
#             task="sentiment-analysis", 
#             model=model_name
#         )
        
#         # Realizar el análisis de sentimiento
#         analysis = sentiment_analyzer(comment)[0]
        
#         sentiments.append({
#             'label': analysis['label'],  # ('POS', 'NEG', 'NEU')
#             'score': analysis['score']  # Probabilidad asociada
#         })

#     return sentiments


### Codigo con ejemplo del profesor
# from textblob import TextBlob

# def analyze_sentiment(comments):
#     sentiments = []
#     for comment in comments:
#         analysis = TextBlob(comment).sentiment.polarity
#         sentiments.append('positive' if analysis > 0 else 'negative' if analysis < 0 else 'neutral')
#     return sentiments
