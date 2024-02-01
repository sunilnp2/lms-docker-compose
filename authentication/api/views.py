from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from authentication.api.serializers import SignUpSerializer, LoginSerializer
from authentication.models import User

class SignUpSerializerView(APIView):
    """
    This class is responsible for handling user registration through the provided API endpoint.
    It supports both GET and POST HTTP methods.
    Endpoint :
        http://localhost:8000/auth/api/signup/
    """
    def get(self, request):
        return Response({"message":"Get method on Registration"})
    
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response("Successfully Registered",serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetUserView(APIView):

    """
    This class is responsible for retrieving user information through the provided API endpoint.
    It supports the GET HTTP method.

    Endpoint :
        http://localhost:8000/auth/api/getalluser/ - Retrive all Users
        http://localhost:8000/auth/api/getuser/id/ - Retrive specific User

    """
    def get(self,request,pk = None, format= None):
        try:
            if pk:
                try:
                    usr = User.objects.get(id = pk)
                    serializer = SignUpSerializer(usr)
                    return Response(serializer.data, status = status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND) 
            
            users = User.objects.all()
            serializer = SignUpSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND) 



    
class LoginSerializerView(APIView):

    """
    This class is responsible for handling user login through the provided API endpoint.
    It supports the POST HTTP method.
    Endpoint :
        http://localhost:8000/auth/api/login/
    """
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": "Login Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
