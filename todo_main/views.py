from .models import todo
from .serializer import TodoSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.


class Home(APIView):
    def get(self, request):
        return Response(
            {"message": "Please use Post man to interact or admin panel..."},
            status=status.HTTP_200_OK,
        )


class UserRegisteration(APIView):
    # This view has to be accessed by any one to register themselve
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=serializer.data["username"])
            token_obj, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"data": serializer.data, "token": str(token_obj)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tdata = todo.objects.all()
        serialised = TodoSerializer(tdata, many=True)
        return Response(serialised.data)

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return todo.objects.get(pk=pk)
        except todo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tdata = self.get_object(pk)
        serializer = TodoSerializer(tdata)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tdata = self.get_object(pk)
        print(tdata)
        serializer = TodoSerializer(tdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tdata = self.get_object(pk)
        tdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
