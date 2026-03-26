from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)
CORS(app)

# 阿里云百炼 API 配置
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'

def generate_stream(prompt):
    """调用阿里云百炼 API 生成流式响应"""
    headers = {
        'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "qwen-max",
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": "你是专业的电视剧营销投流策略专家，擅长制定精准的投流策略、生成吸引人的投放文案。你需要基于剧集特点，给出可落地的营销建议。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "text"
        }
    }
    
    try:
        response = requests.post(
            DASHSCOPE_API_URL,
            headers=headers,
            json=data,
            stream=True,
            timeout=60
        )
        
        for line in response.iter_lines():
            if line:
                yield line.decode('utf-8') + '\n'
                
    except Exception as e:
        yield f"Error: {str(e)}"

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'message': '电视剧营销投流 AI 工作台运行正常'}

@app.route('/api/generate-strategy', methods=['POST'])
def generate_strategy():
    """生成投流策略"""
    data = request.json
    
    drama_name = data.get('dramaName', '')
    drama_type = data.get('dramaType', '')
    cast = data.get('cast', '')
    highlights = data.get('highlights', [])
    target_audience = data.get('targetAudience', '')
    budget = data.get('budget', '')
    duration = data.get('duration', '')
    platforms = data.get('platforms', [])
    
    prompt = f"""
请为以下电视剧制定详细的投流策略方案：

【剧集信息】
- 剧名：{drama_name}
- 类型：{drama_type}
- 主演阵容：{cast}
- 核心看点：{', '.join(highlights)}
- 目标受众：{target_audience}

【投放信息】
- 预算范围：{budget}
- 投放周期：{duration}
- 投放平台：{', '.join(platforms)}

请输出以下内容：

## 一、目标受众画像分析
- 核心人群特征（年龄、性别、地域、兴趣）
- 观剧动机分析
- 消费行为特征

## 二、四大平台内容策略
针对每个平台，请给出：
### 抖音
- 内容形式建议
- 创意方向
- 话题标签策略
- 投放时段建议

### 小红书
- 内容形式建议
- 种草方向
- 关键词策略
- 达人合作建议

### 视频号
- 内容形式建议
- 互动策略
- 朋友圈传播方案

### 微博
- 话题策划
- 明星互动方案
- 粉丝运营策略

## 三、预算分配建议
- 各平台预算分配比例及理由
- 预热期/热播期/收官期的预算分配

## 四、投放节奏规划
- 预热期（开播前1周）：目标、策略、关键动作
- 热播期（播出期间）：目标、策略、关键动作
- 收官期（最后1周）：目标、策略、关键动作

## 五、KPI 目标设定
- 曝光目标
- 互动目标
- 转化目标（拉新到站内观看）
- ROI 预估

## 六、风险预警与应对
- 可能遇到的问题
- 应对预案

请给出专业、详细、可落地的建议。
"""
    
    def generate():
        for chunk in generate_stream(prompt):
            yield chunk
    
    return Response(stream_with_context(generate()), mimetype='text/plain')

@app.route('/api/generate-copywriting', methods=['POST'])
def generate_copywriting():
    """生成投放文案"""
    data = request.json
    
    drama_name = data.get('dramaName', '')
    content = data.get('content', '')
    styles = data.get('styles', [])
    
    prompt = f"""
请为以下电视剧素材生成投放文案：

【剧集信息】
- 剧名：{drama_name}

【素材内容/看点】
{content}

【文案风格】
{', '.join(styles)}

请为抖音、小红书、视频号、微博四个平台分别生成文案，每个平台的文案要符合平台调性：

## 抖音文案
- 时长建议：15-30秒
- 文案风格：快节奏、强吸引力、悬念感
- 必须包含：
  - 视频标题（15字以内）
  - 视频文案（带情感节奏）
  - 话题标签（3-5个）
  - BGM 建议

## 小红书文案
- 文案风格：种草感、情感共鸣、细节描写
- 必须包含：
  - 标题（带emoji，吸睛）
  - 正文（情感化描述，分点说明）
  - 关键词（5-8个）
  - 封面建议

## 视频号文案
- 文案风格：简洁有力、朋友圈传播感
- 必须包含：
  - 视频标题
  - 文案描述
  - 朋友圈分享文案

## 微博文案
- 文案风格：话题感、互动性、热搜体质
- 必须包含：
  - 微博正文（带话题）
  - 话题标签（2-3个）
  - 互动问题

请确保文案：
1. 符合各平台用户习惯
2. 突出剧集看点
3. 有强烈的点击欲望
4. 避免违禁词和敏感内容
"""
    
    def generate():
        for chunk in generate_stream(prompt):
            yield chunk
    
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
