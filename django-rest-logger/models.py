from django.db import models
import json
from django.conf import settings
# Create your models here.
from django.http.request import QueryDict


class RequestResponseNote(models.Model):
    date = models.DateTimeField(auto_now=True)
    url = models.TextField()
    method = models.CharField(max_length=10)
    ip = models.GenericIPAddressField(blank=True, null=True)
    request_content_type = models.CharField(max_length=255, null=True, blank=True)
    request_body = models.TextField(null=True, blank=True)
    request_headers = models.TextField(null=True, blank=True)
    request_query_params = models.TextField(null=True, blank=True)
    response_status_code = models.IntegerField('Status_code', null=False)
    response_body = models.TextField(null=True, blank=True)
    response_content_type = models.CharField(max_length=255, blank=True, null=True)
    response_headers = models.TextField(null=True, blank=True)
    process_time = models.TextField(null=True, blank=True)
    user_name = models.TextField(null=True, blank=True)

    def set_request_headers(self, headers_dict: dict):
        s = ''
        for key, value in headers_dict.items():
            s += '{}: {}\n'.format(key, value)

        self.request_headers = s

    def get_request_headers_array(self):
        return self.request_headers.split('\n')

    def set_response_header(self, headers_dict: dict):
        s = ''
        for key, value in headers_dict.items():
            s += '{}: {}\n'.format(key, value)

        self.response_headers = s

    def get_response_headers(self):
        return self.response_headers

    def set_request_query_params(self, params: QueryDict):
        s = ''
        for key, value in params.lists():
            s += '{}: {}\n'.format(key, str(value) if len(value) > 1 else str(value[0]))
        self.request_query_params = s

    def get_request_query_params(self):
        return self.request_query_params

    def get_code_first_digit(self):
        return self.response_status_code//100

    def get_short_body(self):
        if len(self.response_body) > 1000:
            return self.response_body[:1000] + '....'
        else:
            return self.response_body

    def save(self, *args, **kwargs):
        super(RequestResponseNote, self).save(*args, **kwargs)
        max_log = getattr(settings, 'LOGGING_MAX_COUNT', 100)
        assert isinstance(max_log, int), 'LOGGING_MAX_COUNT must be a number!'
        count = RequestResponseNote.objects.count()
        while count >= max_log:
            note = RequestResponseNote.objects.first()
            note.delete()
            count = RequestResponseNote.objects.count()
