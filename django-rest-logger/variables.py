# coding=utf-8
from django.conf import settings

__author__ = 'Altuhov Kirill'

REQUEST_HEADERS = ['HTTP_USER_AGENT', 'HTTP_AUTHORIZATION', ]
RESPONSE_HEADERS = []
RECEIVED_REQUEST_CONTENT_TYPE = ['application/json', 'application/xml', 'multipart/form-data',
                                 'application/x-www-form-urlencoded', ]
RECEIVED_RESPONSE_CONTENT_TYPE = ['application/json', 'application/xml', ]
START_PATH_ACCEPT = ['/api/', ]


def get_request_headers_names():
    headers = getattr(settings, 'LOGGING_REQUEST_HEADERS', None)
    if not headers:
        return REQUEST_HEADERS
    else:
        assert isinstance(headers, list), 'settings.LOGGING_REQUEST_HEADERS must be a list!'
        return headers


def get_received_request_content_types():
    content_types = getattr(settings, 'LOGGING_RECEIVED_REQUEST_CONTENT_TYPES', None)
    if not content_types:
        return RECEIVED_REQUEST_CONTENT_TYPE
    else:
        assert isinstance(content_types, list), 'settings.LOGGING_RECEIVED_REQUEST_CONTENT_TYPES must be a list!'
        return content_types


def get_received_response_content_types():
    content_types = getattr(settings, 'LOGGING_RECEIVED_RESPONSE_CONTENT_TYPES', None)
    if not content_types:
        return RECEIVED_RESPONSE_CONTENT_TYPE
    else:
        assert isinstance(content_types, list), 'settings.LOGGING_RECEIVED_RESPONSE_CONTENT_TYPES must be a list!'
        return content_types


def get_start_path_accept():
    paths = getattr(settings, 'LOGGING_START_PATH_ACCEPT', None)
    if not paths:
        return START_PATH_ACCEPT
    else:
        assert isinstance(paths, list), 'settings.LOGGING_START_PATH_ACCEPT must be a list!'
        return paths


def get_response_headers():
    headers = getattr(settings, 'LOGGING_RESPONSE_HEADERS', None)
    if not headers:
        return RESPONSE_HEADERS
    else:
        assert isinstance(headers, list), 'settings.LOGGING_RESPONSE_HEADERS must be a list!'
        return headers


def show_user_name():
    show = getattr(settings, 'SHOW_USER_NAME', False)
    if show:
        assert getattr(settings, 'USER_NAME_FUNC', None) is not None
        return True
    return False


def get_user_name_func():
    return getattr(settings, 'USER_NAME_FUNC', None)

