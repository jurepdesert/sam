# Creator Portal

## Установка и запуск

### 1. Установи зависимости
```bash
pip install flask flask-cors yt-dlp
```

### 2. Запусти бэкенд
```bash
python app.py
```
Сервер запустится на http://localhost:5000

### 3. Открой фронтенд
Просто открой файл `index.html` в браузере (двойной клик).

---

## Как это работает

- **index.html** — фронтенд (выбор языка → ввод ссылки → загрузка → статистика)
- **app.py** — бэкенд на Flask, использует `yt-dlp` для получения реальных данных канала

## Поддерживаемые форматы ссылок

```
https://youtube.com/@cnn
https://www.youtube.com/channel/UCxxxxxx
@cnn
youtube.com/@cnn
```

## Обновление yt-dlp

YouTube часто меняет API, поэтому обновляй yt-dlp регулярно:
```bash
pip install -U yt-dlp
```
