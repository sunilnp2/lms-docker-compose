import base64
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from authentication.models import User
from library.models import *
from rest_framework import status
from library.api.serializers import BookSerializer, BookDetailSerializer, BorrowedBooksSerializer
from django.utils import timezone

# Unit Testing For SIgnup 
class SignupViewTestCase(APITestCase):

    def test_create_user(self):
        url = reverse('authentication:signup')

        data = {'email': 'test@gmail.com',
                 'name': 'New User',
                   'password': 'password123',
                     'password2': 'password123'}
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email = data['email'])
        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.is_active)


    def test_incorrect_data(self):
        url = reverse('authentication:signup')

        data = {'email': 'test@gmail.com',
                 'name': 'New User',
                   'password': 'password123',
                     'password2': 'sunil123'}
        
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Unit Testing for GetUser ------------------ 
class GetUserViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com', name='Test User', password = "test123")

    def test_get_user_detail(self):
        url = reverse('authentication:getuser', kwargs={'pk': self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@gmail.com')
        self.assertEqual(response.data['name'], 'Test User')

    def test_get_all_users(self):
        url = reverse('authentication:getalluser') 

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'test@gmail.com')
        self.assertEqual(response.data[0]['name'], 'Test User')

    def test_user_not_found(self):
        url = reverse('authentication:getuser', kwargs={'pk': 999})  # Use an ID that doesn't exist

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'User not found')


# Unit testing for Login 
class LoginSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com', name='Test User')
        self.valid_data = {'email': 'test@gmail.com', 'password': 'test123'}
        self.invalid_data = {'email': 'test@gmail.com', 'password': 'wrong_password'}

    def test_valid_login(self):
        url = reverse('authentication:login')

        response = self.client.post(url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.assertEqual(response.data['success'], 'Login Successfully')

    def test_invalid_login(self):
        url = reverse('authentication:login') 

        response = self.client.post(url, self.invalid_data, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)



# ----------------------------Unit Testing for Library API Views----------------------------------
# Unit Test for Create,Read,Update Book 
class BookCreateReadAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com',name = "Test User", password='test123')
        Book.objects.create(title='Book 1', isbn='111', published_date='2022-01-30', genre='finance')
        Book.objects.create(title='Book 2', isbn='222', published_date='2022-01-31', genre='fiction')
    def test_get_all_books(self):
        url = reverse('library:book_all_create') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_single_book(self):
        book = Book.objects.create(title='Single Book', isbn='0987654321', published_date='2022-01-31', genre='Non-Fiction')
        url = reverse('library:book', args=[book.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Single Book')

    def test_create_book(self):
        email = 'test@gmail.com'
        password = 'test123'
        credentials = f"{email}:{password}".encode('utf-8')
        auth_header = 'Basic ' + base64.b64encode(credentials).decode('utf-8')

        data = {'title': 'Test Book', 'isbn': '1267890', 'published_date': '2022-01-30', 'genre': 'fiction'}
        url = reverse('library:book_all_create')

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Book')
        


# Unit Testing for BookDetail create, retrive and update
class BookDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com',name = "Test User", password='test123')
        self.book = Book.objects.create(title='Book 1', isbn='111', published_date='2022-01-30', genre='finance')
        self.book_detail = BookDetails.objects.create(book=self.book, number_of_pages=100, publisher='Test Publisher', language='English')
    def test_get_book_detail(self):
        url = reverse('library:bookdetail-getupdate', kwargs={'pk': self.book_detail.id})
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number_of_pages'], 100)

    def test_patch_book_detail(self):
        url = reverse('library:bookdetail-getupdate', kwargs={'pk': self.book_detail.id})
        self.client.force_authenticate(user=self.user)

        data = {'number_of_pages': 150}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number_of_pages'], 150)

    def test_create_book_detail(self):
        email = 'test@gmail.com'
        password = 'test123'
        credentials = f"{email}:{password}".encode('utf-8')
        auth_header = 'Basic ' + base64.b64encode(credentials).decode('utf-8')

        url = reverse('library:create-book-detail')
        # self.client.force_authenticate(user=self.user)

        book_data = BookSerializer(self.book).data

        data = {'book': book_data, 'number_of_pages': 120, 'publisher': 'New Publisher', 'language': 'english'}
        response = self.client.post(url, data, format='json',HTTP_AUTHORIZATION=auth_header)

        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)


# Test case for Get,Create,Retrrive Borrow Books 
class BorrowReadBooksAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com',name = "Test User", password='test123')
        self.book = Book.objects.create(title='Test Book', isbn='1234567890', published_date='2022-01-30', genre='fiction')
        self.borrowed_book = BorrowedBooks.objects.create(user=self.user, book=self.book)

    def test_borrow_book(self):
        url = reverse('library:borrowbook')
        self.client.force_authenticate(user=self.user)

        data = {'user': self.user.id, 'book': self.book.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['book'], self.book.id)

    def test_list_borrowed_books(self):
        url = reverse('library:list_borrowed_book')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('borrowed_books' in response.data)
        self.assertTrue('available_books' in response.data)
        self.assertEqual(len(response.data['borrowed_books']), 1) 
        self.assertEqual(len(response.data['available_books']), 0)  


class ReturnBorrowedBookAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com',name = "Test User", password='test123')
        self.book = Book.objects.create(title='Test Book', isbn='1234567890', published_date='2022-01-30', genre='fiction')
        self.borrowed_book = BorrowedBooks.objects.create(user=self.user, book=self.book, borrowed_date=timezone.now().date())

    def test_return_borrowed_book(self):
        url = reverse('library:return-book', kwargs={'pk': self.borrowed_book.id})
        self.client.force_authenticate(user=self.user)

        returned_date = (timezone.now() + timezone.timedelta(days=7)).strftime("%Y-%m-%d")
        data = {'returned_date': returned_date}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Book returned successfully.')

        # Check if the returned_date is updated in the database
        updated_borrowed_book = BorrowedBooks.objects.get(pk=self.borrowed_book.id)
        self.assertEqual(updated_borrowed_book.returned_date, timezone.datetime.strptime(returned_date, "%Y-%m-%d").date())

    def test_return_borrowed_book_invalid_date_format(self):
        url = reverse('library:return-book', kwargs={'pk': self.borrowed_book.id})
        self.client.force_authenticate(user=self.user)

        invalid_date = 'invalid_date_format'
        data = {'returned_date': invalid_date}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid date format.')