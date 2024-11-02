FROM python:3.12
RUN apt-get update && apt-get install -y curl
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]