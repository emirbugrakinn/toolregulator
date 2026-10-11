import time
import random
import requests
import os
from flask import Flask, render_template_string

app = Flask(__name__)

def auto_seo_generator(tool_name):
    high_revenue_hooks = ["Free", "Best", "2026", "No Sign-up", "Top"]
    hooks = random.sample(high_revenue_hooks, 2)
    category = random.choice(["AI Tool", "Developer", "Productivity"])
    seo_title = f"{hooks[0]} {tool_name} {hooks[1]} - {category}"
    url_slug = tool_name.lower().replace(" ", "-") + f"-{hooks[0].lower()}"
    return seo_title, url_slug, category

def fetch_live_tools():
    try:
        response = requests.get("https://hacker-news.firebaseio.com/v0/showstories.json", timeout=5)
        story_ids = response.json()[:10]
        
        live_data = []
        for index, sid in enumerate(story_ids):
            item_res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5).json()
            if 'title' in item_res and 'url' in item_res:
                name = item_res['title'].replace("Show HN: ", "")
                seo_title, url_slug, category = auto_seo_generator(name)
                
                live_data.append({
                    "badge": f"Trend #{index+1}",
                    "category": category,
                    "title": seo_title,
                    "description": f"Bugün keşfedilen en güncel araçlardan biri. Küresel geliştirici topluluğu tarafından oylandı. (Skor: {item_res.get('score', 0)})",
                    "url": item_res['url']
                })
        return live_data
    except Exception as e:
        return [
            {"badge": "Trend #1", "category": "AI Tool", "title": "Free AutoCoder 2026 - AI Tool", "description": "Bağlantı hatası durumunda gösterilen yedek veri.", "url": "#"}
        ]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToolRegulator - Best Free Tech & AI Tools 2026</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0b1120; color: #f8fafc; margin: 0; padding: 40px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; border-bottom: 1px solid #1e293b; padding-bottom: 20px; }
        h1 { font-size: 32px; margin: 0; color: #10b981; letter-spacing: -1px; }
        .subtitle { color: #94a3b8; font-size: 16px; margin-top: 5px; }
        .sponsor-btn { background: #3b82f6; color: #fff; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px; transition: 0.2s; }
        .sponsor-btn:hover { background: #2563eb; }
        .card { background: #1e293b; border: 1px solid #334155; padding: 24px; border-radius: 12px; margin-bottom: 20px; transition: 0.2s; }
        .card:hover { border-color: #10b981; transform: translateY(-2px); }
        .badge { background: #064e3b; color: #34d399; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; float: right; }
        .category { font-size: 13px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
        .title { font-size: 20px; font-weight: 700; margin: 10px 0; color: #f1f5f9; }
        .desc { font-size: 15px; color: #cbd5e1; margin-bottom: 16px; line-height: 1.5; }
        .btn { display: inline-block; background: #10b981; color: #0b1120; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; }
        .btn:hover { background: #059669; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>ToolRegulator</h1>
                <div class="subtitle">Auto-curated registry of the best new tech tools. (Live Data)</div>
            </div>
            <a href="#" class="sponsor-btn">Submit a Tool ($15/day)</a>
        </div>
        
        {% for item in projects %}
        <div class="card">
            <span class="badge">{{ item.badge }}</span>
            <div class="category">{{ item.category }}</div>
            <div class="title">{{ item.title }}</div>
            <div class="desc">{{ item.description }}</div>
            <a target="_blank" href="{{ item.url }}" class="btn">Launch Tool</a>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    projects = fetch_live_tools()
    return render_template_string(HTML_TEMPLATE, projects=projects)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
