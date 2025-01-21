from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email= serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True)

    def validate(self,data):
        if 'username' not in data:
            raise serializers.ValidationError({'username': 'Username is required'})
        if 'email' not in data:
            raise serializers.ValidationError({'email': 'Email is required'})
        if 'password' not in data:
            raise serializers.ValidationError({'password': 'Password is required'})
        
        if len(data['password']) < 8:
            raise serializers.ValidationError({'password': 'Password must be at least 8 characters long'})

        return data
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True)

    def validate(self, data):
        if 'email' not in data:
            raise serializers.ValidationError({'email': 'Email is required'})
        if 'password' not in data:
            raise serializers.ValidationError({'password': 'Password is required'})
        
        return data
    