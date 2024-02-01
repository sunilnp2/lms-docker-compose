from django.contrib.auth import authenticate
from authentication.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists. Please try with a new email.")

        elif value[0].isdigit():
            raise serializers.ValidationError("Email must start with a letter.")

        end_strings = [".gmail.com", ".yahoo.com", ".hotmail.com", "yopmail.com", "tempmail.com"]
        val = any(value.endswith(end_str) for end_str in end_strings)
        if not val:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password length must be more than 6 characters.")

        if value[0].isdigit() == True or value[0].isupper() == False:
            raise serializers.ValidationError("First letter must be a capital letter.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match. Please try again.")
        return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        name = validated_data.get("name")
        password = validated_data.get("password")

        user = User.objects.create_user(name = name, email=email, password=password)
        return user
        
        
#-------------- code for signin-------------------------------------------------------------- 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
    def create(self,validated_data):
        email = validated_data.get('email')
        pw = validated_data.get('password')
    
        user = authenticate(email = email, password = pw)
        if user is not None:
            return Response({'msg':'Login Success'}, status=status.HTTP_200_OK)
        return Response({'errors':{'non_field_errors':["Username Or Password is not valid"]}},
                        status = status.HTTP_404_NOT_FOUND)
