from django.http import HttpResponse
from django.urls import path


def hello(request):
    return HttpResponse("""
        <h1>Мой первый сайт</h1>
        <p>Здесь будет мой проект на Django.</p>
        <a href="/about/">О проекте</a>
        <br>
        <a href="/contacts/">Контакты</a>
    """)


def about(request):
    return HttpResponse("""
        <h1>О проекте</h1>
        <p>Я учусь создавать сайты на Python.</p>
        <a href="/">На главную</a>
    """)


def contacts(request):
    return HttpResponse("""
        <h1>Контакты</h1>
        <p>Автор: Капитан Код. Контакт вымышленный.</p>
        <a href="/">На главную</a>
    """)


urlpatterns = [
    path("", hello),
    path("about/", about),
    path("contacts/", contacts),
]
