from library.models import Book, BookDetails, BorrowedBooks
from rest_framework import serializers, status
from rest_framework.response import Response



class BookSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
       model = Book
       fields = ['id', 'title', 'isbn', 'published_date', 'genre']
       read_only_fields = ['id']

       def create(self, validated_data):
            title = validated_data.get("title")
            isbn = validated_data.get("isbn")
            published_date = validated_data.get("published_date")
            genre = validated_data.get("genre")
            # Create a new Book instance
            book = Book.objects.create(title = title, isbn = isbn, published_date = published_date, genre = genre)
            book.save()
            return Response({"success":"Book Add Successfully"}, status=status.HTTP_201_CREATED)
       

class BookDetailSerializer(serializers.ModelSerializer):
    # Nested serializer for the Book model

    class Meta:
        model = BookDetails
        fields = ['id','book', 'number_of_pages', 'publisher', 'language']
        read_only_fields = ['id']



class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = ['id','user', 'book', 'borrowed_date', 'returned_date']
        read_only_fields = ['id']

    

        
