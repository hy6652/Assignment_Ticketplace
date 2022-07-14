from django.contrib.auth.models import User

from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'password_check']

        extra_kwargs = {
            'password': {'write_only':True}
        }

    def save(self):
        username       = self.validated_data['username']
        email          = self.validated_data['email']
        password       = self.validated_data['password']
        password_check = self.validated_data['password_check']

        if password != password_check:
            raise serializers.ValidationError('both password should be same')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return user