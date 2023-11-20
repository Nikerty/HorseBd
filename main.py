import random
import sqlite3

from typing import AnyStr
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from loger import logger

def remove_empty_elements(input_list):
    processed_list = [element for element in input_list if element.strip() != '']
    return processed_list

def word_shortener(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    stemmer = SnowballStemmer("russian")
    question = tokenizer.tokenize(text)
    WordArray = []
    for word in question:
        WordArray.append(stemmer.stem(word).lower())
    return WordArray

def find_answer(keyword):
    """
    :param keyword: Ключевое слова
    :return: возвращает ответ
    """
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("horse_database.db")
    cursor = conn.cursor()
    search_term = f'% {keyword} %'
    query = "SELECT answer FROM my_table WHERE ' ' || LOWER(keywords) || ' ' LIKE ?;"
    cursor.execute(query, (search_term,))

    # Получаем результат запроса
    result = cursor.fetchone()

    # Закрываем соединение с базой данных
    conn.close()
    if result:
        list = remove_empty_elements(result[0].split(";"))
        return list[random.randint(0, len(list) - 1)]  # Возвращаем найденный ответ
    else:
        return None
    
def assistant(question: AnyStr):
    logger.debug('вопрос (question): [' + question + "]")

    helloKeyWords = ['кон', "привет", "здравств"]
    goodByeKeyWords = ['пок', "проща", "забуд"]

    WordArray = word_shortener(text=question)
    response = ''

    if any(helloWord in WordArray for helloWord in helloKeyWords):
        response += ("Здравствуйте! Я конь Василий, ваш гид по достопримечательностям Ростовской области. Задайте мне "
                     "вопросы об интересующей вас достопримечательности, и, если я знаю о ней, то поведаю вам! Для "
                     "завершения разговора скажите пока")
        return response

    if any(goodByeKeyWord in WordArray for goodByeKeyWord in goodByeKeyWords):
        response += "До свидания, рад был помочь!"
        return response

    for word in WordArray:
        if find_answer(word):
            logger.debug("Ключевое слово: " + word)
            return find_answer(word)
