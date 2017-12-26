import datetime
import os
from os import listdir
from os.path import isfile, join, isdir
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from djangorestlogger.models import RequestResponseNote
from djangorestlogger.variables import show_user_name

try:
    DIR = settings.LOG_DIR
except:
    raise ImproperlyConfigured()


# def get_index_page(request):
#     files = [f for f in listdir(DIR) if isfile(join(DIR, f)) and not f.startswith('.')]
#     files.sort(key=lambda x: os.stat(os.path.join(DIR, x)).st_mtime)
#     files.reverse()
#     t = os.path.getmtime(os.path.join(DIR, files[0]))
#     last_request = datetime.datetime.fromtimestamp(t)
#     dirs = list()
#     return render(request, 'index.html', {'files': files, 'last_request': last_request, 'dirs': dirs})
#
#
# def get_log_file(request, path):
#     if path.endswith('/'):
#         path = path[:-1]
#     if not os.path.exists(path):
#         return HttpResponse("file don't exist", status=HTTP_404_NOT_FOUND)
#     if not os.path.isfile(path):
#         return HttpResponse('is not file', status=HTTP_404_NOT_FOUND)
#     try:
#         f = open(join(DIR, path), 'r', encoding='utf8')
#     except FileNotFoundError:
#         return HttpResponse("file don't exist", status=HTTP_404_NOT_FOUND)
#     content = f.read()
#     return HttpResponse(content, content_type="text/plain charset=utf-8")
#
#
# def get_path(request, path):
#     if path.endswith('/'):
#         path = path[:-1]
#     real_path = os.path.join(DIR, path)
#     if not os.path.exists(real_path):
#         return HttpResponse("file or dir don't exist", status=HTTP_404_NOT_FOUND)
#     if os.path.isdir(real_path):
#         files = [f for f in listdir(real_path) if isfile(join(real_path, f)) and not f.startswith('.')]
#         dirs = [d for d in listdir(real_path) if isdir(join(real_path, d)) and not d.startswith('.')]
#         files.sort(key=lambda x: os.stat(os.path.join(real_path, x)).st_mtime)
#         files.reverse()
#         dirs.sort()
#         if len(files) > 0:
#             t = os.path.getmtime(os.path.join(real_path, files[0]))
#             last_request = datetime.datetime.fromtimestamp(t)
#         else:
#             last_request = ' '
#
#         return render(request, 'index.html', {'files': files, 'last_request': last_request, 'dirs': dirs})
#     if os.path.isfile(real_path):
#         try:
#             f = open(join(DIR, path), 'r', encoding='utf8')
#         except FileNotFoundError:
#             return HttpResponse("file don't exist", status=HTTP_404_NOT_FOUND)
#         content = f.read()
#         return HttpResponse(content, content_type="text/plain charset=utf-8")
#     return HTTP_500_INTERNAL_SERVER_ERROR('ERROR((')


def get_viewer(request):
    logs = RequestResponseNote.objects
    code = request.GET.get('filter_code', None)
    url = request.GET.get('filter_url', None)
    method = request.GET.get('filter_method', None)
    count = request.GET.get('filter_count', 100)
    open_body = request.GET.get('open_body', None)
    if open_body == None:
        from_session = request.session.get('open_body', None)
        if not from_session:
            from_session = False
        open_body = from_session
    if open_body == 'on':
        open_body = True
    if open_body == 'False':
        open_body = False
    request.session['open_body'] = open_body
    if code:
        logs = logs.filter(response_status_code=code)
    if url:
        logs = logs.filter(url__icontains=url)
    if method:
        logs = logs.filter(method__iexact=method)

    logs = logs.order_by('-date').all()
    if count:
        count = int(count)
        logs = logs[:count]
    return render(request, 'viewer.html', {'logs': logs, 'code': code, 'url': url, 'method': method,
                                           'count': count, 'open_body': open_body, 'show_name': show_user_name()})


def get_body(request, pk):
    log = get_object_or_404(RequestResponseNote, pk=pk)

    return HttpResponse(log.response_body, content_type="text/plain charset=utf-8")
