Команды Makefile (запуск через `uv`):

- `make init` — создать виртуальное окружение `.venv` и синхронизировать зависимости (`uv sync --dev`).
- `make install` — установить зависимости в окружение (`uv sync --dev`).
- `make run` — запустить dev-сервер (uvicorn + SSL + reload).
- `make migrate` — создать таблицы напрямую из моделей (не миграции).
- `make revision REV_MSG="message"` — создать alembic миграцию (`--autogenerate`).
- `make upgrade` — применить alembic миграции (`head`).
- `make lint` — запустить pylint.
- `make mypy` — запустить mypy.
- `make test` — запустить pytest.
- `make check` — compileall + mypy + lint + tests (для pre-commit).
- `make clean` — удалить `__pycache__`, `*.pyc` и `./test.db`.

Миграции Alembic:

добавить модель → добавить её импорт в `app/models/__init__.py` → запустить `make revision REV_MSG="..."` → проверить файл в `alembic/versions/` → применить `make upgrade`.
