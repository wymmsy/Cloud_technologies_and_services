# Отчёт о выполнении лабораторной работы 3
## _Обычная версия_

Плохой CI/CD файл
```
name: Bad CI/CD

on:
  push:
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@master
      
      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.9
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest || true

      - name: Debug info
        run: |
          echo "Listing root directory"
          ls -la /
```

Что с ним не так:  
1. Использование ```@master``` вместо зафиксированной версии, например ```checkout@v4```
2. Устаревшая версия Python 3.9
3. Нет кэша зависимостей, поэтому каждый билд скачивает их заново, чем замедляет работу файла
4. Полностью игнорирует результат работы тестов
5. Дебаггинг с выводом всей директории даёт лишний доступ к системе и может привести к утечкам
<img width="1889" height="934" alt="Screenshot from 2025-12-21 02-02-01" src="https://github.com/user-attachments/assets/473cc473-3a70-4121-902f-e0b096ee137b" />  
Хороший CI/CD файл

```
name: Good CI/CD

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

jobs:
  test:
    name: Test on Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest -v
```

Что исправлено:  
1. Зафиксированы версии checkout
2. Версии Python актуальные, код проверяется сразу с 3 версиями для проверки совместимости
3. Встроенное кэширование устанавливаемых пакетов
4. Благодаря ```pytest -v``` файл падает при ошибке в тестах
5. Дано разрешение только на чтение контента, что лучше с точки зрения безопасности
  
<img width="1889" height="862" alt="Screenshot from 2025-12-21 02-04-57" src="https://github.com/user-attachments/assets/e3338790-02b6-4dbc-a49e-56fe9940089c" />
