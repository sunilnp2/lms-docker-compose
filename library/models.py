from typing import Any
from django.db import models
from authentication.models import User


GENRE = ((''))
# Book model for register all books
class Book(models.Model):

    GENRE = (
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('sci-fiction', 'Science Fiction'),
        ('love-story', 'Love Story'),
        ('horror', 'Horror'),
        ('finance', 'Finance'),
    )

    title = models.CharField(max_length = 200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    genre = models.CharField(max_length=50, choices = GENRE)

    def __str__(self):
        return self.title
    


# BookDetails Model for Details of each book
class BookDetails(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE) # One to one relation with Book model
    number_of_pages = models.PositiveIntegerField()
    publisher = models.CharField(max_length=255)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.book.title



# BorrowedBooks Model for track borrowed book from library 
class BorrowedBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.name