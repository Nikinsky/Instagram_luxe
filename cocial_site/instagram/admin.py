from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class PostIMGInlines(admin.TabularInline):
    model = PostIMG
    extra = 1

class PostVideoInlines(admin.TabularInline):
    model = PostVideo
    extra = 1




@admin.register(Post)
class PostTranAdmin(TranslationAdmin):
    inlines = [PostIMGInlines, PostVideoInlines]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }





admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Save)
admin.site.register(SaveItem)
admin.site.register(CommentLike)
admin.site.register(PostLike)

