from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import ModelAdmin

from logging_viewer.models import RequestResponseNote

@admin.register(RequestResponseNote)
class RequestResponseNoteAdmin(ModelAdmin):
    list_display = ['pk','date', 'url', 'method', 'response_status_code']
    list_display_links = list_display

