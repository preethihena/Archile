from django.contrib import admin
from .models import *

admin.site.register([User,Channel,Subscription,Post,Post_files,Channel_threads,Post_threads,channel_actions])
admin.site.register([Tags,Post_tags,Channel_tags,post_actions,post_file_actions,channel_thread_actions,post_thread_actions,])