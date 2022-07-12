from api.models import Document, LinkToDownload
from api.serializers import DocumentSerializer,LinkSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.generic.detail import DetailView
from django.http import FileResponse, HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
import os
import zipfile
from io import BytesIO
from .serializers import RegisterSerializer, UserSerializer, LinkDetailsSerializer


class DocumentView(APIView):

    def post(self, request, format=None):
        try:
            for i in range(len(request.data)):
                obj = request.data
                obj['rdoc'] = request.data[str(i)]
                serializer = DocumentSerializer(data=obj)
                if serializer.is_valid():
                    serializer.save()
            return Response({'msg': ' Uploaded Successfully', 'status':'success'}, status=status.HTTP_201_CREATED)
        except:
            return Response("Error",status=400)

    def get(self, request, format=None):
        files = Document.objects.all().order_by('-id')
        serializer = DocumentSerializer(files, many=True)
        return Response({'status':'success', 'files': serializer.data}, status=status.HTTP_200_OK)


class BaseFileDownloadView(DetailView):
    def get(self, request, *args, **kwargs):
        filename = self.kwargs.get('filename', None)
        if filename is None:
            raise ValueError("Found empty filename")
        some_file = self.model.objects.get(rdoc="rdocs"+"/"+filename)
        some_file.download += 1
        some_file.save()
        response = FileResponse(some_file.rdoc, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response


class BaseFileDownloadViewMultiple(APIView):
    model = Document

    def post(self, request, *args, **kwargs):

        filenames = request.data['data']
        zip_subdir = "somefiles"
        zip_filename = "%s.zip" % zip_subdir
        # Open StringIO to grab in-memory ZIP contents
        s = BytesIO()
        # The zip compressor
        zf = zipfile.ZipFile(s, "w")
        files = []
        for filename in filenames:
            some_file = self.model.objects.get(rdoc="rdocs" + "/" + filename)
            some_file.download += 1
            files.append(some_file)
            some_file.save()

        for file in filenames:
            zf.write((os.path.dirname(os.path.abspath(__file__)) + '/media/rdocs/' + file).replace('/api', ''),
                  file)
        zf.close()
        resp = HttpResponse(s.getvalue(), content_type="application/zip")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp


class SomeFileDownloadView(BaseFileDownloadView):
    model = Document


class Link(ModelViewSet):
    lookup_field = "link"
    serializer_class = LinkSerializer
    queryset = LinkToDownload.objects.all()
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if timezone.now() > instance.expire:
            return Response("Link has expired", status=403)
        response = FileResponse(instance.url.rdoc, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.url.rdoc
        return response


class LinkDetails(ReadOnlyModelViewSet):
    lookup_field = "link"
    serializer_class = LinkDetailsSerializer
    queryset = LinkToDownload.objects.all()
    permission_classes = (permissions.AllowAny,)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })