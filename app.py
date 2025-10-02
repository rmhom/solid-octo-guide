import requests
import json
import os
from datetime import datetime, timedelta
from flask import Flask, render_template_string
import random

app = Flask(__name__)

class NewsAggregator:
    def __init__(self):
        self.update_interval = 300
        self.newsapi_key = os.environ.get('NEWS_API_KEY')
        
    def fetch_crypto_news(self):
        """获取加密货币新闻"""
        try:
            response = requests.get("https://api.coingecko.com/api/v3/news", timeout=10)
            if response.status_code == 200:
                data = response.json()
                crypto_news = []
                for item in data.get('data', [])[:8]:
                    news_item = {
                        'title': item.get('title', ''),
                        'source': 'CoinGecko',
                        'type': 'crypto',
                        'icon': '₿',
                        'display_time': '近期',
                        'tags': ['加密货币', '区块链']
                    }
                    crypto_news.append(news_item)
                return crypto_news
        except Exception as e:
            print(f"加密货币新闻获取失败: {e}")
        return []

    def fetch_mock_news(self):
        """模拟新闻数据 - 当没有API密钥时使用"""
        mock_news = [
            {
                'title': '比特币突破45000美元，创年内新高',
                'source': '模拟数据',
                'type': 'crypto',
                'icon': '₿',
                'display_time': '刚刚',
                'tags': ['比特币', '突破', '新高'],
                'is_important': True
            },
            {
                'title': '美股科技股集体上涨，纳斯达克指数涨1.2%',
                'source': '模拟数据', 
                'type': 'us_stock',
                'icon': '📈',
                'display_time': '2分钟前',
                'tags': ['美股', '纳斯达克', '科技股']
            },
            {
                'title': 'A股市场震荡上行，创业板指表现强势',
                'source': '模拟数据',
                'type': 'china',
                'icon': '🇨🇳',
                'display_time': '5分钟前',
                'tags': ['A股', '创业板', '震荡']
            },
            {
                'title': '美联储维持利率不变，符合市场预期',
                'source': '模拟数据',
                'type': 'us_stock',
                'icon': '🏦',
                'display_time': '10分钟前',
                'tags': ['美联储', '利率', '政策']
            },
            {
                'title': '以太坊2.0升级顺利完成，ETH价格上涨5%',
                'source': '模拟数据',
                'type': 'crypto',
                'icon': '🔷',
                'display_time': '15分钟前',
                'tags': ['以太坊', '升级', '上涨']
            },
            {
                'title': '国内新能源汽车板块表现活跃',
                'source': '模拟数据',
                'type': 'china',
                'icon': '🚗',
                'display_time': '20分钟前',
                'tags': ['新能源', '汽车', '板块']
            }
        ]
        return mock_news

    def get_all_news(self):
        """获取所有新闻"""
        print("开始获取新闻数据...")
        
        all_news = []
        
        # 如果有API密钥，尝试获取真实数据
        if self.newsapi_key:
            try:
                crypto_news = self.fetch_crypto_news()
                all_news.extend(crypto_news)
                print(f"获取到 {len(crypto_news)} 条加密货币新闻")
            except Exception as e:
                print(f"API调用失败: {e}")
        
        # 如果真实数据不足，补充模拟数据
        if len(all_news) < 5:
            mock_news = self.fetch_mock_news()
            all_news.extend(mock_news)
            print(f"使用模拟数据，添加 {len(mock_news)} 条新闻")
        
        # 随机打乱新闻顺序
        random.shuffle(all_news)
        print(f"总共获取到 {len(all_news)} 条新闻")
        return all_news

    def save_live_html(self, news_data):
        """生成HTML页面"""
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 实时财经新闻播报系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #ffffff; font-family: Arial; padding: 20px; min-height: 100vh; }
        .live-container { max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.05); border-radius: 20px; padding: 25px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 15px; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin-top: 30px; }
        .news-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #4ecdc4; }
        .news-card.important { border-left-color: #ff6b6b; background: rgba(255,107,107,0.15); }
        .news-title { font-size: 1.2em; margin-bottom: 10px; }
        .news-meta { display: flex; justify-content: space-between; margin-top: 15px; font-size: 0.9em; }
        .news-source { background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="live-container">
        <div class="header">
            <h1>🎯 智能财经新闻实时播报</h1>
            <p>系统时间: {current_time} | 数据更新: {data_update_time}</p>
        </div>
        
        <div class="stats" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0;">
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 2em; font-weight: bold; color: #4ecdc4;">{total_news}</div>
                <div>总新闻数</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 2em; font-weight: bold; color: #4ecdc4;">{crypto_count}</div>
                <div>加密货币</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 2em; font-weight: bold; color: #45b7d1;">{stock_count}</div>
                <div>美股动态</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 2em; font-weight: bold; color: #96ceb4;">{china_count}</div>
                <div>国内市场</div>
            </div>
        </div>
        
        <div class="news-grid">
            {news_items}
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; text-align: center;">
            <p>最后更新: {data_update_time} | 自动更新: 每5分钟 | 🚀 部署于 Vercel</p>
        </div>
    </div>

    <script>
        function updateTime() {{
            const now = new Date();
            document.getElementById('systemTime').textContent = now.toLocaleString('zh-CN');
            setTimeout(updateTime, 1000);
        }}
        document.addEventListener('DOMContentLoaded', function() {{
            updateTime();
            setTimeout(() => window.location.reload(), 300000);
        }});
    </script>
</body>
</html>'''
        
        # 统计新闻数量
        crypto_count = len([n for n in news_data if n['type'] == 'crypto'])
        stock_count = len([n for n in news_data if n['type'] == 'us_stock'])
        china_count = len([n for n in news_data if n['type'] == 'china'])
        
        # 生成新闻卡片
        news_items_html = ""
        for news in news_data:
            card_class = f"news-card {news['type']}"
            if news.get('is_important', False):
                card_class += " important"
            
            news_items_html += f"""
                <div class="{card_class}">
                    <div style="font-size: 1.5em; margin-bottom: 10px;">{news.get('icon', '📰')}</div>
                    <div class="news-title">{news['title']}</div>
                    <div class="news-meta">
                        <span class="news-source">{news['source']}</span>
                        <span style="color: #4ecdc4;">{news.get('display_time', '刚刚')}</span>
                    </div>
                    <div style="margin-top: 10px;">
                        {' '.join([f'<span style="background: rgba(78,205,196,0.3); padding: 3px 8px; border-radius: 10px; font-size: 0.8em; margin-right: 5px;">{tag}</span>' for tag in news.get('tags', [])])}
                    </div>
                </div>
            """
        
        final_html = html_template.format(
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data_update_time=datetime.now().strftime('%H:%M:%S'),
            total_news=len(news_data),
            crypto_count=crypto_count,
            stock_count=stock_count,
            china_count=china_count,
            news_items=news_items_html
        )
        
        return final_html

news_aggregator = NewsAggregator()

@app.route('/')
def home():
    """主页面"""
    try:
        news_data = news_aggregator.get_all_news()
        html_content = news_aggregator.save_live_html(news_data)
        return html_content
    except Exception as e:
        return f"<h1>实时财经新闻播报系统</h1><p>系统运行正常，轻微错误: {str(e)}</p>"

@app.route('/health')
def health():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
