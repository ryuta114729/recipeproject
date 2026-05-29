from django.contrib import admin

from .models import Recipe
from .models import Review
from .models import Favorite

admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Favorite)

admin.site.site_header = 'レシピアプリ管理画面'
admin.site.site_title = '管理画面'
admin.site.index_title = '管理メニュー'
admin.site.site_url = '/'