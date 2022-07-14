from this import d
from django.shortcuts import render
from django.template.response import TemplateResponse
import requests
from bs4 import BeautifulSoup
from transliterate import translit


class Parse:
    def parse(word, url):
        # Замена ё на е
        for i in word:
            if i == "ё":
                word = word.replace(i, "е")
        # Траслитерация слова и обозначения его первой буквы на латинице
        match word[0]:
            case "е":
                FirstLetter = "ye"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "ж":
                FirstLetter = "zh"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "й":
                FirstLetter = "iy"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "ч":
                FirstLetter = "ch"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "ш":
                FirstLetter = "sh"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "щ":
                FirstLetter = "sch"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "ъ":
                word = "tverdyi-znak"
                FirstLetter = "tznak"
            case "ы":
                word, FirstLetter = "y"
            case "ь":
                word = "myagkii-znak"
                FirstLetter = "mznak"
            case "ю":
                FirstLetter = "yu"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case "я":
                FirstLetter = "ya"
                word = translit(word, 'ru', reversed=True)
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
            case _:
                word = translit(word, 'ru', reversed=True)
                FirstLetter = str(word[0])
                for i in word:
                    if i == "'":
                        word = word.replace(i, "")
        url = f'{url}/{FirstLetter}/{word}.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        dic = soup.find_all('div', class_="found_word")
        res = ""

        for gloses in dic:
            res += gloses.p.text

        return res


def index1(requeat):
    return render(request, 'index.html')


def index(request):
    word = 'арбуз'
    dictionaries = [
        ['Толковый словарь Даля', 'https://diclist.ru/slovar/dalya'],
        ['Толковый словарь Ожегова', 'https://diclist.ru/slovar/ozhegova'],
        ['Толковый словарь Ушакова', 'https://diclist.ru/slovar/ushakova'],
        ['Словарь Ефремовой', 'https://diclist.ru/slovar/efremovoy'],
        ['Энциклопедия Брокгауза и Ефрона', 'https://diclist.ru/slovar/dalya']
    ]

    for i in dictionaries:
        i.append(Parse.parse(word, i[1]))

    data = {'dict': dictionaries}

    return TemplateResponse(request, 'result.html', data)
