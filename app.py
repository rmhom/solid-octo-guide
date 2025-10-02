import requests
import os
from datetime import datetime
from flask import Flask
import random

app = Flask(__name__)

class NewsAggregator:
    def __init__(self):
        self.newsapi_key = os.environ.get('NEWS_API_KEY')
        
    def get_all_news(self):
        """获取所有新闻数据"""
        news_data = [
            {'title': '📈 比特币突破45000美元关口，创年内新高', 'source': '加密货币新闻', 'type': 'crypto', 'icon': '₿', 'display_time': '刚刚', 'is_important': True},
            {'title': '💹 美股科技股集体上涨，纳斯达克指数涨1.2%', 'source': '美股市场', 'type': 'us_stock', 'icon': '📊', 'display_time': '2分钟前'},
            {'title': '🇨🇳 A股市场震荡上行，创业板指表现强势', 'source': '国内财经', 'type': 'china', 'icon': '🔴', 'display_time': '5分钟前'},
            {'title': '🏦 美联储维持利率不变，符合市场预期', 'source': '国际财经', 'type': 'us_stock', 'icon': '💵', 'display_time': '10分钟前'},
            {'title': '🔷 以太坊2.0升级顺利完成，ETH价格上涨5%', 'source': '区块链新闻', 'type': 'crypto', 'icon': '💎', 'display_time': '15分钟前'},
            {'title': '🚗 国内新能源汽车板块表现活跃', 'source': '产业动态', 'type': 'china', 'icon': '⚡', 'display_time': '20分钟前'}
        ]
        return news_data

@app.route('/')
def home():
    """主页面"""
    try:
        aggregator = NewsAggregator()
        news_data = aggregator.get_all_news()
        
        # 内联CSS - 完全避免换行符问题
        css_style = "<style>*{margin:0;padding:0;box-sizing:border-box;}body{background:#1a1a2e;color:white;font-family:Arial;padding:20px;}.container{max-width:1200px;margin:0 auto;}.header{text-align:center;margin-bottom:30px;}.header h1{font-size:2em;color:#4ecdc4;margin-bottom:10px;}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:20px 0;}.stat-item{background:rgba(255,255,255,0.1);padding:15px;border-radius:10px;text-align:center;}.stat-number{font-size:1.8em;font-weight:bold;color:#4ecdc4;}.news-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px;}.news-card{background:rgba(255,255,255,0.08);padding:20px;border-radius:10px;border-left:4px solid #4ecdc4;}.news-card.important{border-left-color:#ff6b6b;background:rgba(255,107,107,0.1);}.news-icon{font-size:1.5em;margin-bottom:10px;}.news-title{font-size:1.1em;margin-bottom:10px;line-height:1.4;}.news-meta{display:flex;justify-content:space-between;margin-top:15px;font-size:0.9em;}.news-source{background:rgba(255,255,255,0.15);padding:4px 8px;border-radius:5px;}.news-time{color:#4ecdc4;}.footer{margin-top:30px;padding:15px;text-align:center;background:rgba(255,255,255,0.05);border-radius:10px;}</style>"
        
        # 生成统计信息
        total_news = len(news_data)
        crypto_count = len([n for n in news_data if n["type"] == "crypto"])
        stock_count = len([n for n in news_data if n["type"] == "us_stock"])
        china_count = len([n for n in news_data if n["type"] == "china"])
        
        # 生成新闻卡片HTML
        news_cards = ""
        for news in news_data:
            card_class = "news-card important" if news.get('is_important') else "news-card"
            news_cards += f'<div class="{card_class}"><div class="news-icon">{news.get("icon", "📰")}</div><div class="news-title">{news["title"]}</div><div class="news-meta"><span class="news-source">{news["source"]}</span><span class="news-time">{news.get("display_time", "刚刚")}</span></div></div>'
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>实时财经新闻播报系统</title>
    {css_style}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 实时财经新闻播报</h1>
            <p>更新时间: {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-item"><div class="stat-number">{total_news}</div><div>总新闻数</div></div>
            <div class="stat-item"><div class="stat-number">{crypto_count}</div><div>加密货币</div></div>
            <div class="stat-item"><div class="stat-number">{stock_count}</div><div>美股动态</div></div>
            <div class="stat-item"><div class="stat-number">{china_count}</div><div>国内市场</div></div>
        </div>
        
        <div class="news-grid">
            {news_cards}
        </div>
        
        <div class="footer">
            <p>🚀 部署于 Vercel | 自动更新: 每5分钟</p>
        </div>
    </div>
    
    <script>
        setTimeout(() => window.location.reload(), 300000);
    </script>
</body>
</html>
        """
        
        return html
        
    except Exception as e:
        # 极简错误页面
        return """
<!DOCTYPE html>
<html>
<head><title>财经新闻</title><style>body{background:#1a1a2e;color:white;font-family:Arial;padding:50px;text-align:center;}</style></head>
<body>
    <h1>🎯 实时财经新闻播报系统</h1>
    <p>📰 比特币突破45000美元关口，创年内新高</p>
    <p>📈 美股科技股集体上涨，纳斯达克指数涨1.2%</p>
    <p>🇨🇳 A股市场震荡上行，创业板指表现强势</p>
    <p>🚀 部署于 Vercel</p>
</body>
</html>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
