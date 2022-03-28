FROM python:3.10-alpine3.15
WORKDIR /app
COPY requirements.txt requirements.txt
COPY repositories /etc/apk/repositories
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install && \
    apk --purge del .build-deps
COPY /app .
CMD ["python3", "-u", "main.py"]