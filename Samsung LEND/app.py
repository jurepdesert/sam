#!/usr/bin/env python3
"""
Flask backend — получает данные YouTube канала через yt-dlp
Запуск: pip install flask yt-dlp flask-cors && python app.py
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp
import re

app = Flask(__name__)
CORS(app)  # разрешаем запросы с фронтенда

def format_number(n):
    if n is None:
        return "N/A"
    n = int(n)
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)

def get_channel_url(raw: str) -> str:
    """Нормализует ссылку на канал"""
    raw = raw.strip()
    if raw.startswith("@"):
        return f"https://www.youtube.com/{raw}"
    if "youtube.com" in raw:
        return raw if raw.startswith("http") else "https://" + raw
    return f"https://www.youtube.com/@{raw}"

@app.route("/channel", methods=["GET"])
def channel():
    url_param = request.args.get("url", "").strip()
    if not url_param:
        return jsonify({"error": "No URL provided"}), 400

    channel_url = get_channel_url(url_param)

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,       # не скачивать видео
        "playlistend": 1,           # берём только 1 запись чтобы быстро
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

        if not info:
            return jsonify({"error": "Channel not found"}), 404

        # yt-dlp возвращает разные поля в зависимости от типа
        name        = info.get("uploader") or info.get("channel") or info.get("title") or "Unknown"
        channel_id  = info.get("channel_id") or info.get("uploader_id") or ""
        subscribers = info.get("channel_follower_count") or info.get("follower_count")
        video_count = info.get("playlist_count") or info.get("video_count")
        view_count  = info.get("view_count")
        thumbnail   = info.get("thumbnails", [{}])[-1].get("url") if info.get("thumbnails") else None
        description = (info.get("description") or "")[:200]

        # Формируем ссылку
        if channel_id:
            clean_url = f"youtube.com/channel/{channel_id}"
        else:
            clean_url = channel_url.replace("https://", "").replace("http://", "")

        return jsonify({
            "name":        name,
            "channel_id":  channel_id,
            "subscribers": format_number(subscribers),
            "subscribers_raw": subscribers,
            "videos":      format_number(video_count),
            "videos_raw":  video_count,
            "views":       format_number(view_count),
            "views_raw":   view_count,
            "thumbnail":   thumbnail,
            "description": description,
            "url":         clean_url,
            "channel_url": channel_url,
        })

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"yt-dlp error: {str(e)[:200]}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)[:200]}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("\n=== Creator Portal Backend ===")
    print("Запускается на http://localhost:5000")
    print("Фронтенд открывай: index.html в браузере\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
