# API Benchmark: Flask vs FastAPI

Сервис для сравнительного анализа производительности Flask и FastAPI. Реализует идентичный CRUD функционал для списка задач, позволяя на практике увидеть разницу между синхронным и асинхронным подходами.

## Запуск

Сначала установите зависимости:
```bash
pip install -r requirements.txt
```

Запуск Flask (синхронный режим):
```bash
python main.py --framework flask
```

Запуск FastAPI (асинхронный режим):
```bash
python main.py --framework fastapi
```

## Пример

Пример запроса через `curl` для создания новой задачи:

```bash
# Для Flask (по умолчанию на 5000)
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title": "Купить молоко", "completed": false}'

# Для FastAPI (по умолчанию на 8000)
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Купить молоко", "completed": false}'
```

## Тесты

Для запуска всех тестов используйте команду:
```bash
python -m unittest discover -s tests -v
```
