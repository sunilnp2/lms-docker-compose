from library.api.serializers import BookSerializer, BookDetailSerializer, BorrowedBooksSerializer
from library.models import Book,BookDetails, BorrowedBooks
from library.api.custom_permissions import CustomPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from django.utils import timezone

class BookCreateReadAPIView(APIView):
    """
    This class handles the creation and retrieval of book records through the provided API endpoint.
    It supports both GET and POST HTTP methods.
    Endpoint :
        - http://localhost:8000/library/api/book_all_create/ - Create a book and get all book
        - http://localhost:8000/library/api/book/id - get all book or specific book

    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [CustomPermission]

    # Retrieve details of a specific book
    def get(self, request, pk=None):
        try:
            if pk is not None:
                book = Book.objects.get(id=pk)
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                books = Book.objects.all()
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        

#  create book or list all books
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        try:
            if serializer.is_valid():
                book = serializer.save()
                return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

        
class BookDetailAPIView(APIView):
    """
    This class handles the get, retrive and update of detail information of 'Book' provided API endpoint.
    It supports GET, POST, and PATCH HTTP methods

    Endpoint :
        - http://localhost:8000/library/api/create-book-detail/ - Create Detail of specific book
        - http://localhost:8000/library/api/book-detail/id - Retrive book detail and update
        
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [CustomPermission]
    def get(self,request,pk = None):
        if pk:
            try:
                book = BookDetails.objects.get(id=pk)
                serializer = BookDetailSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error":"Pk Need to see detail"})

    def patch(self, request,pk = None,format= None):
        book_details = BookDetails.objects.get(id = pk)
        if book_details:
            serializer = BookDetailSerializer(book_details, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'BookDetails not found'}, status=status.HTTP_404_NOT_FOUND)
    

    def post(self,request):
        try:
            serializer = BookDetailSerializer(data=request.data)
            if serializer.is_valid():
                detail = serializer.save()
                return Response(BookDetailSerializer(detail).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class BorrowReadBooksAPIView(APIView):
    """
    This class manages the borrowing of books through the provided API endpoint.
    It supports both GET and POST HTTP methods.

    Endpoint:
        http://localhost:8000/library/api/list_borrowed_book/ - List Borrowed Books (Get)
        http://localhost:8000/library/api/borrowbook/ - Borrow Book (Post)
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [CustomPermission]

    # Records book borrowing and returns a response 
    def post(self, request):
        try:
            serializer = BorrowedBooksSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Lists borrowed and available books
    def get(self, request):
        try:
            borrowed_books = BorrowedBooks.objects.all()
            available_books = Book.objects.exclude(id__in=borrowed_books.values('book__id'))
            
            borrowed_serializer = BorrowedBooksSerializer(borrowed_books, many=True)
            available_serializer = BookSerializer(available_books, many=True)
            
            response_data = {
                'borrowed_books': borrowed_serializer.data,
                'available_books': available_serializer.data,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ReturnBorrowedBookAPIView(APIView):
    """
    This class handles the updating of the system when a book is returned through the provided API endpoint.
    It supports the PUT HTTP method.

    Endpoint:
            http://localhost:8000/library/api/return-book/id/ - Return Borrowed Book (PUT) 
        
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [CustomPermission]
    
    # Updates system when a book is returned.
    def put(self, request, pk):
        try:
            borrowed_book = BorrowedBooks.objects.get(pk=pk)
            returned_date = request.data.get('returned_date')
            try:
                returned_date = timezone.datetime.strptime(returned_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({'detail': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

            if returned_date < borrowed_book.borrowed_date:
                return Response({'detail': 'Returned date must be equal to or greater than the borrowed date.'}, status=status.HTTP_400_BAD_REQUEST)

            borrowed_book.returned_date = returned_date
            borrowed_book.save()
            return Response({'detail': 'Book returned successfully.'}, status=status.HTTP_200_OK)

        except BorrowedBooks.DoesNotExist:
            return Response({'detail': 'Borrowed book not found.'}, status=status.HTTP_404_NOT_FOUND)
    