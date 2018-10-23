from .views import *
from django.urls import path

urlpatterns = [
	#use same name for url, view function and "name" : Ex:path('asd',asd,name="asd"),
    path('',index,name="index"),
    path('search/<str:query>',search,name="search"),
    path('search_box',search_box,name="search_box"),
]
