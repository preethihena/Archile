from .views import *
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name="index"),
    path('logout',user_logout,name="logout"),
    path('user_login',user_login,name="user_login"),
    re_path('archile/auth/user/(?P<token_id>[\w\!-@+]+)/',home,name="home"),
    re_path('actions/(?P<type_of>[a-z_]+)/(?P<action>[0-9]+)/(?P<any_id>[0-9]+)/',actions,name="actions"),
    path('search/<str:query>',search,name="search"),
    path('search_box',search_box,name="search_box"),
    path('create_channel',create_channel,name="create_channel"),
    path('create_post/<int:c_id>',create_post,name="create_post"),
    path('save_post/',save_post,name="save_post"),
    path('edit_post/<int:p_id>',edit_post,name="edit_post"),
    path('post/<int:p_id>',post,name="post"),
    path('channel/<int:c_id>',channel,name="channel"),
    path('subscribe_channel/<int:c_id>',subscribe_channel,name="subscribe_channel"),
    path('edit_channel/<int:c_id>',edit_channel,name="edit_channel"),
    path('report_channel/<int:c_id>',report_channel,name="report_channel"),
    re_path('download/(?P<path>[\w\.!@?#$%&:+;=-]+[.][A-Za-z0-9]+)/(?P<pf_id>[0-9]+)/',download,name="download"),
    path('add_thread/<str:place>/<int:any_id>',add_thread,name="add_thread"),
    path('add_reply/<str:place>/<int:any_id>',add_reply,name="add_reply"),
    path('my_channels',my_channels,name="my_channels"),
    path('liked_posts',liked_posts,name="liked_posts"),
    path('my_subscriptions',my_subscriptions,name="my_subscriptions"),
    path('post_thread_action/<int:pt_id>/<int:typ>',post_thread_action,name="post_thread_action"),
    path('channel_thread_action/<int:ct_id>/<int:typ>',channel_thread_action,name="channel_thread_action"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)