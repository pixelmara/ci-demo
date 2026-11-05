"""Собирает статическую версию приложения в папку public/ для GitHub Pages."""
import json
import os
from pathlib import Path

from app import app

out = Path("public")
out.mkdir(exist_ok=True)

client = app.test_client()
data = client.get("/").get_json()
total = client.get("/add/2/3").get_json()["result"]
version = os.environ.get("CIRCLE_SHA1", "local")[:7]

html = f"""<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>ci-demo</title></head>
<body>
  <h1>{data["message"]}</h1>
  <p>Статус: {data["status"]}</p>
  <p>2 + 3 = {total}</p>
  <p>Версия (коммит): {version}</p>
</body>
</html>
"""
(out / "index.html").write_text(html, encoding="utf-8")
(out / "api.json").write_text(json.dumps(data), encoding="utf-8")
(out / ".nojekyll").write_text("")
print("Сайт собран в", out.resolve())
