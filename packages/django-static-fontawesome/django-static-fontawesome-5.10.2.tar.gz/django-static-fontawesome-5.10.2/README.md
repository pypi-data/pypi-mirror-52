# django-static-fontawesome

Django application contain font-awesome static files

## Install

    pip install django-static-fontawesome

## Installed Resources

- all resource files of fontawesome-free-5.10.2-web.zip from https://fontawesome.com

## Settings

    INSTALLED_APPS = [
        ...
        "django_static_fontawesome",
        ...
    ]

## Use static files

    {% load staticfiles %}

    {% block style %}
        <link rel="stylesheet" type="text/css" href="{% static "fontawesome/css/all.min.css" %}" />
    {% endblock %}

    <i class="fa fa-home"></i> Home

## About release

- Release version sames with fontawesome version.
