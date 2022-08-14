from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.fields.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def get_absolute_url(self):   # По одной из конвенций django функция, указывающая
                                  # на конкретный объект новостей должна называться именно так

        return reverse('view_news',                      #Название маршрута, как во view
                        kwargs={"pk": self.pk},     #Второй аргумент - номер категории,
                       )                                 #т.е первичный ключ - pk


class Category(models.Model):
    title = models.CharField(max_length=150,
                             db_index=True,
                             verbose_name='Наименование категории'
                             )
    def get_absolute_url(self):   #По одной из конвенций djangoфункция, указывающая
                               # на конкретный объект категорий должна называться именно так

        return reverse('category',                      #Название маршрута, как во view
                        kwargs={"category_id": self.pk} #Второй аргумент - номер категории,
                       )                                #т.е первичный ключ - pk

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title








