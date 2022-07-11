from django.core.files.base import File
from api.models import Document,LinkToDownload
from django.core.validators import URLValidator
from django.core.files.base import ContentFile
import uuid
from urllib.request import urlretrieve
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','first_name', 'last_name', 'email')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        password = validated_data['password'],
                                        email = validated_data['email'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class FileUrlField(serializers.FileField):
    def to_internal_value(self, data):
        try:
            URLValidator()(data)
        except serializers.ValidationError as e:
            raise serializers.ValidationError('Invalid Url')
        file, http_message = urlretrieve(data)
        file = File(open(file, 'rb'))
        return super(FileUrlField, self).to_internal_value(ContentFile(file.read(), name=file.name))


class DocumentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()

    class Meta:
        model=Document
        fields = ['id', 'rdoc', 'name', 'type', 'download', 'created']


class LinkSerializer(serializers.ModelSerializer):
    link = serializers.ReadOnlyField()

    def create(self, validated_data):
        validated_data["link"] = uuid.uuid4()
        return super(LinkSerializer, self).create(validated_data)

    class Meta:
        model=LinkToDownload
        fields = "__all__"


class LinkDetailsSerializer(serializers.ModelSerializer):
    url = DocumentSerializer(many=False, read_only=True)

    class Meta:
        model=LinkToDownload
        fields = "__all__"
