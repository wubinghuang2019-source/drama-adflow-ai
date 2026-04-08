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
            self._stream_response(prompt)
        elif self.path == '/api/generate-copywriting':
            prompt = self._build_copywriting_prompt(data)
            self._stream_response(prompt)
        elif self.path == '/api/search-accounts':
            prompt = self._build_account_search_prompt(data)
            self._stream_response(prompt)
        elif self.path == '/api/generate-analysis':
            prompt = self._build_analysis_prompt(data)
            self._stream_response(prompt)
        else:
            self._send_json(404, {'error': 'Not found'})

    def _build_strategy_prompt(self, data):
        platforms = data.get('platforms', ['抖音', '小红书', '视频号', '微博'])
        
        prompt = f"""你是资深电视剧营销投流专家，请基于以下信息制定**可落地、可执行**的投流策略方案。

【剧集基本信息】
- 剧名：{data.get('dramaName', '')}
- 类型：{data.get('dramaType', '')}
- 主演阵容：{data.get('cast', '')}
- 核心看点：{', '.join(data.get('highlights', []))}
- 目标受众：{data.get('targetAudience', '')}

【投放资源配置】
- 预算范围：{data.get('budget', '')}
- 投放周期：{data.get('duration', '')}
- 投放平台：{', '.join(platforms)}

请输出详细的投流策略方案，每一条建议都要**具体、可操作、可量化**。

---

## 一、目标受众精准画像

基于剧集类型和目标受众，深度分析：

### 核心人群特征
- **年龄层**：按优先级排序（如：25-35岁女性 > 35-45岁男性）
- **性别比例**：基于历史数据预估（如：女性65%，男性35%）
- **地域分布**：重点投放城市（Top 10，按优先级）
- **兴趣标签**：与剧集匹配的兴趣关键词（如：追剧、情感剧、古装）

### 观剧动机深度拆解
1. **情感需求**：观众在剧中寻找什么情感（如：治愈、共鸣、刺激）
2. **社交需求**：哪些内容容易被讨论和分享（如：高光时刻、争议话题）
3. **知识需求**：是否需要提供背景知识（如：历史、文化）

### 消费行为特征
- **观看习惯**：碎片化/完整观看、追更速度
- **付费意愿**：付费点播/会员/免费观看
- **分享行为**：朋友圈/微博/小红书分享偏好

---

## 二、分平台内容策略

针对选定平台，制定差异化内容方案："""

        # 根据选定的平台添加具体策略
        if '抖音' in platforms:
            prompt += """

### 抖音策略 🎵

**核心打法：黄金3秒法则 + 热点引爆**

#### 内容形式
1. **高光剪辑（40%）**：15-30秒，开头3秒必须有冲突/悬念/反差
2. **剧情预告（30%）**：剧集预告片+情感文案，吸引追更
3. **幕后花絮（20%）**：片场日常、演员互动，增加亲切感
4. **话题挑战（10%）**：发起#XX剧追更挑战，鼓励UGC

#### 创意方向
- **开头爆款公式**："没想到..." + 高光场景 + "太虐/太甜了"
- **情感节奏**：前半段铺垫 → 中间高潮 → 结尾引导互动
- **BGM选择**：
  * 悲伤场景：纯音乐或低沉人声
  * 高能场景：快节奏鼓点或燃曲
  * 甜蜜场景：轻快旋律或热门BGM

#### 话题标签策略
- **必带标签**：#剧名 #追剧 #每日更新
- **情感标签**：根据场景选择 #催泪 #甜宠 #烧脑
- **蹭热点**：结合当日热搜 #今日追剧推荐

#### 投放时段与出价
- **黄金时段**：20:00-22:00（出价提高30%）
- **平峰时段**：12:00-14:00、15:00-17:00
- **低谷时段**：23:00-次日8:00（降低出价或暂停）

#### 数据优化
- **点击率<1%**：优化开头3秒，增加悬念
- **完播率<30%**：剪辑节奏加快，缩短时长
- **互动率<2%**：增加引导评论的问题
"""

        if '小红书' in platforms:
            prompt += """

### 小红书策略 📕

**核心打法：情感共鸣 + 深度种草**

#### 内容形式
1. **剧情分析（50%）**：长图+文字，深度解析角色和剧情
2. **观剧感受（30%）**：个人感受+推荐理由，带情绪价值
3. **明星互动（15%）**：主演相关内容，吸引粉丝
4. **追剧攻略（5%）**：观看顺序、重点集数提示

#### 种草方向
- **情感锚点**：找到观众最在意的情感痛点（如：爱情、亲情、成长）
- **对比种草**：与同类剧集对比，突出本剧优势
- **场景代入**：描述具体场景，让观众产生画面感

#### 关键词策略
- **核心词**：剧名、主演、类型（如：#繁花 #胡歌 #年代剧）
- **长尾词**：具体场景、角色名（如：#宝总汪小姐 #繁花黄河路）
- **情绪词**：催泪、甜宠、治愈（根据剧集特点选择）

#### 达人合作建议
- **KOC种草**：100-500粉的小红书用户，真实感强，性价比高
- **中腰部达人**：1万-10万粉，垂直领域（如：情感、追剧、影评）
- **头部达人**：10万+粉，建议合作1-2位提升声量
- **合作内容**：观剧笔记+情感故事+推荐理由

#### 发布节奏
- **预热期**：每天1篇，营造期待感
- **热播期**：每天2-3篇，保持热度
- **收官期**：每天1篇，引导收藏和回味
"""

        if '视频号' in platforms:
            prompt += """

### 视频号策略 📱

**核心打法：朋友圈裂变 + 沉浸式体验**

#### 内容形式
1. **高光片段（60%）**：10-20秒，选择最戳心的场景
2. **预告片剪辑（30%）**：30秒内，节奏快、信息密度高
3. **剧情回顾（10%）**：关键场景合集，适合收官期

#### 互动策略
- **引导点赞**："觉得这个场景戳心的，双击❤️支持一下"
- **引导评论**："你们觉得XX会怎么做？评论区告诉我"
- **引导转发**："转发给懂这部剧的人"

#### 朋友圈传播方案
- **文案模板**：
  * "一句话金句" + 观剧感受 + 推荐指数
  * 示例："《XX》第3集这一幕太戳心了！看得我哭了一晚上😭"
- **转发诱因**：
  * 情感共鸣："你们看到这一幕了吗？"
  * 社交货币："这部剧太上头了，必须安利给你们"
  * 讨论话题："你们觉得XX和XX最后会在一起吗？"

#### 发布时段
- **最佳时间**：中午12点（午休）、晚上20-21点（晚餐后）
- **避开时间**：9-11点（工作）、22点后（睡觉）
"""

        if '微博' in platforms:
            prompt += """

### 微博策略 🐦

**核心打法：话题运营 + 粉丝联动**

#### 话题策划
1. **固定话题**：#剧名每日更新#（每天一条剧情）
2. **热点话题**：根据剧情节奏制造话题（如#XX角色名场面#）
3. **情感话题**：引发讨论（如#XX剧最戳心的一幕#）
4. **对比话题**：与同类剧集对比（如#年度最XX剧集#）

#### 明星互动方案
- **主演微博**：发布追剧感受、回应粉丝评论
- **官微互动**：@主演和剧组，形成传播矩阵
- **直播预热**：开播前主演直播互动，制造期待
- **花絮互动**：片场花絮+明星互动，增加亲切感

#### 粉丝运营策略
- **超话运营**：
  * 每日发布剧情讨论帖
  * 回复粉丝评论，保持活跃
  * 引导粉丝生产UGC（剪辑、同人、观后感）
- **粉丝群维护**：
  * 建立官方粉丝群，及时答疑解惑
  * 提供独家花絮、剧照，增强归属感
  * 发起粉丝活动（如：观剧打卡、角色投票）

#### 发布技巧
- **蹭热点**：在热搜话题下发布相关内容
- @策略：@官微、@主演、@相关博主
- **发布时间**：
  * 工作日：19-21点（下班高峰）
  * 周末：全天可发，重点12-14点、20-22点
"""

        prompt += f"""

---

## 三、预算精细化分配

基于总预算 `{data.get('budget', '')}`，建议分配如下：

### 各平台预算分配
| 平台 | 比例 | 预算金额 | 分配理由 |
|------|------|----------|----------|
| 抖音 | XX% | ¥XX万 | 流量最大，适合曝光 |
| 小红书 | XX% | ¥XX万 | 种草转化率高 |
| 视频号 | XX% | ¥XX万 | 社交裂变效果好 |
| 微博 | XX% | ¥XX万 | 话题运营，提升声量 |

### 阶段预算分配（总周期：{data.get('duration', '')}）
| 阶段 | 时间范围 | 预算占比 | 预算金额 | 核心目标 |
|------|----------|----------|----------|----------|
| 预热期 | 开播前1周 | 20% | ¥XX万 | 积累预约，制造期待 |
| 热播期 | 播出前70% | 60% | ¥XX万 | 拉新拉活，提升热度 |
| 收官期 | 播出后30% | 20% | ¥XX万 | 引导回味，沉淀口碑 |

---

## 四、投放节奏精准规划

### 预热期（开播前1周）
**目标**：积累1万+预约，制造开播话题热度
- **抖音**：每天3-5条，内容为预告片+花絮+演员互动
- **小红书**：每天2-3篇，预告解析+角色介绍+幕后故事
- **视频号**：每天2条，预告剪辑+情感文案
- **微博**：每天1条，官宣定档+主演互动+话题预热
- **关键动作**：
  1. 开播前3天，发布终极预告
  2. 主演直播互动，回答粉丝问题
  3. 发起#XX剧开播在即#话题

### 热播期（播出期间）
**目标**：单日新增观看用户5万+，话题阅读量破亿
- **抖音**：每天5-8条，紧跟剧情更新，高光剪辑+情感文案
- **小红书**：每天3-5篇，剧情解析+观剧感受+角色讨论
- **视频号**：每天3-4条，高光片段+互动引导
- **微博**：每天2-3条，话题运营+剧情讨论+热搜冲击
- **关键动作**：
  1. 每天发布当日高光剪辑
  2. 结合剧情制造话题（如#XX角色太戳心#）
  3. 主演发布追剧感受，与粉丝互动

### 收官期（最后1周）
**目标**：沉淀口碑，引导完整观看+收藏推荐
- **抖音**：每天3-4条，名场面合集+情感回顾+推荐引导
- **小红书**：每天2-3篇，观后感+角色总结+安利推荐
- **视频号**：每天2条，高光合集+完整观看引导
- **微博**：每天1-2条，收官话题+口碑总结+感谢观众
- **关键动作**：
  1. 发布名场面合集剪辑
  2. 引导观众完整观看
  3. 感谢观众支持，强化情感连接

---

## 五、KPI 目标设定

### 曝光目标
- **总曝光量**：{int(float(data.get('budget', '50').replace('万', '')) * 200) if '万' in data.get('budget', '50') else '1000'}万+
- **各平台曝光**：抖音60% | 小红书20% | 视频号10% | 微博10%
- **CPM成本**：控制在¥XX以内

### 互动目标
- **互动率**：平均3%+（抖音2% | 小红书5% | 视频号4% | 微博3%）
- **点赞数**：{int(float(data.get('budget', '50').replace('万', '')) * 10) if '万' in data.get('budget', '50') else '50'}万+
- **评论数**：{int(float(data.get('budget', '50').replace('万', '')) * 1) if '万' in data.get('budget', '50') else '5'}万+
- **分享数**：{int(float(data.get('budget', '50').replace('万', '')) * 0.5) if '万' in data.get('budget', '50') else '2.5'}万+

### 转化目标（拉新到站内观看）
- **拉新数**：{int(float(data.get('budget', '50').replace('万', '')) * 5) if '万' in data.get('budget', '50') else '25'}万+
- **转化率**：CTR 5%+，CVR 3%+
- **客单价**：按平台实际付费情况统计

### ROI 预估
- **付费ROI**：1:3+（投入1元，回收3元）
- **免费ROI**：自然流量占比40%+
- **口碑ROI**：豆瓣评分7.5+，好评率85%+

---

## 六、风险预警与应对

### 可能遇到的风险
1. **内容同质化**：与同类剧集内容重复，缺乏差异化
   - **应对**：深挖剧集独特卖点，突出差异化亮点
2. **舆情风险**：剧情/演员引发负面讨论
   - **应对**：提前准备舆情预案，及时发声引导
3. **流量饱和**：投放后期效果衰减
   - **应对**：调整内容策略，增加情感共鸣和用户互动
4. **平台规则变化**：平台算法或政策调整
   - **应对**：密切关注平台动态，及时优化策略

### 应对预案
- **舆情监控**：每日监测舆情，24小时响应负面信息
- **内容调整**：根据数据反馈，实时优化内容和投放策略
- **备用方案**：准备多套备选内容和投放方案

---

【重要提醒】
1. **数据驱动**：所有决策基于实时数据，每3天复盘一次
2. **快速试错**：小范围测试后快速放量，避免大额损失
3. **情感连接**：始终以用户情感为核心，建立品牌好感度
4. **长期运营**：不只关注短期ROI，更要培养品牌和用户忠诚度

请开始生成策略方案，输出要具体、可执行、可量化。"""

        return prompt

    def _build_copywriting_prompt(self, data):
        platforms = data.get('platforms', ['抖音', '小红书', '视频号', '微博'])
        styles = data.get('styles', [])
        
        prompt = f"""你是专业的电视剧营销文案专家，请为以下电视剧素材生成高质量的投放文案。

【剧集信息】
- 剧名：{data.get('dramaName', '')}

【素材内容/看点】
{data.get('content', '')}

【文案风格】
{', '.join(styles) if styles else '根据平台特点自动适配'}

【投放平台】
{', '.join(platforms)}

请针对选定的平台，生成可直接使用的投放文案。每个平台的内容要：

1. **紧扣素材看点**：基于提供的素材内容，提炼1-2个最吸引人的核心亮点
2. **符合平台调性**：严格遵循各平台的用户习惯和内容特点
3. **突出情感共鸣**：用故事化表达，让观众产生代入感
4. **强化行动指令**：引导用户点击、转发、评论等互动行为
"""

        # 为每个平台添加具体要求
        if '抖音' in platforms:
            prompt += """

## 抖音文案 🎵
**黄金3秒原则**：开头必须抓住眼球
- 视频标题：15字以内，有冲突、悬念、反差（如"这一幕我哭了3遍"）
- 视频文案：
  * 第1句：抛出悬念或冲突（"谁能想到..."、"没想到最后..."）
  * 中间：用2-3句话描述高光场景，带情感节奏
  * 结尾：引导互动（"你觉得呢？"、"在评论区告诉我"）
- BGM建议：根据情绪选择（悲伤时用纯音乐，高能时用快节奏）
- 话题标签：3-5个，包括剧名+情感词+热门标签（#剧名 #追剧 #催泪）
- 发布时间：建议晚上8-10点或周末黄金时段
"""

        if '小红书' in platforms:
            prompt += """

## 小红书文案 📕
**种草感+情感共鸣**：
- 标题：15-20字，带2-3个emoji，制造好奇心（"🎬这部剧让我哭到失声！"）
- 正文结构：
  * 开头：用"姐妹们"、"家人们"等称呼拉近距离
  * 中间：分点描述，用emoji分隔（✨看点1、💔看点2）
  * 细节：加入个人观剧感受，如"第X集XX场景太戳心了"
  * 结尾：总结推荐理由+引导收藏
- 关键词：6-8个，覆盖剧名、主演、剧情类型、情感词
- 封面建议：高光画面+大字标题（如"哭到失声"、"虐心预警"）
- 发布时间：建议工作日午休12-14点、晚上20-22点
"""

        if '视频号' in platforms:
            prompt += """

## 视频号文案 📱
**简洁有力+朋友圈传播**：
- 视频标题：12字以内，直击核心看点（如"这部剧，绝了"）
- 文案描述：50字以内，用短句和感叹号（"没想到最后反转这么虐！"）
- 朋友圈分享文案：
  * 形式："一句话+观剧感受+推荐指数"
  * 示例："《XX》第3集这一幕太戳心了！看得我哭了一晚上😭 推荐⭐⭐⭐⭐⭐"
  * 加上：#追剧日常 #宝藏剧集
- 发布时间：建议中午12点、晚上8-9点（朋友圈高峰期）
"""

        if '微博' in platforms:
            prompt += """

## 微博文案 🐦
**话题感+热搜体质**：
- 微博正文：
  * 第1句：抛出话题或金句（"《XX》第X集这一幕太虐了！"）
  * 中间：简述场景+个人感受，2-3句话
  * 结尾：互动问题（"你们看到这一幕了吗？哭了吗？"）
- 话题标签：2-3个，格式 #剧名# + #情感词#（#繁花# #追剧日常#）
- 发布技巧：
  * 发布后@官方账号和主演
  * 在热门话题下发布增加曝光
  * 发布时间：工作日晚上19-21点，周末全天
- 互动：回复评论，保持话题热度
"""

        prompt += """

【质量要求】
1. **真实可落地**：每条文案都是可以实际发布的，避免空泛内容
2. **数据驱动**：参考近期热门剧集的爆款文案套路
3. **情绪价值**：让观众看完就想点开看或分享给朋友
4. **差异化明显**：每个平台的文案风格要鲜明区别

请开始生成，直接输出文案内容，不要解释说明。"""

        return prompt

    def _build_account_search_prompt(self, data):
        keyword = data.get('keyword', '')
        platform = data.get('platform', '不限')
        category = data.get('category', '不限')
        fans = data.get('fans', '不限')

        prompt = f"""你是专业的电视剧营销选号专家，擅长为影视剧投流推荐合适的KOL/达人账号。

【搜索需求】
- 关键词：{keyword}
- 目标平台：{platform if platform else '全部平台（抖音、小红书、视频号、微博）'}
- 垂类领域：{category if category else '不限'}
- 粉丝量级：{fans if fans else '不限'}

请基于你的知识，为该剧推荐 8-12 个适合合作推广的达人/KOL账号。

推荐要求：
1. **精准匹配**：达人的内容方向、粉丝画像必须与电视剧目标受众高度重合
2. **数据真实**：参考公开可查的数据（如粉丝量、互动率），标注"仅供参考"
3. **性价比分析**：根据粉丝量和互动率评估性价比
4. **合作建议**：给出每个达人的合作方式和报价区间建议

请按以下格式输出（Markdown表格 + 详细说明）：

## 推荐达人列表

| 序号 | 达人昵称 | 平台 | 内容垂类 | 粉丝量 | 平均互动率 | 估粉比评估 | 推荐理由 | 建议合作形式 | 预估报价区间 |
|------|---------|------|---------|--------|-----------|-----------|---------|------------|------------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... | ... |

（填入 8-12 个达人，数据标注"参考值"）

## 选号分析总结

### 整体推荐策略
- **头部达人**（100万+）：建议合作 X 位，用于...
- **中腰部达人**（10-100万）：建议合作 X 位，用于...
- **尾部KOC**（1-10万）：建议合作 X 位，用于...

### 注意事项
1. 数据为参考值，建议通过第三方数据平台（飞瓜/新榜/蝉妈妈）进一步验证
2. 实际报价需联系达人或通过MCN机构获取
3. 关注达人近期内容质量变化，避免合作期间内容质量下降

请开始生成推荐列表。"""

        return prompt

    def _build_analysis_prompt(self, data):
        monitor_data = data.get('data', [])
        dimensions = data.get('dimensions', [])
        extra = data.get('extra', '')
        campaign = data.get('campaign', {})

        # 构建数据摘要
        data_summary = ""
        if monitor_data:
            total_spend = sum(d.get('spend', 0) for d in monitor_data)
            total_impression = sum(d.get('impression', 0) for d in monitor_data)
            total_click = sum(d.get('click', 0) for d in monitor_data)
            total_interact = sum(d.get('interact', 0) for d in monitor_data)
            total_convert = sum(d.get('convert', 0) for d in monitor_data)

            data_summary += f"""
### 投放数据汇总
- **录入数据条数**：{len(monitor_data)} 条
- **总消耗**：{total_spend:,.0f} 元
- **总曝光**：{total_impression:,.0f}
- **总点击**：{total_click:,.0f}（点击率：{(total_click/total_impression*100) if total_impression > 0 else 0:.2f}%）
- **总互动**：{total_interact:,.0f}（互动率：{(total_interact/total_impression*100) if total_impression > 0 else 0:.2f}%）
- **总转化**：{total_convert:,.0f}（转化率：{(total_convert/total_click*100) if total_click > 0 else 0:.2f}%）

### 每日明细
| 日期 | 平台 | 消耗(元) | 曝光 | 点击 | 互动 | 转化 |
|------|------|----------|------|------|------|------|
"""
            for d in monitor_data:
                data_summary += f"| {d.get('date','')} | {d.get('platform','')} | {d.get('spend',0):,.0f} | {d.get('impression',0):,.0f} | {d.get('click',0):,.0f} | {d.get('interact',0):,.0f} | {d.get('convert',0):,.0f} |\n"

            # 按平台汇总
            by_platform = {}
            for d in monitor_data:
                p = d.get('platform', '')
                if p not in by_platform:
                    by_platform[p] = {'spend': 0, 'impression': 0, 'click': 0, 'interact': 0, 'convert': 0}
                by_platform[p]['spend'] += d.get('spend', 0)
                by_platform[p]['impression'] += d.get('impression', 0)
                by_platform[p]['click'] += d.get('click', 0)
                by_platform[p]['interact'] += d.get('interact', 0)
                by_platform[p]['convert'] += d.get('convert', 0)

            data_summary += "\n### 各平台汇总\n| 平台 | 消耗(元) | 曝光 | 点击率 | 互动率 | 转化率 | 单次点击成本 |\n|------|----------|------|--------|--------|--------|------------|\n"
            for p, v in by_platform.items():
                ctr = (v['click']/v['impression']*100) if v['impression'] > 0 else 0
                ir = (v['interact']/v['impression']*100) if v['impression'] > 0 else 0
                cvr = (v['convert']/v['click']*100) if v['click'] > 0 else 0
                cpc = (v['spend']/v['click']) if v['click'] > 0 else 0
                data_summary += f"| {p} | {v['spend']:,.0f} | {v['impression']:,.0f} | {ctr:.2f}% | {ir:.2f}% | {cvr:.2f}% | ¥{cpc:.2f} |\n"

        campaign_info = ""
        if campaign:
            campaign_info += f"""
### 投放计划信息
- 项目名称：{campaign.get('name', '-')}
- 投放周期：{campaign.get('start', '-')} 至 {campaign.get('end', '-')}
- 总预算：{campaign.get('budget', '-')} 万元
"""

        prompt = f"""你是专业的电视剧营销数据分析专家，请基于以下投放数据进行深度效果分析。

{campaign_info}
{data_summary}

【分析维度】
{', '.join(dimensions)}

{f'【补充说明】{extra}' if extra else ''}

请生成专业的效果分析报告，包括：

## 📊 整体效果评估
- 各项核心指标的达成情况
- 与行业平均水平的对比
- 总体评价和打分

## 📈 趋势分析
- 消耗趋势（是否平稳/有异常波动）
- 效果趋势（曝光/点击/互动的变化）
- 各平台表现对比

{'## 💰 ROI 分析' if 'ROI' in dimensions else ''}
- 各平台投入产出比
- 单次转化成本分析
- 预算使用效率评估

{'## 🎬 素材效果排名' if '素材' in dimensions else ''}
- 基于数据推断各类型素材的表现
- 高效素材特征总结
- 低效素材优化建议

{'## 👥 受众行为分析' if '受众' in dimensions else ''}
- 点击-互动-转化漏斗分析
- 用户行为特征
- 受众偏好洞察

{'## ⚠️ 异常预警' if '异常' in dimensions else ''}
- 数据异常点识别
- 潜在风险预警
- 应急处理建议

{'## 💡 优化建议' if '优化' in dimensions else ''}
- 即时可执行的优化方案
- 预算调整建议
- 内容策略调整
- 下阶段投放建议

请基于真实数据进行分析，给出具体、可操作的结论和建议。使用 Markdown 格式输出。"""

        return prompt

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
