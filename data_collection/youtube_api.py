import configparser
from googleapiclient.discovery import build

def get_youtube_api_key():
    """Leer la API key desde config.ini."""
    config = configparser.ConfigParser()
    config.read('config.ini')  # Leer configuración desde config.ini
    return config['YouTube']['API_KEY']

def get_comments(video_id, max_comments=5000):
    """Obtener comentarios con manejo de paginación."""
    api_key = get_youtube_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None  # Token de paginación

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # Límite máximo por página
            pageToken=next_page_token
        )
        response = request.execute()

        # Extraer comentarios
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # Verificar si hay más páginas
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # No hay más páginas

    print(f"Total de comentarios obtenidos: {len(comments)}")
    return comments

