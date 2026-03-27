import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/health':
            self._send_json(200, {'status': 'ok', 'message': '电视剧营销投流 AI 工作台运行正常'})
        else:
            self._send_json(404, {'error': 'Not found'})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json(400, {'error': 'Invalid JSON'})
            return

        if self.path == '/api/generate-strategy':
            prompt = self._build_strategy_prompt(data)
        elif self.path == '/api/generate-copywriting':
            prompt = self._build_copywriting_prompt(data)
        else:
            self._send_json(404, {'error': 'Not found'})
            return

        # 调用阿里云 API 并流式返回
        self._stream_response(prompt)

    def _build_strategy_prompt(self, data):
        return f"""请为以下电视剧制定详细的投流策略方案：

【剧集信息】
- 剧名：{data.get('dramaName', '')}
- 类型：{data.get('dramaType', '')}
- 主演阵容：{data.get('cast', '')}
- 核心看点：{', '.join(data.get('highlights', []))}
- 目标受众：{data.get('targetAudience', '')}

【投放信息】
- 预算范围：{data.get('budget', '')}
- 投放周期：{data.get('duration', '')}
- 投放平台：{', '.join(data.get('platforms', []))}

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

请给出专业、详细、可落地的建议。"""

    def _build_copywriting_prompt(self, data):
        return f"""请为以下电视剧素材生成投放文案：

【剧集信息】
- 剧名：{data.get('dramaName', '')}

【素材内容/看点】
{data.get('content', '')}

【文案风格】
{', '.join(data.get('styles', []))}

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
4. 避免违禁词和敏感内容"""

    def _stream_response(self, prompt):
        import os
        import requests as req_lib

        api_key = os.environ.get('DASHSCOPE_API_KEY', '')

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-DashScope-SSE': 'enable'
        }

        payload = {
            "model": "qwen-max",
            "input": {
                "messages": [
                    {"role": "system", "content": "你是专业的电视剧营销投流策略专家，擅长制定精准的投流策略、生成吸引人的投放文案。你需要基于剧集特点，给出可落地的营销建议。请使用 Markdown 格式输出，让内容结构清晰。"},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "result_format": "message",
                "incremental_output": True
            }
        }

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            response = req_lib.post(
                'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue
                line_str = line.decode('utf-8')
                if line_str.startswith('data:'):
                    data_str = line_str[5:].strip()
                    if data_str == '[DONE]':
                        break
                    try:
                        result = json.loads(data_str)
                        content = result.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
                        if content:
                            self.wfile.write(content.encode('utf-8'))
                            self.wfile.flush()
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
                else:
                    try:
                        result = json.loads(line_str)
                        content = result.get('output', {}).get('text', '')
                        if content:
                            self.wfile.write(content.encode('utf-8'))
                            self.wfile.flush()
                    except (json.JSONDecodeError, KeyError):
                        continue
        except Exception as e:
            self.wfile.write(f"\n\n❌ 生成出错：{str(e)}".encode('utf-8'))
            self.wfile.flush()

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
