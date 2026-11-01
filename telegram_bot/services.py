# telegram_bot/services.py
import os
import requests
import yt_dlp

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Ruta absoluta hacia el ejecutable node.exe dentro de la carpeta local node_runtime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
node_executable = os.path.join(BASE_DIR, "node_runtime", "node.exe")

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
    """Descarga el audio de YouTube usando Node.js local, lo convierte a MP3 y lo envía."""
    send_telegram_message(chat_id, "⏳ Procesando y descargando el audio, un momento...")

    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    # Estructura corregida que espera yt-dlp para los runtimes de JS
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'js_runtimes': {
            'node': {
                'path': node_executable
            }
        },
        'quiet': False,
    }

    try:
        print(f"DEBUG: Iniciando extracción para {youtube_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            file_id = info['id']
            title = info.get('title', 'Audio de YouTube')
            file_path = os.path.join(output_dir, f"{file_id}.mp3")

        print(f"DEBUG: Archivo generado en {file_path}, enviando a Telegram...")
        url = f"{TELEGRAM_API_URL}/sendAudio"
        with open(file_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            data = {
                'chat_id': chat_id,
                'title': title,
                'performer': 'YouTube Bot'
            }
            response = requests.post(url, data=data, files=files, timeout=60)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        print("DEBUG: ¡Audio enviado con éxito!")
        return response.json()

    except Exception as e:
        print(f"❌ EXCEPCIÓN CAPTURADA: {str(e)}")
        send_telegram_message(chat_id, f"❌ Error al procesar el audio: {str(e)}")
        return None