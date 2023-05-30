from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from .serializers import UserSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(views.APIView):
    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user=form.get_user())
            return Response(UserSerializer(user).data)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(views.APIView):
    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user