from django.contrib import admin
from .models import Author, Book, Genre, Language, Status, BookInstance, Adress, Purchase


# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    list_filter = ('last_name', 'date_of_birth')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death'), 'biographi']


admin.site.register(Author, AuthorAdmin)


# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'inv_num')
    list_filter = ('status', 'due_back', 'book')
    fieldsets = (('Экземпляр книги', {'fields': ('book', 'imprint', 'inv_num')}),
                 ('Статус и окончание его действия', {'fields': ('borrower', 'status', 'due_back', 'adress')}),
                 )


class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('language', 'author')
    inlines = [BookInstanceInline]


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
admin.site.register(Adress)
admin.site.register(Purchase)
