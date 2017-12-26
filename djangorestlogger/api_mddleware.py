#-*- coding: utf-8 -*-
import logging

from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_str
from ipware.ip import get_real_ip
from rest_framework.request import Request
from django.utils.translation import ugettext_lazy as _

from core.models import User

__author__ = 'Altuhov Kirill'
"""
Api middleware module
"""

request_logger = logging.getLogger('api.request.logger')
error_log = logging.getLogger(__name__)


class LoggingMiddleware(MiddlewareMixin):
    """
    Provides full logging of requests and responses
    """
    _initial_http_body = None
    _post_dict = None
    _files_dict = None
    _start_time = None
    _end_time = None

    REQUEST_HEADERS = ['CONTENT_TYPE', 'HTTP_AUTHORIZATION', 'HTTP_SPORT', 'HTTP_ROLE']
    RESPONSE_HEADERS = ['Content-Type', ]
    RECEIVED_REQUEST_CONTENT_TYPE = ['application/json', 'application/xml', 'multipart/form-data',
                                     'application/x-www-form-urlencoded', ]
    RECEIVED_RESPONSE_CONTENT_TYPE = ['application/json', 'application/xml', ]
    IP_HEADER = ['X-Forwarded-For', 'X-Real-IP', 'REMOTE_ADDR', ]
    START_PATH_ACCEPT = ['/api/', ]
    LOG_LEVEL = logging.INFO

    MAX_RESPONSE_PART_LEN = 10000

    def process_request(self, request):
        self._start_time = datetime.now()
        self._initial_http_body = request.body
        if (request.POST):
            self._post_dict = request.POST
        if request.FILES:
            self._files_dict = request.FILES


    def create_first_line(self, request, response):
        log_str = '{method}: {path} code: {code}\n'\
            .format(method=request.method,
                    path=request.path,
                    code=response.status_code
                    )
        return log_str

    def create_request_part(self, request, response):
        request_part = '\trequest:\n'

        # Client IP
        # for ip_header in self.IP_HEADER:
        #     ip = request.META.get(ip_header)
        #     if ip:
        #         request_part += '\t\tClient IP: {ip}\n'.format(ip=ip)
        #         break
        ip = get_real_ip(request)
        request_part += '\t\tClient IP: {ip}\n'.format(ip=ip)

        # Headers
        request_headers = self.REQUEST_HEADERS
        if request_headers and request_headers.count != 0:
            for header in request_headers:
                if request.META.get(header):
                    request_part += '\t\t{header_name} : "{header_content}"\n'.format(header_name=header,
                                                                                      header_content=request.META.get(header))

        # Query params
        params_dict = request.GET
        if params_dict and len(params_dict) != 0:
            request_part += '\t\tQuery params:\n'
            for k, v in params_dict.lists():
                request_part += '\t\t\t {key} : {value} \n'.format(key=k, value=str(v) if len(v) > 1 else str(v[0]))

        # Body
        if request.META.get('CONTENT_TYPE'):
            content_type = request.META.get('CONTENT_TYPE')
            for ct in self.RECEIVED_REQUEST_CONTENT_TYPE:
                if content_type.startswith(ct):
                    break
            else:
                return request_part

            body = ''

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
                    error_log.warning('Problem with parsing request. content_type: {}'.format(content_type))
            good_looking_body = '\t\t\t' + body.replace('\n', '\n\t\t\t')
            request_part += '\t\tBody:\n {body}\n'.format(body=good_looking_body)



            # if content_type.startswith('multipart/form-data'):
            #     print(len(request.POST))
            #     print(self._initial_http_body)
            #     body = ''
            #     # try:
            #     #     body = self.goodLookingBodyFormUrlencoded()
            #     # except:
            #     #     body = 'Не удалось расшифровать'
            # else:
            #     request_body_decoded = self._initial_http_body.decode("utf-8")
            #     if request_body_decoded and len(request_body_decoded) != 0:
            #         if 'application/x-www-form-urlencoded' in self.RECEIVED_REQUEST_CONTENT_TYPE and \
            #                 request.META.get('CONTENT_TYPE').startswith('application/x-www-form-urlencoded'):
            #             try:
            #                 body = self.parseFormParams()
            #             except:
            #                 body = request_body_decoded
            #         else:
            #             body = request_body_decoded
            # good_looking_body = '\t\t\t' + body.replace('\n', '\n\t\t\t')
            # request_part += '\t\tBody:\n {body}\n'.format(body=good_looking_body)

        return request_part

    def parseFormParams(self):
        s = ''
        if self._post_dict:
            for key, val in self._post_dict.items():
                s += '{} : {}\n'.format(key, val)
        return s

    def parsFilesParams(self):
        s = ''
        if self._files_dict:
            for key, val in self._files_dict.items():
                param = '{key} : file (name: "{name}", size: {size}kb, content_type: {type})\n'\
                    .format(key=key, name=val.name, size=round(val.size/1024, 2), type=val.content_type)
                s += param
        return s


    def create_response_part(self, request, response):
        response_part = '\tresponse:\n'

        # Headers
        response_headers = self.RESPONSE_HEADERS
        if response_headers and response_headers.count != 0:
            for header in response_headers:
                if response.get(header):
                    response_part += '\t\t{header_name} : "{header_content}"\n'.format(header_name=header,
                                                                                       header_content=response[header])
        # Body
        if response.get('Content-Type') and response['Content-Type'] in self.RECEIVED_RESPONSE_CONTENT_TYPE:
            response_body_decoded = response.content.decode("utf-8")
            if response_body_decoded and len(response_body_decoded) != 0:
                if len(response_body_decoded) > self.MAX_RESPONSE_PART_LEN:
                    response_body_decoded = response_body_decoded[:self.MAX_RESPONSE_PART_LEN] + '.......'
                good_looking_body = '\t\t\t' + response_body_decoded.replace('\n', '\n\t\t\t')
                response_part += '\t\tBody:\n {body}\n'.format(body=good_looking_body)
        else:
            response_part += '\t\tBody:\n \t\t\t{body}\n'.format(body='None')

        return response_part

    def create_processing_part(self):
        delta = self._end_time - self._start_time
        # time = '{s}.{ms:0>3} {mks:0>3}'.format(s=delta.seconds, ms=delta.microseconds//1000, mks=delta.microseconds % 1000)
        return '\tprocess time: {}\n'.format(delta.total_seconds())

    def process_response(self, request, response):
        self._end_time = datetime.now()
        try:
            if request_logger.level > self.LOG_LEVEL:
                return response
            for path in self.START_PATH_ACCEPT:
                if request.path.startswith(path):
                    break
            else:
                return response
            log_str = ''
            log_str += self.create_first_line(request, response)
            log_str += self.create_processing_part()
            log_str += self.create_request_part(request, response)
            log_str += self.create_response_part(request, response)
            request_logger.info(log_str)
        except Exception as e:
            error_log.exception(e)
        return response
