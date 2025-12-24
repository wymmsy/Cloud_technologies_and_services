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
