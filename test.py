import re
import random

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty +=1

    percentage = float(message_certainty) / float (len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
        highest_prob = {}

        def response(bot_response_list, list_of_words, single_response = False, required_words = []):
            nonlocal highest_prob
            prob = message_probability(message, list_of_words, single_response, required_words)
            if prob > 0:
                highest_prob[tuple(bot_response_list)] = prob

        response(['Hola', '¡Hola! ¿Cómo estás?', '¡Hola! ¿Qué tal?'], ['hola', 'klk', 'saludos', 'buenas'], single_response = True)
        response(['Estoy bien y tú?', 'Muy bien, gracias ¿Y tú?', 'Todo bien, ¿cómo estás?'], ['como', 'estas', 'va', 'vas', 'sientes'], required_words=['como'])
        response(['Estamos ubicados en la calle 23 número 123', 'Nuestra dirección es Calle 23 #123', 'Nos encontramos en la dirección Calle 23, número 123'], ['ubicados', 'direccion', 'donde', 'ubicacion'], single_response=True)
        response(['Siempre a la orden', 'De nada, ¿hay algo más en lo que pueda ayudarte?', 'No hay problema, ¿en qué más puedo ayudarte?'], ['gracias', 'te lo agradezco', 'thanks'], single_response=True)

        if not highest_prob:
            return unknown()
        best_responses = max(highest_prob, key=highest_prob.get)
        best_response = random.choice(best_responses)
        return best_response

def unknown():
    response = ['¿Puedes repetir la consulta?', 'No estoy muy seguro de lo que necesitas...', 'No logro entender lo que necesitas...'][random.randrange(3)]
    return response

while True:
    print("Bot: " + get_response(input('You: ')))
