import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_api(request):
    """
    Handles POST requests from the chatbot frontend, communicates with the Gemini API,
    and returns a response.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_message = body.get('message')
            system_prompt = body.get('system_prompt')
            chat_history = body.get('chat_history', [])

            if not user_message:
                return JsonResponse({'error': 'No se proporcionó un mensaje'}, status=400)

            # Retrieve the API key securely from settings.py
            api_key = getattr(settings, "GEMINI_API_KEY", None)

            if not api_key:
                print("Error: La clave de API de Gemini no se encontró en settings.py")
                return HttpResponseServerError('Clave de API no configurada en el servidor.')

            # API URL for Gemini
            API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

            # Prepare the payload for the Gemini API call
            payload = {
                "contents": chat_history,
                "systemInstruction": {
                    "parts": [{"text": system_prompt}]
                },
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 200
                }
            }
            
            # Add the current user message to the payload
            payload['contents'].append({"role": "user", "parts": [{"text": user_message}]})

            # Make the POST request to the Gemini API
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes

            data = response.json()
            
            # Extract the generated text from the API response
            bot_response = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Lo siento, no pude procesar tu solicitud.')
            
            # Return the bot's response to the frontend
            return JsonResponse({'message': bot_response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except requests.exceptions.RequestException as e:
            print(f"Error al llamar a la API de Gemini: {e}")
            return HttpResponseServerError('Error en la comunicación con la IA.')
        except Exception as e:
            print(f"Error inesperado: {e}")
            return HttpResponseServerError('Ocurrió un error inesperado en el servidor.')

    return JsonResponse({'error': 'Método no permitido'}, status=405)
