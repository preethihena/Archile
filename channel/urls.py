from .views import *
from django.urls import path,re_path

urlpatterns = [
    path('',index,name="index"),
    path('login',login,name="login"),
    re_path('archile/auth/user/(?P<token_id>[\w\.-]+)/',home,name="home"),
    path('search/<str:query>',search,name="search"),
    path('search_box',search_box,name="search_box"),
    path('create_channel',create_channel,name="create_channel"),
    path('create_post/<int:c_id>',create_post,name="create_post"),
    path('save_post/',save_post,name="save_post"),
    path('edit_post',edit_post,name="edit_post"),
    path('post',post,name="post"),
    path('channel',channel,name="channel"),
]
