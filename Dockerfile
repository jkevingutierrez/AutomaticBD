# Start with a Python image.
FROM python:3.6

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get -y update

# Copy all our files into the image.
RUN mkdir /code
WORKDIR /code
COPY . /code/

# Install our requirements.
RUN pip install -U pip
RUN pip install -Ur requirements.txt

# Collect our static media.
RUN /code/manage.py collectstatic --noinput
