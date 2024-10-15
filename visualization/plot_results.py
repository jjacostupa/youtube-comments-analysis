import matplotlib.pyplot as plt
import pandas as pd

def plot_sentiment_distribution(sentiments):
    sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
    plt.bar(sentiment_counts.keys(), sentiment_counts.values())
    plt.title("Distribución de Sentimientos")
    plt.ylabel("Número de Comentarios")
    plt.xlabel("Sentimiento")
    
    plt.savefig('sentiment_distribution.png')  # Guardar gráfico
    plt.clf()  # Limpiar la figura

def save_results(comments, cleaned_comments, sentiments, topics, cleaned_status, detected_languages, entities):
    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write("Comentarios, Comentarios Limpios, Sentimiento, Estado de Limpieza, Idioma Detectado, Entidades Detectadas\n")
        f.write("=" * 80 + "\n")

        # Convertir la lista de temas en una cadena
        topics_str = ['; '.join(topic) for topic in topics]  # Unir palabras de cada tema con un punto y coma
        all_topics_str = '; '.join(topics_str)  # Unir todos los temas en una cadena

        for i in range(len(comments)):
            f.write(f"Comentario Original: {comments[i]}\n")
            f.write(f"Comentario Limpio: {cleaned_comments[i]}\n")
            f.write(f"Sentimiento: {sentiments[i]}\n")
            f.write(f"Estado de Limpieza: {cleaned_status[i]}\n")  # Cambiado para no repetir el comentario limpio
            f.write(f"Idioma Detectado: {detected_languages[i]}\n")  # Guardar idioma detectado
            f.write(f"Entidades Detectadas: {entities[i]}\n")  # Agregar entidades detectadas
            f.write("\n")  # Línea en blanco entre comentarios
        
        # Agregar todos los temas al final del archivo
        f.write("Temas Generados:\n")
        f.write(all_topics_str + "\n")  # Guardar todos los temas generados

    print("Resultados guardados en 'results.txt'.")

