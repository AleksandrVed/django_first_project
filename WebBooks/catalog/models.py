from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name=models.CharField(max_length=200, help_text="Введите жанр книги", verbose_name="Жанр книги")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, help_text="Введите язык книги", verbose_name="Язык книги")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Введите имя автора", verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, help_text="Введите фамилию автора", verbose_name="Фамилия автора")
    date_of_birth=models.DateField(help_text="Введите дату рождения", verbose_name="Дата рождения", null=True, blank=True)
    date_of_death = models.DateField(help_text="Введите дату смерти", verbose_name="Дата смерти", null=True,blank=True)
    biographi = models.TextField(max_length=10000, help_text="Введите биографию автора", verbose_name="Биография автора", null=True, blank=True)
    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Название книги", verbose_name="Название книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, help_text="Выберите жанр книги", verbose_name="Жанр книги", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE, help_text="Выберите язык книги", verbose_name="Язык книги", null=True)
    author = models.ManyToManyField('Author', help_text="Выберите автора книги", verbose_name="Автор книги")
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги", verbose_name="Краткое описание книги")
    isbn = models.CharField(max_length=13, help_text="Должно содержать 13 символов", verbose_name="ISBN книги")
    file = models.FileField(upload_to='books/')
    price = models.CharField(max_length=20, null=True,help_text="Введите цену", verbose_name="Цена")
    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Авторы'
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Status(models.Model):
    name=models.CharField(max_length=20, help_text="Введите статус экземпляра книги", verbose_name="Статус экземпляра книги")

    def __str__(self):
        return self.name

class Adress(models.Model):
    name=models.CharField(max_length=100, help_text="Введите адрес магазина", verbose_name="Адрес магазина")
    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class BookInstance(models.Model):
    book=models.ForeignKey('Book', on_delete=models.CASCADE, null=True, verbose_name="Книга")
    inv_num = models.CharField(max_length=20, null=True, help_text="Введите инвентарный номер экземпляра", verbose_name="Инвентарный номер")
    imprint = models.CharField(max_length=200,help_text="Введите издательство и год выпуска", verbose_name="Издательство")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,help_text="Введите статус экземпляра", verbose_name="Статус экземпляра")
    due_back = models.DateField(null=True, blank=True, help_text="Введите дату окончания статуса", verbose_name="Дата окончания статуса")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True,verbose_name="Заказчик", help_text="Выберите заказчика книги")
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE, help_text="Адрес магазина", verbose_name="Адрес магазина")
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    def __str__(self):
        return '%s %s %s' % (self.inv_num, self.book, self.status)