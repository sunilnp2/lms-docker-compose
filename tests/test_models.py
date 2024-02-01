from django.test import TestCase
from authentication.models import User
import random
from library.models import Book, BookDetails, BorrowedBooks
from datetime import datetime

from faker import Faker
fake = Faker()
# Unit Testing for User Model -----------------------
class UserTestCase(TestCase):

# Unit Testing for create user 
    def test_create_user(self):
        email = "sunilnepali@gmail.com"
        name = "Sunil Nepali"
        password = "sunil123"

        user = User.objects.create_user(email = email, name = name, password = password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)

# Unit Testing for create superuser 
    def test_create_superuser(self):
        email = "sunil1@gmail.com"
        name = "Anil Nepali"
        password = "anill123"

        user = User.objects.create_superuser(email = email, name = name , password = password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)

# Test Case Success for Get User full Name------------------
class UserMethodTestCase(TestCase):
    def test_get_name(self):
        user  =User(email = "sunil@gmail.com", name = "Sunil Nepali")

        self.assertEqual(user.get_name(),"Sunil Nepali")

# ---------------Unit Testing for Library App---------------------
    
# testcase for book model 
class BookTestCase(TestCase):
    def test_create_book(self):
        elements=['fiction', 'nonfiction', 'mystery', 'fantasy', 'sci-fiction', 'love-story', 'horror', 'finance']

        title = "Atomic Habits"
        isbn  = "40840953"
        genre = random.choice(elements)
        published_date = datetime.today()

        book = Book.objects.create(
            title = title, isbn = isbn, genre = genre, published_date = published_date
        
        )
        self.assertEqual(book.title, title)
        self.assertEqual(book.isbn, isbn)
        self.assertEqual(book.genre, genre)
        self.assertEqual(book.published_date, published_date)

# unit testing for BookDetails 
class BookDetailsTeseCase(TestCase):

    
    def setUp(self):
        title = "Atomic Habits"
        isbn  = "354045"
        genre = "finance"
        published_date = datetime.today()
        self.book = Book.objects.create(
            title = title, isbn = isbn, genre = genre, published_date = published_date
        )

    def test_create_book_detail(self):
        number_of_pages = 344
        publisher = "Asmita Publication"
        language = "English"

        detail = BookDetails(book = self.book, number_of_pages = number_of_pages, publisher = publisher, language = language)
        
        self.assertEqual(detail.book, self.book)
        self.assertEqual(detail.number_of_pages, number_of_pages)
        self.assertEqual(detail.publisher, publisher)
        self.assertEqual(detail.language, language)

# Test Case for BorrowedBooks 
class BorrowedBookTestCase(TestCase):

    
    def setUp(self):
        title = "Atomic Habits"
        isbn  = "238549"
        genre = "finance"
        published_date = datetime.today()
        self.book = Book.objects.create(
            title = title, isbn = isbn, genre = genre, published_date = published_date
        
        )

        email = "sunilnepali@gmail.com"
        name = "Sunil Nepali"
        password = "sunil123"

        self.user = User.objects.create_user(email = email, name = name, password = password)

    def test_create_bprrpwed_book(self):
        borrow = BorrowedBooks(book = self.book,user = self.user)
        
        self.assertEqual(borrow.book, self.book)
        self.assertEqual(borrow.user, self.user)


        