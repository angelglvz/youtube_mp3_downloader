import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services import send_telegram_message, download_and_send_youtube_mp3

@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Endpoint que recibe las actualizaciones (updates) de Telegram."""
    try:
        data = json.loads(request.body.decode("utf-8"))
        
        if "message" in data:
            message = data["message"]
            chat_id = message["chat"]["id"]
            user_text = message.get("text", "")
            user_first_name = message["from"].get("first_name", "Usuario")

            if user_text.startswith("/start"):
                response_text = (
                    f"¡Hola, {user_first_name}! 🎵\n\n"
                    "Envíame un enlace de YouTube y te enviaré el archivo MP3."
                )
                send_telegram_message(chat_id, response_text)

            elif user_text.startswith("/help"):
                send_telegram_message(chat_id, "Pega cualquier enlace de YouTube para descargar su audio.")

            elif "youtube.com" in user_text or "youtu.be" in user_text:
                download_and_send_youtube_mp3(chat_id, user_text)

            else:
                send_telegram_message(chat_id, "Por favor, envíame un enlace válido de YouTube.")

        return JsonResponse({"status": "ok"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)