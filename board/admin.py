from django.contrib import admin
from .models import *

admin.site.register(Board)
admin.site.register(Article)
admin.site.register(ArticlePhoto)
admin.site.register(ArticleVote)
admin.site.register(ArticleVoteItem)
admin.site.register(Comment)
admin.site.register(Reply)
