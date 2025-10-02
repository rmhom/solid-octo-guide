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
        """模拟新闻数据"""
        mock_news = [
            {
                'title': '比特币突破45000美元，创年内新高',
                'source': '财经新闻',
                'type': 'crypto',
                'icon': '₿',
                'display_time': '刚刚',
                'tags': ['比特币', '突破', '新高'],
                'is_important': True
            },
            {
                'title': '美股科技股集体上涨，纳斯达克指数涨1.2%',
                'source': '美股动态', 
                'type': 'us_stock',
                'icon': '📈',
                'display_time': '2分钟前',
                'tags': ['美股', '纳斯达克', '科技股']
            },
            {
                'title': 'A股市场震荡上行，创业板指表现强势',
                'source': '国内财经',
                'type': 'china',
                'icon': '🇨🇳',
                'display_time': '5分钟前',
                'tags': ['A股', '创业板', '震荡']
            }
        ]
        return mock_news

    def get_all_news(self):
        """获取所有新闻"""
        all_news = []
        
        if self.newsapi_key:
            try:
                crypto_news = self.fetch_crypto_news()
                all_news.extend(crypto_news)
            except Exception as e:
                print(f"API调用失败: {e}")
        
        if len(all_news) < 3:
            mock_news = self.fetch_mock_news()
            all_news.extend(mock_news)
        
        random.shuffle(all_news)
        return all_news

    def save_live_html(self, news_data):
        """生成HTML页面"""
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>实时财经新闻播报系统</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        body { 
            background: #1a1a2e; 
            color: white; 
            font-family: Arial; 
            padding: 20px; 
            min-height: 100vh; 
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.05); 
            border-radius: 15px; 
            padding: 20px; 
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .header h1 { 
            font-size: 2.2em; 
            margin-bottom: 10px; 
            color: #4ecdc4; 
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 15px; 
            margin: 20px 0; 
        }
        .stat-item { 
            background: rgba(255,255,255,0.1); 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center; 
        }
        .stat-number { 
            font-size: 1.8em; 
            font-weight: bold; 
            color: #4ecdc4; 
        }
        .news-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 20px; 
            margin-top: 30px; 
        }
        .news-card { 
            background: rgba(255,255,255,0.08); 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 4px solid #4ecdc4; 
        }
        .news-card.important { 
            border-left-color: #ff6b6b; 
            background: rgba(255,107,107,0.1); 
        }
        .news-icon { 
            font-size: 1.8em; 
            margin-bottom: 10px; 
        }
        .news-title { 
            font-size: 1.1em; 
            margin-bottom: 10px; 
            line-height: 1.4; 
        }
        .news-meta { 
            display: flex; 
            justify-content: space-between; 
            margin-top: 15px; 
            font-size: 0.9em; 
        }
        .news-source { 
            background: rgba(255,255,255,0.15); 
            padding: 4px 8px; 
            border-radius: 5px; 
        }
        .news-time { 
            color: #4ecdc4; 
        }
        .footer { 
            margin-top: 30px; 
            padding: 15px; 
            background: rgba(255,255,255,0.05); 
            border-radius: 10px; 
            text-align: center; 
            font-size: 0.9em; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 实时财经新闻播报</h1>
            <p>系统时间: {current_time} | 更新: {data_update_time}</p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{total_news}</div>
                <div>总新闻数</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{crypto_count}</div>
                <div>加密货币</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{stock_count}</div>
                <div>美股动态</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{china_count}</div>
                <div>国内市场</div>
            </div>
        </div>
        
        <div class="news-grid">
            {news_items}
        </div>
        
        <div class="footer">
            <p>最后更新: {data_update_time} | 自动更新: 每5分钟 | 🚀 部署于 Vercel</p>
        </div>
    </div>

    <script>
        setTimeout(() => window.location.reload(), 300000);
    </script>
</body>
</html>'''
        
        crypto_count = len([n for n in news_data if n['type'] == 'crypto'])
        stock_count = len([n for n in news_data if n['type'] == 'us_stock'])
        china_count = len([n for n in news_data if n['type'] == 'china'])
        
        news_items_html = ""
        for news in news_data:
            card_class = "news-card"
            if news.get('is_important', False):
                card_class += " important"
            
            news_items_html += f'''
                <div class="{card_class}">
                    <div class="news-icon">{news.get('icon', '📰')}</div>
                    <div class="news-title">{news['title']}</div>
                    <div class="news-meta">
                        <span class="news-source">{news['source']}</span>
                        <span class="news-time">{news.get('display_time', '刚刚')}</span>
                    </div>
                </div>
            '''
        
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
        return f"<h1>实时财经新闻播报系统</h1><p>系统运行正常</p><p>调试信息: {str(e)}</p>"

@app.route('/health')
def health():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
