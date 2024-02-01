from django.contrib import admin
from library.models import Book, BookDetails, BorrowedBooks
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'isbn', 'published_date', 'genre']
    list_display_links  = ['id', 'title', 'isbn', 'published_date', 'genre']

admin.site.register(Book, BookAdmin)
admin.site.register(BookDetails)

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'borrowed_date', 'returned_date']
    list_display_links = ['id', 'user', 'book', 'borrowed_date', 'returned_date']
admin.site.register(BorrowedBooks, BorrowedBookAdmin)