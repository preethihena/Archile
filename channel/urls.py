from .views import *
from django.urls import path,re_path

urlpatterns = [
	#use same name for url, view function and "name" : Ex:path('asd',asd,name="asd"),
    path('',index,name="index"),
    #path('/search/',dammi,name="dammi"),
    re_path('archile/auth/user/(?P<token_id>[\w\.-]+)/',home,name="home"),
    path('search/<str:query>',search,name="search"),
    path('search_box',search_box,name="search_box"),
]
