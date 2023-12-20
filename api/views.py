from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from dotenv import load_dotenv

load_dotenv()

# users
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserLoginSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'User registration succesful'}, 
            status=status.HTTP_201_CREATED, 
            headers=headers)

class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)

# data
from .models import Data 
from .serializers import DataUploadSerializer, DataListSerializer, DataSerializer

class DataUploadView(generics.CreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataUploadSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserDataView(generics.ListAPIView):
    serializer_class = DataListSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = User.objects.all()[0]
        return Data.objects.filter(user=user)

class DataDetailView(generics.RetrieveAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    lookup_field = 'id' 

# data types
from .models import DataType
from .serializers import DataTypeSerializer

class AllDataTypesView(generics.ListAPIView):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer

# data
from .models import ProcessedData
from .serializers import GenerateProcessedDataSerializer, UserProcessedDataSerializer, ProcessedDataSerializer
from .utils import generate_processed_data

class GenerateProcessedDataView(generics.CreateAPIView):
    serializer_class = GenerateProcessedDataSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        processed_data = serializer.save(user=self.request.user)
        generate_processed_data.delay(serializer.data, processed_data.id)

class UserProcessedDataView(generics.ListAPIView):
    serializer_class = UserProcessedDataSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = User.objects.all()[0]
        return ProcessedData.objects.filter(user=user)

class ProcessedDataDetailView(generics.RetrieveAPIView):
    queryset = ProcessedData.objects.all()
    serializer_class = ProcessedDataSerializer
    lookup_field = 'id'

# nerfs
from .models import Nerf
from .serializers import NerfSerializer


class AllNerfsView(generics.ListAPIView):
    queryset = Nerf.objects.all()
    serializer_class = NerfSerializer

# nerf models
from .models import NerfModel
from .serializers import NerfModelSerializer, GenerateNerfModelSerializer, NerfModelListSerializer
from .utils import generate_nerf_model

class GenerateNerfModelView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = GenerateNerfModelSerializer

    def perform_create(self, serializer):
        nerf_model = serializer.save(user=self.request.user)
        generate_nerf_model.delay(serializer.data, nerf_model.id) 

class UserNerfModelsView(generics.ListAPIView):
    serializer_class = NerfModelListSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = User.objects.all()[0]
        return NerfModel.objects.filter(user=user)

class NerfModelDetailView(generics.RetrieveAPIView):
    queryset = NerfModel.objects.all()
    serializer_class = NerfModelSerializer
    lookup_field = 'id'

# export methods
from .models import ExportMethod
from .serializers import ExportMethodSerializer

class AllExportMethodsView(generics.ListAPIView):
    queryset = ExportMethod.objects.all()
    serializer_class = ExportMethodSerializer

# nerf objects
from .models import NerfObject
from .serializers import NerfObjectSerializer, GenerateNerfObjectSerializer
from .utils import generate_nerf_object

class GenerateNerfObjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GenerateNerfObjectSerializer

    def perform_create(self, serializer):
        nerf_object = serializer.save(user=self.request.user)
        generate_nerf_object.delay(serializer.data, nerf_object.id)

class UserNerfObjectsView(generics.ListAPIView):
    serializer_class = NerfObjectSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = User.objects.all()[0]
        return NerfObject.objects.filter(user=user)

class NerfObjectDetailView(generics.RetrieveAPIView):
    queryset = NerfObject.objects.all()
    serializer_class = NerfObjectSerializer
    lookup_field = 'id'

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MeshNerfObjectView(APIView):
    def get(self, request, nerf_object_id):
        nerf_object = get_object_or_404(NerfObject, pk=nerf_object_id)
        file_path = nerf_object.object_file.path

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'inline; filename={nerf_object.object_file.name}'
            return response

class TextureNerfObjectView(APIView):
    def get(self, request, nerf_object_id):
        nerf_object = get_object_or_404(NerfObject, pk=nerf_object_id)
        file_path = nerf_object.texture_file.path

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'inline; filename={nerf_object.texture_file.name}'
            return response

class MaterialNerfObjectView(APIView):
    def get(self, request, nerf_object_id):
        nerf_object = get_object_or_404(NerfObject, pk=nerf_object_id)
        file_path = nerf_object.material_file.path

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'inline; filename={nerf_object.material_file.name}'
            return response

# reviews
from .models import Review
from .serializers import ReviewSerializer, AddReviewSerializer

class AddReviewView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllReviewsView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# TODO: Fix filter criteria

class DataTypeReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(object__data__user=self.request.user)

class DataReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(object__data__user=self.request.user)

class NerfReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(object__nerf_model__nerf__user=self.request.user)

class NerfModelReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(object__nerf_model__user=self.request.user)

class ExportMethodReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(object__export_method__user=self.request.user)

class NerfObjectReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(object__user=self.request.user)