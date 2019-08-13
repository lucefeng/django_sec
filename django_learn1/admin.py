from django.contrib import admin

# Register your models here.
from django_learn1.models import *
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id','btitle','bpub_date'] #显示的字段
    search_fields = ['btitle']
class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['hname','hgender','hcontent']
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','email','password']
    search_fields = ['name']
class Comments_NoteAdmin(admin.ModelAdmin):
    list_display = ['hname','hcontent','h_time']

admin.site.register(BookInfo,BookInfoAdmin)
admin.site.register(HeroInfo,HeroInfoAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Comments_Note,Comments_NoteAdmin)
# admin.site.register(UserModels)