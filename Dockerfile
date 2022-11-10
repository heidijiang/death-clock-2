FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get install -y --no-install-recommends g++ && \
    apt-get install libfreetype6-dev -y && \
    apt-get install libxft-dev -y && \
    python -m pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]