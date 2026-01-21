# Название виртуального окружения
VENV=.venv

# Команды
.PHONY: init install run migrate clean revision upgrade lint mypy test check

# Создание виртуального окружения и установка зависимостей
init:
	uv venv $(VENV)
	uv sync --dev

# Установка зависимостей
install:
	uv sync --dev

# Запуск сервера разработки
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile ./certs/192.168.10.146-key.pem --ssl-certfile ./certs/192.168.10.146.pem --reload

# Инициализация базы данных
migrate:
	uv run python -c "from app.core.database import engine; from app.models.base_model import BaseModel; BaseModel.metadata.create_all(bind=engine)"

# Очистка (удаление базы и кэшей)
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -f ./test.db

# Alembic миграции
REV_MSG ?= "migration"
revision:
	uv run alembic revision --autogenerate -m "$(REV_MSG)"

upgrade:
	uv run alembic upgrade head

lint:
	uv run pylint app/

mypy:
	uv run mypy app/

test:
	uv run pytest || { code=$$?; if [ $$code -eq 5 ]; then exit 0; fi; exit $$code; }

check:
	uv run python -m compileall app/
	$(MAKE) mypy
	$(MAKE) lint
	$(MAKE) test
