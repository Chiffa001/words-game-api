Создание миграций:

добавить модель → добавить её импорт в `app/models/__init__.py` → запустить `make revision` с REV_MSG. После чего `autogenerate` увидит новую таблицу

- Создать миграцию: `make revision REV_MSG="add users table"`
- Применить миграции: `make upgrade
