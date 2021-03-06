# Django REST logger

---

# Overview

This is the system for logging and viewing requests that your server processes. This package will be useful to the
backend developers to understand what parameters are sent by the client, and for the frontend developers to understand
what data they send and receive from the server.

# Installation

Install using `pip`

    pip install djangorestlogger

Add `'logging_viewer'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'logging_viewer',
    )

Add `'logging_viewer.middleware.DBLoggingMiddleware'` to your `MIDDLEWARE` setting.

    MIDDLEWARE = [
        'logging_viewer.middleware.DBLoggingMiddleware',
        ...
    ]

Add `'logging_viewer.middleware.DBLoggingMiddleware'` to your `MIDDLEWARE` setting.

    MIDDLEWARE = [
        'logging_viewer.middleware.DBLoggingMiddleware',
        ...
    ]

Add djangorestlogger urls to you urlpatterns.

    from djangorestlogger import urls as log_urls
    urlpatterns = [
        url(r'^logs/', include(log_urls)),
        ...
    ]

Open in browser 127.0.0.1/logs/viewer/

