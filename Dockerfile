FROM python:3.9.7-slim-buster
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get install -y --no-install-recommends g++ && \
    python -m pip install --upgrade pip
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app/app.py" ]