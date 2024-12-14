from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 故事场景列表
scenes = ["森林", "城市", "海边", "山顶", "沙漠"]
characters = ["小男孩", "老爷爷", "小猫", "机器人", "仙女"]
actions = ["冒险", "寻宝", "帮助他人", "解决谜题", "交朋友"]

@app.get("/", response_class=HTMLResponse)
def generate_story():
    # 随机选择故事元素
    scene = random.choice(scenes)
    character = random.choice(characters)
    action = random.choice(actions)
    
    # 生成随机故事
    story = f"""
    <html>
        <head>
            <title>随机故事生成器</title>
            <style>
                body {{
                    font-family: "Microsoft YaHei", Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .story {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    font-size: 2em;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }}
                p {{
                    line-height: 1.8;
                    font-size: 1.1em;
                    margin: 15px 0;
                    text-indent: 2em;
                }}
                .story-container {{
                    animation: fadeIn 1s ease-in;
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
            </style>
        </head>
        <body>
            <div class="story-container">
                <div class="story">
                    <h1>✨ 今日故事 ✨</h1>
                    <p>在一个美丽的{scene}里，住着一个{character}。阳光温柔地洒在地面上，微风轻轻吹过。</p>
                    <p>有一天，{character}决定去{action}。这个决定让生活变得与往常不同。</p>
                    <p>这是一段奇妙的旅程，充满了欢笑与惊喜。每一步都是新的发现，每一刻都值得珍藏...</p>
                </div>
            </div>
        </body>
    </html>
    """
    return story