from django.contrib import admin
from api.models import Document

@admin.register(Document)
class DocumentModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'rdoc']

