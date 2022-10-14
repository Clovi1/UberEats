from django.db import models
from slugify import slugify


class Restaurant(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', max_length=100, unique=True, db_index=True)
    time = models.CharField('Время', max_length=50)
    image = models.ImageField('Изображение', upload_to='restaurants')
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey('auth.User', related_name='restaurants', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Kitchen(models.Model):
    title = models.CharField('Название', max_length=100)

    restaurants = models.ManyToManyField('Restaurant', related_name='kitchen', blank=True)

    def __str__(self):
        return self.title


class Food(models.Model):
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='food')
    price = models.IntegerField('Цена')
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey('auth.User', related_name='food', on_delete=models.CASCADE)
    restaurants = models.ForeignKey('Restaurant', related_name='food', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField('Название', max_length=100)

    food = models.ManyToManyField('Food', related_name='categories', blank=True)
    restaurants = models.ManyToManyField('Restaurant', related_name='categories', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title
