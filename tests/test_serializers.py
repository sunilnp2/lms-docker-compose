from rest_framework.test import APITestCase
from authentication.models import User
from library.models import Book,BookDetails, BorrowedBooks
from authentication.api.serializers import SignUpSerializer, LoginSerializer
from library.api.serializers import BookSerializer, BookDetailSerializer, BorrowedBooksSerializer
from rest_framework import status

class SignUpSerializerTeseCase(APITestCase) :
    data = {'email': 'test@gmail.com',
                 'name': 'New User',
                   'password': 'password123',
                     'password2': 'password123'}
    def test_user_password_missmatch(self):
        serializer = SignUpSerializer(data = self.data)
        self.assertTrue(serializer.is_valid())

    def test_create_user(self):
        
        serializer = SignUpSerializer(data = self.data)
        self.assertTrue(serializer.is_valid())
        user = serializer.create(serializer.validated_data)

        self.assertEqual(user.email,self.data['email'])
        self.assertEqual(user.name,self.data['name'])
        # self.assertTrue(user.check_password(self.data['password']))

    def test_email_duplicate(self):
        User.objects.create(email = "test@gmail.com", name= "Test user", password = "test123")

        serializer = SignUpSerializer(data = self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['email'][0],"user with this Email already exists." )



class LoginSerializerTestCase(APITestCase):
    def test_login(self):
        user = User.objects.create_user(email = "test@gmail.com", name= "Test user", password = "test123")
        
        # user = User.objects.all().first()
        # print(f"The user is {user}")
        data = {'email': 'test@gmail.com', 'password': 'test123'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response = serializer.create(serializer.validated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'msg': 'Login Success'})

        
    def test_invalid_login(self):  
        data = {'email': 'test@gmail.com', 'password': 'test123'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response = serializer.create(serializer.validated_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('non_field_errors', response.data['errors'])


class BookSerializerTestCase(APITestCase):

    def setUp(self):
        # Create a sample Book instance for testing
        self.sample_book_data = {
            'title': 'Sample Book',
            'isbn': '1234567890',
            'published_date': '2022-01-01',
            'genre': 'fiction',
        }
        self.sample_book = Book.objects.create(**self.sample_book_data)
    def test_create_book(self):
        # Create a request data for creating a new book
        new_book_data = {
            'title': 'New Book',
            'isbn': '0987654321',
            'published_date': '2023-02-15',
            'genre': 'fiction',
        }

        # Serialize the request data
        serializer = BookSerializer(data=new_book_data)
        if serializer.is_valid() == False:
            print(serializer.errors)

        # Validate the serializer data
        self.assertTrue(serializer.is_valid())
        
        # Create a new book using the serializer's create method
        created_book_response = serializer.create(serializer.validated_data)

        # Perform assertions based on the response
        # self.assertEqual(created_book_response.data, {'success': 'Book Add Successfully'})

        # Check if the new book is created in the database
        new_book = Book.objects.get(title='New Book')
        self.assertEqual(new_book.isbn, '0987654321')
        self.assertEqual(new_book.published_date.strftime('%Y-%m-%d'), '2023-02-15')
        self.assertEqual(new_book.genre, 'fiction')



