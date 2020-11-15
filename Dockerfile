FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y gettext libgettextpo-dev libfontconfig wkhtmltopdf
RUN mkdir /django_project
WORKDIR /django_project/django_project
RUN pip install --upgrade pip
ADD ./requirements.txt /django_project/
RUN pip install -r ../requirements.txt
ADD ./django_project /django_project/django_project/
