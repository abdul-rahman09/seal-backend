from django.db import models


class Document(models.Model):
    download= models.IntegerField(default=0)
    rdoc = models.FileField(upload_to='rdocs', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.rdoc.name.replace('rdocs/', '')

    @property
    def type(self):
        arr = self.rdoc.name.split('.')
        if len(arr) > 1:
            return self.rdoc.name.split('.')[-1]
        return ""


class LinkToDownload(models.Model):
    expire = models.DateTimeField(auto_now=False, auto_now_add=False)
    url = models.ForeignKey(Document, on_delete=models.CASCADE)
    link = models.CharField(max_length=100, default="")

