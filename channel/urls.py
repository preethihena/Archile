from .views import *
from django.urls import path,re_path

urlpatterns = [
    path('',index,name="index"),
    path('login',login,name="index"),
    re_path('archile/auth/user/(?P<token_id>[\w\.-]+)/',home,name="home"),
    path('search/<str:query>',search,name="search"),
    path('search_box',search_box,name="search_box"),
    path('create_channel',create_channel,name="create_channel"),
]
