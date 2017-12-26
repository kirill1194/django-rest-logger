# [Django REST logger][docs]

---

# Overview

This is the system for logging and viewing requests that your server processes. This package will be useful to the
backend developers to understand what parameters are sent by the client, and for the frontend developers to understand
what data they send and receive from the server.

# Installation

Install using `pip`

    pip install djangorestlogger

Add `'rest_framework'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'logging_viewer',
    )

Add `'logging_viewer.middleware.DBLoggingMiddleware'` to your `MIDDLEWARE` setting.

    MIDDLEWARE = [
        'logging_viewer.middleware.DBLoggingMiddleware',
        ...
    ]