import string
from django.shortcuts import render
from django.template.response import TemplateResponse
import requests
from bs4 import BeautifulSoup
from transliterate import translit
from django import forms


class Form(forms.Form):
    word = forms.CharField(label='')


class Parse:
    def wordManage(FirstLetter):
        """Trasliterating word and designation it first letter"""
        FirstLetter = f"{FirstLetter}"
        word = translit(word, 'ru', reversed=True)
        for i in word:
            if i == "'":
                word = word.replace(i, "")

    def parse(word, url):
        # Replacement "е" to "ё"
        for i in word:
            if i == "ё":
                word = word.replace(i, "е")
        # Trasliterating word and designation it first letter
        match word[0]:
            case "е":
                Parse.wordManage('ye')
            case "ж":
                Parse.wordManage('zh')
            case "й":
                Parse.wordManage('iy')
            case "ч":
                Parse.wordManage('ch')
            case "ш":
                Parse.wordManage('sh')
            case "щ":
                Parse.wordManage('sch')
            case "ъ":
                word = "tverdyi-znak"
                FirstLetter = "tznak"
            case "ы":
                word, FirstLetter = "y"
            case "ь":
                word = "myagkii-znak"
                FirstLetter = "mznak"
            case "ю":
                Parse.wordManage('yu')
            case "я":
                Parse.wordManage('ya')
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


def index(request):
    userform = Form()
    data = {"form": userform}

    return render(request, "index.html", data)


def result(request):
    if request.method == "POST":
        word = request.POST.get("word")
        word = str(word)

    dictionaries = [
        ['Толковый словарь Даля', 'https://diclist.ru/slovar/dalya'],
        ['Толковый словарь Ожегова', 'https://diclist.ru/slovar/ozhegova'],
        ['Толковый словарь Ушакова', 'https://diclist.ru/slovar/ushakova'],
        ['Словарь Ефремовой', 'https://diclist.ru/slovar/efremovoy'],
        ['Энциклопедия Брокгауза и Ефрона', 'https://diclist.ru/slovar/dalya']
    ]

    for i in dictionaries:
        i.append(Parse.parse(word.lower(), i[1]))

    userform = Form()
    data = {'dict': dictionaries, 'word': word, "form": userform}

    return TemplateResponse(request, 'result.html', data)
