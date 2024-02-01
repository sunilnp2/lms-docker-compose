from django.urls import path, include
from library.api.views import BookCreateReadAPIView, BookDetailAPIView, BorrowReadBooksAPIView, ReturnBorrowedBookAPIView

urlpatterns = [

    path('book_all_create/', BookCreateReadAPIView.as_view(), name='book_all_create'),
    path('book/<int:pk>/', BookCreateReadAPIView.as_view(), name='book'),

    path('create-book-detail/',BookDetailAPIView.as_view(), name='create-book-detail'),
    path('book-detail/<int:pk>',BookDetailAPIView.as_view(), name='bookdetail-getupdate'),

    path('borrowbook/', BorrowReadBooksAPIView.as_view(), name='borrowbook'),
    path('list_borrowed_book/', BorrowReadBooksAPIView.as_view(), name='list_borrowed_book'),
    path('return-book/<int:pk>/', ReturnBorrowedBookAPIView.as_view(), name='return-book'),
    
]
