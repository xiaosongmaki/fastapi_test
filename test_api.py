import requests
import webbrowser
from urllib.parse import urljoin

def test_story_generator():
    # 设置基础 URL
    base_url = "https://fastapitest-production-97cd.up.railway.app"
    
    try:
        # 发送 GET 请求
        response = requests.get(base_url)
        
        # 检查状态码
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API 访问成功！")
            
            # 将响应内容保存为 HTML 文件
            with open("story.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            # 在浏览器中打开生成的故事
            webbrowser.open("story.html")
            
            print("故事已在浏览器中打开，请查看。")
        else:
            print("❌ API 访问失败！")
            
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    print("开始测试故事生成器 API...")
    test_story_generator() 