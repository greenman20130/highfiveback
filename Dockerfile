# Versions
ARG PYTHON=python:3.10-alpine
## Stage one ##
FROM $PYTHON AS build
WORKDIR /usr/app
ARG BUILD_VERSION

# Установка C зависимостей
RUN apk add --no-cache --update \
            gcc \
            libc-dev \
            linux-headers \
            postgresql-dev \
            libusb-dev \
            libffi-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей python
RUN python3 -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"
COPY requirements/base.txt ./requirements.txt
RUN pip install -r requirements.txt

## Stage two ##
FROM $PYTHON
ARG BUILD_VERSION

# Установка зависимостей C, создание пользователя
RUN apk add --no-cache libusb-dev \
 && adduser -D cobra \
 && mkdir /usr/app \
 && chown cobra:cobra /usr/app
WORKDIR /usr/app

# Подготовка кода и окружения
COPY --chown=cobra:cobra --from=build /usr/app/venv ./venv
COPY --chown=cobra:cobra /src ./src

# Settings
USER cobra
ENV PATH="/usr/app/venv/bin:$PATH"
EXPOSE 8000

# Переменные среды
ENV BUILD_VERSION=${BUILD_VERSION:-noversion}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Metadata
LABEL app.version="${BUILD_VERSION}"

# Запуск
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
CMD ["--port", "8000", "--proxy-headers"]
HEALTHCHECK --interval=7s --timeout=3s --start-period=60s \
        CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ping

