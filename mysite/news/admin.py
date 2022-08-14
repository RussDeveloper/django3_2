from django.contrib import admin

from .models import News, Category

# Register your models here.


class NewsAdmin(admin.ModelAdmin):    #Класс-редактор
    list_display = ('id',
                    'title',
                    'category',
                    'created_at',
                    'updated_at',
                    'is_published',
                    )
    list_display_links = ('id', 'title')   #Поля, которые должны быть ссылками
    search_fields = ('title', 'content')   #Поля, по которым осуществляется поиск
    list_editable = ('is_published',)      #Список редактируемости полей из общего списка
    list_filter = ('is_published', 'category',)


class CategoryAdmin(admin.ModelAdmin):    #Класс-редактор
    list_display = ('id',
                    'title',
                    )
    list_display_links = ('id', 'title')   #Поля, которые должны быть ссылками
    search_fields = ('title', )   #Поля, по которым осуществляется поиск


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

