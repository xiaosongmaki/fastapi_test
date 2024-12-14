from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import logging
from datetime import datetime
from typing import List, Optional
import json
import os
from fastapi.responses import FileResponse
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="智能故事生成器",
    description="一个专业的故事生成API，支持自定义故事元素和模板",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建templates和static目录
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 数据模型
class StoryElement(BaseModel):
    category: str
    content: str

class StoryTemplate(BaseModel):
    template: str
    elements: dict

# 存储故事元素的数据结构
story_elements = {
    "scenes": [
        "在一片神秘的森林里", "在繁华的未来城市中", "在宁静的海边", 
        "在雪峰耸立的山顶", "在广袤的沙漠中", "在童话般的城堡里"
    ],
    "characters": [
        "勇敢的小男孩", "智慧的老爷爷", "可爱的小猫", "先进的机器人",
        "美丽的仙女", "神秘的旅行者", "调皮的精灵"
    ],
    "actions": [
        "展开了一场惊险的冒险", "开始寻找传说中的宝藏", 
        "遇到了需要帮助的朋友", "解开了一个古老的谜题",
        "结识了新的伙伴", "学会了重要的人生课程"
    ],
    "emotions": [
        "充满好奇", "满怀希望", "略带紧张", 
        "无比兴奋", "深感温暖", "异常勇敢"
    ]
}

# 故事模板
story_templates = [
    {
        "template": """
        {scene}，生活着一个{character}。
        一天，当{emotion}的气氛笼罩着这里时，主人公{action}。
        这成为了一个难忘的经历，让每个听到这个故事的人都感到温暖和感动。
        """,
        "elements": ["scene", "character", "emotion", "action"]
    },
    {
        "template": """
        这是一个关于{character}的故事。
        在{scene}的背景下，我们的主角{emotion}地{action}。
        这不仅仅是一个普通的故事，更是一个关于勇气和智慧的寓言。
        """,
        "elements": ["character", "scene", "emotion", "action"]
    }
]

# 缓存最近生成的故事
story_cache = []
MAX_CACHE_SIZE = 10

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """返回主页面"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "story_elements": story_elements}
    )

@app.get("/api/story", response_class=JSONResponse)
async def generate_story():
    """生成一个随机故事"""
    try:
        template = random.choice(story_templates)
        story_data = {
            "scene": random.choice(story_elements["scenes"]),
            "character": random.choice(story_elements["characters"]),
            "action": random.choice(story_elements["actions"]),
            "emotion": random.choice(story_elements["emotions"])
        }
        
        story = template["template"].format(**story_data)
        
        # 添加到缓存
        if len(story_cache) >= MAX_CACHE_SIZE:
            story_cache.pop(0)
        story_cache.append({
            "story": story,
            "generated_at": datetime.now().isoformat(),
            "template_used": template["template"]
        })
        
        return {
            "status": "success",
            "data": {
                "story": story,
                "elements_used": story_data
            }
        }
    except Exception as e:
        logger.error(f"生成故事时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="生成故事时发生错误")

@app.post("/api/elements/{category}")
async def add_story_element(category: str, element: StoryElement):
    """添加新的故事元素"""
    if category not in story_elements:
        raise HTTPException(status_code=400, detail="无效的故事元素类别")
    
    story_elements[category].append(element.content)
    return {"status": "success", "message": f"成功添加新的{category}"}

@app.get("/api/elements", response_class=JSONResponse)
async def get_story_elements():
    """获取所有故事元素"""
    return story_elements

@app.get("/api/templates", response_class=JSONResponse)
async def get_story_templates():
    """获取所有故事模板"""
    return story_templates

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "cache_size": len(story_cache)
    }

@app.get("/api/stats")
async def get_stats():
    """获取系统统计信息"""
    return {
        "total_scenes": len(story_elements["scenes"]),
        "total_characters": len(story_elements["characters"]),
        "total_actions": len(story_elements["actions"]),
        "total_emotions": len(story_elements["emotions"]),
        "total_templates": len(story_templates),
        "stories_in_cache": len(story_cache)
    }

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(exc.detail),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未处理的异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "服务器内部错误",
            "timestamp": datetime.now().isoformat()
        }
    )