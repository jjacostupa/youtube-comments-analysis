import argparse
from data_collection.youtube_api import get_comments
from data_processing.clean_data import preprocess
from sentiment_analysis.sentiment import analyze_sentiment
from topic_modeling.lda_model import perform_topic_modeling
from entity_recognition.ner import extract_entities
from visualization.plot_results import plot_sentiment_distribution, save_results

def main():
    parser = argparse.ArgumentParser(description="Análisis de comentarios de YouTube")
    parser.add_argument('--video_id', type=str, required=True, help="ID del video a analizar")
    args = parser.parse_args()

    # 1. Recolección de datos
    comments = get_comments(args.video_id)

    # 2. Preprocesamiento
    cleaned_comments, cleaned_status, detected_languages = preprocess(comments)

    # 3. Análisis de Sentimientos
    sentiments = analyze_sentiment(cleaned_comments)

    sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
    print("Distribución de Sentimientos:")
    for sentiment, count in sentiment_counts.items():
        print(f"{sentiment}: {count}")

    # 4. Topic Modeling
    topics = perform_topic_modeling(cleaned_comments)

    print("Temas encontrados:")
    for idx, topic in enumerate(topics):
        print(f"Tema {idx + 1}: {', '.join(topic)}")

    # 5. Extracción de Entidades (NER)
    entities, entity_distribution = extract_entities(cleaned_comments)

    print("Distribución de Entidades Nombradas (NER):")
    for entity_type, count in entity_distribution.items():
        print(f"{entity_type}: {count}")

    # 6. Visualización de Resultados
    plot_sentiment_distribution(sentiments)

    # 7. Guardar Resultados
    save_results(comments, cleaned_comments, sentiments, topics, cleaned_status, detected_languages, entities)

if __name__ == '__main__':
    main()

