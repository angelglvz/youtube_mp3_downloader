import os
import requests
import yt_dlp

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_telegram_message(chat_id, text):
    """Envía un mensaje de texto al chat de Telegram."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    return requests.post(url, json=payload).json()

def download_and_send_youtube_mp3(chat_id, youtube_url):
    """Descarga el audio de YouTube, lo convierte a MP3 y lo envía al usuario."""
    send_telegram_message(chat_id, "⏳ Procesando y descargando el audio, un momento...")

    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            file_id = info['id']
            title = info.get('title', 'Audio de YouTube')
            file_path = os.path.join(output_dir, f"{file_id}.mp3")

        # Enviar archivo de audio a Telegram
        url = f"{TELEGRAM_API_URL}/sendAudio"
        with open(file_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            data = {
                'chat_id': chat_id,
                'title': title,
                'performer': 'YouTube Bot'
            }
            response = requests.post(url, data=data, files=files)
        
        # Limpieza local del archivo
        if os.path.exists(file_path):
            os.remove(file_path)

        return response.json()

    except Exception as e:
        send_telegram_message(chat_id, f"❌ Error al procesar el audio: {str(e)}")
        return None