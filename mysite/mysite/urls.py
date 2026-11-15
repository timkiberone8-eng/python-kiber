from django.http import HttpResponse
from django.urls import path
from catalog.views import home
from django.contrib import admin

def hello(request):
    return HttpResponse("""
        <h1>Мой первый сайт</h1>
        <p>Здесь будет мой проект на Django</p>
        <a href="/about">О проекте</>
        <br>
        <a href="/contaсts">Контакты</>
    """)

def about(request):
    return HttpResponse("""
    <h1>Это страница о моем проекте.</h1>
    <a href="/">На главную</>
    """)

urlpatterns = [
    path("", home),
    path("about/", about),
    path('admin/', admin.site.urls)
]