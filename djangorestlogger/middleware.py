# coding=utf-8

import datetime
from logging_viewer.models import RequestResponseNote
from django.conf import settings
from logging_viewer import variables

import logging

from django.utils.deprecation import MiddlewareMixin
from ipware.ip import get_real_ip

from logging_viewer.variables import get_start_path_accept, get_request_headers_names, \
    get_received_request_content_types, get_response_headers, get_received_response_content_types, get_user_name_func, \
    show_user_name

__author__ = 'Altuhov Kirill'
"""
Api middleware module
"""

error_log = logging.getLogger(__name__)


class DBLoggingMiddleware(MiddlewareMixin):
    _model = None
    _post_dict = None
    _files_dict = None
    _initial_http_body = None
    _start_time = None

    def process_request(self, request):
        self.clean_data()
        self._start_time = datetime.datetime.now()
        try:
            self._model = RequestResponseNote()
            for path in get_start_path_accept():
                if request.path.startswith(path):
                    break
            else:
                return

            self._initial_http_body = request.body
            if (request.POST):
                self._post_dict = request.POST
            if request.FILES:
                self._files_dict = request.FILES

            self.setup_method(request)
            self.set_user_name(request)
            self.setup_url(request)
            self.setup_ip(request)
            self.setup_request_content_type(request)
            self.setup_request_headers(request)
            self.setup_request_query_params(request)
            self.setup_request_body(request)


        except Exception as e:
            error_log.exception('Problem in request handler')

    def process_response(self, request, response):
        try:
            for path in get_start_path_accept():
                if request.path.startswith(path):
                    break
            else:
                return response
            self.setup_response_body(response)
            self.setup_response_content_type(response)
            self.setup_response_headers(response)
            self.setup_response_status_code(response)
            self.setup_time()
            self._model.save()
            # RequestResponseNote.objects.create(url='/api/v1/recovery_pass/email/111', method='TEST',
            #                                    request_content_type='OLOL', response_status_code=100)
        except Exception as e:
            error_log.exception('problem in response handler')
        self.clean_data()
        return response

    def clean_data(self):
        self._model = None
        self._files_dict = None
        self._initial_http_body = None
        self._post_dict = None
        self._start_time = None

    def set_user_name(self, request):
        if show_user_name():
            func = get_user_name_func()
            if func is None:
                return
            self._model.user_name = func(request)

    def setup_method(self, request):
        self._model.method = request.method

    def setup_url(self, request):
        self._model.url = request.path

    def setup_ip(self, request):
        self._model.ip = get_real_ip(request)

    def setup_request_headers(self, request):
        headers_dict = dict()
        headers_names = get_request_headers_names()
        for header_name in headers_names:
            if request.META.get(header_name):
                headers_dict[header_name] = request.META.get(header_name)
        self._model.set_request_headers(headers_dict)

    def setup_request_query_params(self, request):
        self._model.set_request_query_params(request.GET)

    def setup_request_content_type(self, request):
        self._model.request_content_type = request.META.get('CONTENT_TYPE')

    def parseFormParams(self):
        s = ''
        if self._post_dict:
            for key, val in self._post_dict.items():
                s += '{} : {}\n'.format(key, val)
        elif self._initial_http_body:
            try:
                body = self._initial_http_body.decode("utf-8")
                pares = body.split('&')
                for pare in pares:
                    k_v = pare.split('=')
                    if len(k_v) != 2:
                        error_log.error("can't parse request body: {}".format(body))
                        continue
                    s += '{} : {}\n'.format(k_v[0], k_v[1])
            except:
                pass
        return s

    def parsFilesParams(self):
        s = ''
        if self._files_dict:
            for key, val in self._files_dict.items():
                param = '{key} : file (name: "{name}", size: {size}kb, content_type: {type})\n' \
                    .format(key=key, name=val.name, size=round(val.size / 1024, 2), type=val.content_type)
                s += param
        return s


    def setup_request_body(self, request):
        body = ''
        if request.META.get('CONTENT_TYPE'):
            content_type = request.META.get('CONTENT_TYPE')
            for ct in get_received_request_content_types():
                if content_type.startswith(ct):
                    break
            else:
                return

            if content_type.startswith('application/x-www-form-urlencoded'):
                body = self.parseFormParams()

            elif content_type.startswith('multipart/form-data'):
                body = self.parseFormParams()
                body += self.parsFilesParams()

            else:
                try:
                    request_body_decoded = self._initial_http_body.decode("utf-8")
                    if request_body_decoded and len(request_body_decoded) != 0:
                        body = request_body_decoded
                except Exception as e:
                    error_log.exception('Problem with parsing request. content_type: {}'.format(content_type))


        self._model.request_body = body

    def good_looking_body_form_urlencoded(self, request):
        s = ''
        for key, val in request.POST.items():
            s += '{} : {}\n'.format(key, val)
        return s

    def setup_response_headers(self, response):
        headers_dict = dict()
        response_headers = get_response_headers()
        if response_headers and response_headers.count != 0:
            for header in response_headers:
                if response.get(header):
                    headers_dict[header] = response.get(header)
        self._model.set_response_header(headers_dict)

    def setup_response_body(self, response):
        body = ''

        for received_header in get_received_response_content_types():
            if response.get('Content-Type') and response.get('Content-Type').startswith(received_header):
                response_body_decoded = response.content.decode("utf-8")
                if response_body_decoded and len(response_body_decoded) != 0:
                    body=response_body_decoded
                    break
        self._model.response_body = body

    def setup_response_content_type(self, response):
        self._model.response_content_type = response.get('Content-Type')

    def setup_response_status_code(self, response):
        self._model.response_status_code = response.status_code

    def setup_time(self):
        end_time = datetime.datetime.now()
        delta = end_time - self._start_time
        self._model.process_time = str(delta.total_seconds())

