import configparser
import time
from googleapiclient.discovery import build

def get_youtube_api_key():
    """Leer la API key desde config.ini."""
    config = configparser.ConfigParser()
    config.read('config.ini')  # Leer configuración desde config.ini
    return config['YouTube']['API_KEY']

def get_comments(video_id, max_comments=100):
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



# obtener comentarios de un live de youtube

def get_live_chat_id(video_id):
    """Obtener el liveChatId de un video en vivo."""
    api_key = get_youtube_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    )
    response = request.execute()

    live_chat_id = response['items'][0]['liveStreamingDetails'].get('activeLiveChatId')
    if not live_chat_id:
        print("Este video no tiene un chat en vivo activo.")
        return None

    return live_chat_id

def get_live_comments(live_chat_id, max_comments=100, sleep_time=4):
    """Obtener comentarios del chat en vivo con paginación y manejo de tasa."""
    api_key = get_youtube_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None

    try:
        while len(comments) < max_comments:
            try:
                request = youtube.liveChatMessages().list(
                    liveChatId=live_chat_id,
                    part='snippet,authorDetails',
                    maxResults=100,
                    pageToken=next_page_token
                )
                response = request.execute()

                # Extraer mensajes y autores
                for item in response['items']:
                    comment = item['snippet']['textMessageDetails']['messageText']
                    comments.append(comment)
                    print(comment)

                # Verificar si hay más páginas
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break  # No hay más páginas

            except Exception as e:
                print(f"Error: {e}. Esperando {sleep_time} segundos antes de reintentar.")
                time.sleep(sleep_time)  # Esperar antes de reintentar

            # Pausa para respetar la tasa de refresco de la API
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario. Finalizando recolección de datos...")

    print(f"Total de mensajes obtenidos: {len(comments)}")
    return comments


def get_comments_from_video_or_live(video_id, max_comments=100):
    """Obtener comentarios o mensajes de chat en vivo dependiendo del estado del video."""
    live_chat_id = get_live_chat_id(video_id)

    if live_chat_id:
        print("Obteniendo mensajes del chat en vivo...")
        return get_live_comments(live_chat_id, max_comments)
    else:
        print("Obteniendo comentarios del video...")
        return get_comments(video_id, max_comments)


