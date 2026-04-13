FROM python:3.12-slim
ARG APP_VERSION=dev
ARG GIT_SHA=dev
ARG BUILD_TIME=dev
ENV APP_VERSION=${APP_VERSION} GIT_SHA=${GIT_SHA} BUILD_TIME=${BUILD_TIME}
RUN useradd -u 1001 -m appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]