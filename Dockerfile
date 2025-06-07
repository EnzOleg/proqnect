FROM python:3.11

WORKDIR /proqnect

COPY . /proqnect

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "proqnect.asgi:application"]
