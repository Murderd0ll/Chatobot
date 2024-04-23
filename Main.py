import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import datetime

nltk.download('punkt')
nltk.download('stopwords')

def get_response(user_input):
    split_message = word_tokenize(user_input.lower())
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_length = len(user_message)
    message_certainty = 0

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    if message_length > 0:
        percentage = float(message_certainty) / float(message_length)
    else:
        percentage = 0.0

    for word in required_word:
        if word not in user_message:
            return 0

    if single_response or percentage > 0.5:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob = {}

    # Obtener la hora actual del sistema
    now = datetime.datetime.now()
    current_hour = now.hour

    def response(bot_responses, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        prob = message_probability(message, list_of_words, single_response, required_words)
        if prob > 0:
            highest_prob.update({response: prob for response in bot_responses})

    response(['Hola soy ChatoBot un asistente virtual! En que puedo ayudarte', '¡Hola, qué tal! soy ChatoBot un asistente virtual, En que puedo ayudarte'], ['hola', 'klk', 'saludos', 'buenas'], single_response=True)
    response(['Estoy bien y tú?', 'Todo bien, ¿y tú?'], ['como', 'estas', 'va', 'vas', 'sientes'], required_words=['como'])
    response(['Estamos ubicados en la calle 23 numero 123', 'Nuestra dirección es Calle 23, 123'], ['ubicados', 'direccion', 'donde', 'ubicacion'], single_response=True)
    response(['Siempre a la orden', '¡Gracias a ti!', 'De nada'], ['gracias', 'te lo agradezco', 'thanks'], single_response=True)

    # Saludo según la hora del día
    if current_hour < 12:
        response(['Buenos días', '¡Hola! Buenos días'], ['buenos', 'dias', 'mañana'], single_response=True)
    elif current_hour < 18:
        response(['Buenas tardes', '¡Hola! Buenas tardes'], ['buenas', 'tardes'], single_response=True)
    else:
        response(['Buenas noches', '¡Hola! Buenas noches'], ['buenas', 'noches'], single_response=True)

    best_matches = [key for key, value in highest_prob.items() if value >= 1]
    if not best_matches:
        return unknown()
    return random.choice(best_matches)

def unknown():
    response = ['puedes decirlo de nuevo?', 'No estoy seguro de lo quieres', 'búscalo en google a ver que tal'][random.randrange(3)]
    return response

while True:
    print("Bot: " + get_response(input('You: ')))
