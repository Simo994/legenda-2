from django.db import models

# Create your models here.

class Reservation(models.Model):
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    guests = models.IntegerField('Количество гостей')
    message = models.TextField('Сообщение', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.date} {self.time}'

class Feedback(models.Model):
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    subject = models.CharField('Тема', max_length=200, default='Обратная связь')
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Сообщения обратной связи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'

class MenuItem(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название блюда')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='menu/', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class MenuPhoto(models.Model):
    image = models.ImageField(upload_to='menu_photos/', verbose_name='Фото меню')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание (необязательно)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Фото основного меню'
        verbose_name_plural = 'Фото основного меню'
        ordering = ['-created_at']

    def __str__(self):
        return self.description or f"Фото меню {self.id}"

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='news/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']

    def __str__(self):
        return self.title
