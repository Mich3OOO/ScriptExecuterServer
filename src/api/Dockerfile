
FROM python:3.9


WORKDIR /app


COPY ./ /app/


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


CMD ["fastapi", "run", "/app/main.py", "--port", "8000"]