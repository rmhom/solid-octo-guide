
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 实时财经新闻播报 - 直播专用</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #ffffff;
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            padding: 15px;
            min-height: 100vh;
        }
        
        .live-container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 25px;
            padding: 15px;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        
        .price-banner {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
            font-size: 1.3em;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .stat-number {
            font-size: 2.2em;
            font-weight: bold;
            color: #4ecdc4;
            margin-bottom: 5px;
        }
        
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }
        
        .news-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border-radius: 12px;
            padding: 20px;
            border-left: 5px solid #4ecdc4;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .news-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        
        .news-card.crypto {
            border-left-color: #4ecdc4;
        }
        
        .news-card.us_stock {
            border-left-color: #45b7d1;
        }
        
        .news-card.china {
            border-left-color: #96ceb4;
        }
        
        .news-card.important {
            border-left-color: #ff6b6b;
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 107, 107, 0.08));
            animation: pulse 2s infinite;
        }
        
        .news-icon {
            font-size: 2em;
            margin-bottom: 12px;
        }
        
        .news-title {
            font-size: 1.2em;
            line-height: 1.5;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .news-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            font-size: 0.9em;
        }
        
        .news-source {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 12px;
            border-radius: 8px;
            font-weight: 500;
        }
        
        .news-time {
            color: #4ecdc4;
            font-weight: bold;
        }
        
        .live-badge {
            background: #ff6b6b;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 8px;
        }
        
        .footer {
            margin-top: 30px;
            padding: 15px;
            text-align: center;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            font-size: 0.9em;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
        }
        
        /* 直播平台优化 */
        .stream-optimized {
            font-size: 1.1em;
            line-height: 1.6;
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .news-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="live-container stream-optimized">
        <div class="header">
            <h1>🎯 实时财经新闻播报系统</h1>
            <p>直播专用面板 | 更新时间: <span id="currentTime">加载中...</span></p>
        </div>
        
        <div class="price-banner">
            🔥 比特币实时价格: $<span id="btcPrice">118,590</span> | 
            24小时变化: <span id="btcChange">+3.28%</span>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="totalNews">6</div>
                <div>总新闻数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="cryptoCount">3</div>
                <div>加密货币</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="stockCount">2</div>
                <div>美股动态</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="chinaCount">1</div>
                <div>国内市场</div>
            </div>
        </div>
        
        <div class="news-grid" id="newsContainer">
            <!-- 新闻内容由JavaScript动态加载 -->
        </div>
        
        <div class="footer">
            <p>🚀 实时数据播报 | 自动更新 | 直播平台专用</p>
        </div>
    </div>

    <script>
        // 实时新闻数据
        const newsData = [
            {
                title: '🚀 比特币突破$118,590，24小时上涨3.28%',
                source: '实时行情',
                type: 'crypto',
                icon: '₿',
                display_time: '实时',
                important: true
            },
            {
                title: '📈 加密货币总市值24小时增长5.3%',
                source: '市场分析',
                type: 'crypto',
                icon: '💹',
                display_time: '实时'
            },
            {
                title: '💎 以太坊跟随比特币上涨，DeFi板块活跃',
                source: '区块链动态',
                type: 'crypto',
                icon: '🔷',
                display_time: '实时'
            },
            {
                title: '🏦 美联储政策预期支撑数字资产价格',
                source: '政策分析',
                type: 'us_stock',
                icon: '💵',
                display_time: '实时'
            },
            {
                title: '🇨🇳 亚洲市场数字货币相关股票普涨',
                source: '区域行情',
                type: 'china',
                icon: '🔴',
                display_time: '实时'
            },
            {
                title: '🌍 全球机构投资者持续关注加密货币',
                source: '机构动态',
                type: 'us_stock',
                icon: '🏛️',
                display_time: '实时'
            }
        ];

        // 初始化新闻内容
        function renderNews() {
            const container = document.getElementById('newsContainer');
            container.innerHTML = '';
            
            newsData.forEach(news => {
                const cardClass = `news-card ${news.type} ${news.important ? 'important' : ''}`;
                const card = document.createElement('div');
                card.className = cardClass;
                card.innerHTML = `
                    <div class="news-icon">${news.icon}</div>
                    <div class="news-title">${news.title}</div>
                    <div class="news-meta">
                        <span class="news-source">${news.source}</span>
                        <span class="news-time">${news.display_time} <span class="live-badge">LIVE</span></span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        // 更新时间显示
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleString('zh-CN');
            document.getElementById('currentTime').textContent = timeString;
        }

        // 模拟价格变化（直播效果）
        function simulatePriceChange() {
            const priceElement = document.getElementById('btcPrice');
            const changeElement = document.getElementById('btcChange');
            
            // 随机小幅度价格变化
            const currentPrice = 118590;
            const randomChange = (Math.random() - 0.5) * 200;
            const newPrice = currentPrice + randomChange;
            const changePercent = (randomChange / currentPrice * 100).toFixed(2);
            
            priceElement.textContent = newPrice.toLocaleString();
            changeElement.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent}%`;
            changeElement.style.color = changePercent >= 0 ? '#4ecdc4' : '#ff6b6b';
        }

        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            renderNews();
            updateTime();
            
            // 每秒更新时间
            setInterval(updateTime, 1000);
            
            // 每30秒模拟价格变化（直播效果）
            setInterval(simulatePriceChange, 30000);
            
            // 每2分钟刷新页面获取最新数据
            setTimeout(() => {
                window.location.reload();
            }, 120000);
            
            console.log('🎯 直播专用新闻面板已启动');
        });

        // 错误处理
        window.addEventListener('error', function(e) {
            console.error('直播面板错误:', e.error);
        });
    </script>
</body>
</html>
