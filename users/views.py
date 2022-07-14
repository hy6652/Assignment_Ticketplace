from rest_framework                  import status
from rest_framework.views            import APIView
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request):
        seralizer = RegistrationSerializer(data=request.data)

        if seralizer.is_valid():
            user = seralizer.save()
            refresh = RefreshToken.for_user(user)

            data = {}

            data['username'] = user.username
            data['email']    = user.email
            data['token']    = {
                                'refresh': str(refresh),
                                'access' : str(refresh.access_token)
                            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)