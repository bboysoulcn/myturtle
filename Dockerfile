FROM python:3.12.4-alpine3.20
WORKDIR /app
RUN pip install poetry==1.8.3
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install
COPY . .
CMD ["sh","-c","poetry run python main.py"]