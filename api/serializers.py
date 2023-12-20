from rest_framework import serializers

from django.contrib.auth.models import User

# USERS

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

from .models import Data

# VIDEOS

class DataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'user', 'data_file', 'name', 'upload_date']
        read_only_fields = ['id', 'user', 'upload_date']

class DataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'name', 'upload_date']

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

from .models import DataType

# DATA TYPE

class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = '__all__'

from .models import ProcessedData

# DATA

class GenerateProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = ['user', 'data']
        read_only_fields = ['user']

class UserProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = '__all__'

class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = '__all__'


from .models import Nerf

# NERFS

class NerfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nerf
        fields = '__all__'

from .models import NerfModel

# MODELS

class GenerateNerfModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfModel
        fields = ['nerf', 'processed_data', 'user']
        read_only_fields = ['user']

class NerfModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfModel
        fields = '__all__'

class NerfModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfModel
        fields = ['id', 'status', 'model_file', 'processed_data', 'start_date', 'end_date', 'training_time']

# EXPORT METHOD
from .models import ExportMethod

class ExportMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportMethod
        fields = '__all__'

# OBJECTS
from .models import NerfObject

class GenerateNerfObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfObject
        fields = ['nerf_model', 'user', 'export_method']
        read_only_fields = ['user']

class NerfObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfObject
        fields = '__all__'

# SERIALIZER
from .models import Review

class AddReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'object', 'definition_rating', 'detail_rating', 'usability_rating', 'comment']
        read_only_fields = ['user']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
