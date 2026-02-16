# 🌀 味觉虫洞功能升级指南

## 你提出的核心需求

### 1. ❌ 侧边栏还是英文 → ✅ 需要完全中文化
### 2. ❌ 缺少风味相近/对比分析 → ✅ 需要智能判断配对方向  
### 3. ❌ 缺少主辅基调指导 → ✅ 需要明确谁是主角谁是配角
### 4. ❌ 缺少专业厨师建议 → ✅ 需要AI生成应用场景
### 5. ✅ 按照《味觉虫洞》Gem风格优化

---

## 🎯 完整升级方案

我已经为你准备了两个版本:

### 版本A: 快速修复版 (推荐,5分钟完成)
只需修改 `app_pro.py` 的几处代码,立即解决所有问题

### 版本B: 完整重构版 (专业,需要30分钟)
全新的"味觉虫洞"风格应用,包含所有高级功能

---

## 🚀 版本A: 快速修复 (推荐新手)

### 修复1: 侧边栏中文显示

在 `app_pro.py` 中找到第682-692行的食材选择代码,替换为:

```python
# 🔧 修复前 (旧代码)
food_options = [(item['name'], f"{lab.get_emoji(item['name'])} {item['cn_name']}") 
                for item in lab.data]

selected_names = st.multiselect(
    "选择 2-4 种食材进行对比:",
    options=[opt[0] for opt in food_options],
    format_func=lambda x: dict(food_options)[x],
    ...
)
```

```python
# ✅ 修复后 (新代码)
# 创建显示映射: "中文名 · English Name"
food_display_map = {
    item['name']: f"{item['cn_name']} · {item['name']}"
    for item in lab.data
}

selected_names = st.multiselect(
    "选择 2-3 种食材进行深度分析:",
    options=[item['name'] for item in lab.data],
    format_func=lambda x: food_display_map.get(x, x),  # 关键: 使用中文显示
    max_selections=3,
    default=[],
    help="选择食材查看它们的分子共鸣与风味碰撞"
)
```

---

### 修复2: 添加风味相近/对比分析

在 `recipe_consultant.py` 末尾添加新函数:

```python
def analyze_pairing_direction(self, item1, item2):
    """
    智能判断配对方向: 风味相近 vs 风味对比
    """
    families1 = self.translator.analyze_flavor_profile(item1.get('flavor_profiles', ''))
    families2 = self.translator.analyze_flavor_profile(item2.get('flavor_profiles', ''))
    
    # 计算相似度
    common = set(families1.keys()) & set(families2.keys())
    total = set(families1.keys()) | set(families2.keys())
    similarity = len(common) / len(total) if total else 0
    
    # 判断方向
    if similarity >= 0.6:
        return {
            "direction": "harmony",
            "direction_cn": "🌀 分子共鸣型 (风味相近)",
            "description": "两者共享多个风味维度,形成分子共鸣,适合融合创作",
            "similarity": similarity * 100,
            "badge_color": "harmony"  # 用于CSS样式
        }
    elif similarity <= 0.3:
        return {
            "direction": "contrast",
            "direction_cn": "⚡ 极光碰撞型 (风味对比)",
            "description": "风味维度差异显著,形成对比效应,可创造层次记忆点",
            "similarity": similarity * 100,
            "badge_color": "contrast"
        }
    else:
        return {
            "direction": "balanced",
            "direction_cn": "🎯 维度补偿型 (平衡)",
            "description": "部分共鸣、部分对比,通过维度补偿实现平衡",
            "similarity": similarity * 100,
            "badge_color": "balanced"
        }
```

然后在 `app_pro.py` 中使用:

```python
# 在配对分析部分添加 (约第850行)
if len(selected_items) == 2:
    item1, item2 = selected_items[0], selected_items[1]
    
    # ✨ 新增: 配对方向分析
    direction = lab.consultant.analyze_pairing_direction(item1, item2)
    
    st.markdown(f"""
    <div style="text-align:center;margin:2rem 0;">
        <span class="direction-badge badge-{direction['badge_color']}">
            {direction['direction_cn']}
        </span>
        <div style="margin-top:1rem;color:#86868b;">
            {direction['description']}
        </div>
        <div style="margin-top:0.5rem;font-size:0.9rem;color:#0071e3;">
            相似度: {direction['similarity']:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

### 修复3: 添加主辅基调判定

在 `recipe_consultant.py` 中添加:

```python
def determine_主辅_roles(self, item1, item2):
    """
    确定哪个是主基调,哪个是辅助
    基于风味复杂度和强度
    """
    # 计算复杂度
    complexity1 = len(item1.get('flavor_families', {})) * 10
    complexity2 = len(item2.get('flavor_families', {})) * 10
    
    # 计算风味强度(基于分子数量)
    intensity1 = item1.get('molecules_count', 0)
    intensity2 = item2.get('molecules_count', 0)
    
    # 综合评分
    score1 = complexity1 * 0.6 + intensity1 * 0.4
    score2 = complexity2 * 0.6 + intensity2 * 0.4
    
    # 判断主辅
    if abs(score1 - score2) < 15:  # 差距小
        return {
            "type": "equal",
            "ratio": "1:1",
            "description": f"{item1['cn_name']} 与 {item2['cn_name']} 势均力敌,建议等比例使用"
        }
    elif score1 > score2:
        ratio = "3:1" if score1 / score2 > 1.5 else "2:1"
        return {
            "type": "primary_secondary",
            "primary": item1,
            "secondary": item2,
            "ratio": ratio,
            "description": f"🎼 {item1['cn_name']} 作为【主基调】,{item2['cn_name']} 作为【辅助层】提升风味频率"
        }
    else:
        ratio = "3:1" if score2 / score1 > 1.5 else "2:1"
        return {
            "type": "primary_secondary",
            "primary": item2,
            "secondary": item1,
            "ratio": ratio,
            "description": f"🎼 {item2['cn_name']} 作为【主基调】,{item1['cn_name']} 作为【辅助层】提升风味频率"
        }
```

在 `app_pro.py` 中显示:

```python
# 主辅基调分析
roles = lab.consultant.determine_主辅_roles(item1, item2)

st.markdown("### 🎯 主辅基调定位")
st.markdown(f"""
<div style="background:#f5f5f7;border-radius:12px;padding:1.5rem;margin:1rem 0;">
    <div style="font-size:1.1rem;margin-bottom:1rem;">{roles['description']}</div>
    <div style="font-size:1.5rem;font-weight:600;color:#0071e3;text-align:center;">
        建议配比: {roles['ratio']}
    </div>
</div>
""", unsafe_allow_html=True)

if roles['type'] == 'primary_secondary':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:#e3f2fd;padding:1rem;border-radius:8px;border-left:4px solid #0071e3;">
            <div style="font-weight:600;color:#0071e3;">🎼 主基调</div>
            <div style="font-size:1.2rem;margin:0.5rem 0;">{roles['primary']['cn_name']}</div>
            <div style="font-size:0.85rem;color:#666;">提供核心风味框架</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#f5f5f5;padding:1rem;border-radius:8px;border-left:4px solid #999;">
            <div style="font-weight:600;color:#666;">🎵 辅助层</div>
            <div style="font-size:1.2rem;margin:0.5rem 0;">{roles['secondary']['cn_name']}</div>
            <div style="font-size:0.85rem;color:#666;">提升香气与记忆点</div>
        </div>
        """, unsafe_allow_html=True)
```

---

### 修复4: 添加AI厨师建议

在 `app_pro.py` 顶部添加AI函数:

```python
def generate_ai_chef_recommendations(item1, item2, direction, roles):
    """
    使用Claude API生成专业厨师建议
    按照《味觉虫洞》风格
    """
    try:
        import anthropic
        
        # 从环境变量或Streamlit secrets获取API密钥
        api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
        if not api_key:
            return {"success": False, "error": "未配置API密钥"}
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # 构建提示词
        prompt = f"""你是《味觉虫洞》实验室的首席风味设计师。

食材组合:
- 食材1: {item1['cn_name']} ({item1['name']})
- 食材2: {item2['cn_name']} ({item2['name']})

配对分析:
- 方向: {direction['direction_cn']}
- 相似度: {direction['similarity']:.1f}%
- 角色: {roles['description']}
- 配比: {roles['ratio']}

请提供3-4个专业烹饪应用场景,每个场景包括:
1. 场景名称(如: 🍹 分子融合饮品)
2. 具体做法(50-80字)
3. 技术要点(温度/时间/顺序)

使用专业、前卫的语言,包含"频率"、"碰撞"、"共振"等术语。"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "success": True,
            "content": message.content[0].text
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

在配对分析部分添加:

```python
# AI厨师建议
st.markdown("### 👨‍🍳 专业应用场景")

use_ai = st.checkbox("🤖 启用AI生成", value=False, 
                     help="需要配置Anthropic API密钥")

if use_ai:
    with st.spinner("🌀 AI计算中..."):
        ai_result = generate_ai_chef_recommendations(item1, item2, direction, roles)
    
    if ai_result['success']:
        st.markdown(ai_result['content'])
    else:
        st.error(f"AI调用失败: {ai_result['error']}")
        st.info("请在Streamlit secrets中配置 ANTHROPIC_API_KEY")
else:
    # 显示基础建议
    st.info("💡 启用AI获取专业厨师级建议")
```

---

### 修复5: 配置API密钥

创建 `.streamlit/secrets.toml` 文件:

```toml
# Anthropic API配置
ANTHROPIC_API_KEY = "sk-ant-你的密钥"
```

或者在Streamlit Cloud部署时:
1. 进入App设置
2. 找到 "Secrets"
3. 添加:
```
ANTHROPIC_API_KEY = "sk-ant-你的密钥"
```

---

## 📊 版本B: 完整《味觉虫洞》版本

如果你想要完整的虫洞风格,我已经创建了专门的模块:

### 文件结构:
```
flavor_app_wormhole/
├── app_wormhole.py          # 主应用(暗色主题)
├── wormhole_analyzer.py     # 虫洞分析器
├── wormhole_ai.py          # AI生成模块
├── wormhole_style.py        # 虫洞风格CSS
├── flavor_translator_pro.py # 翻译引擎
├── recipe_consultant.py     # 配方顾问
└── flavordb_data.csv        # 数据文件
```

### 核心特点:
1. **暗色科技风** - 紫色渐变+虫洞动画效果
2. **虫洞坐标** - 每个食材的味觉定位
3. **分子共鸣** - 智能检测风味共鸣点
4. **极光碰撞** - 识别对比型配对
5. **主辅基调** - 明确角色定位
6. **感官曲线** - 入口/中段/尾韵描述
7. **AI厨师** - Claude生成专业建议

---

## 🎨 CSS样式增强

在 `app_pro.py` 的CSS部分添加虫洞风格徽章:

```css
.direction-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1.5rem;
    border-radius: 25px;
    font-weight: 600;
    font-size: 1.1rem;
    margin: 0.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.badge-harmony {
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    color: #1d1d1f;
}

.badge-contrast {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    color: #1d1d1f;
}

.badge-balanced {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
```

---

## ✅ 快速验证清单

完成修改后,测试以下功能:

### 1. 侧边栏中文显示
- [ ] 食材列表显示为 "中文名 · English Name"
- [ ] 下拉菜单搜索中文有效
- [ ] 选中后显示中文名

### 2. 配对方向分析
- [ ] 选择两个相似食材(如苹果+梨),显示"分子共鸣型"
- [ ] 选择两个对比食材(如薄荷+巧克力),显示"极光碰撞型"
- [ ] 显示相似度百分比

### 3. 主辅基调
- [ ] 显示谁是主基调,谁是辅助
- [ ] 给出具体配比(如 3:1)
- [ ] 解释角色功能

### 4. AI建议
- [ ] 勾选"启用AI"后可输入API密钥
- [ ] 点击生成后显示loading动画
- [ ] 返回3-4个应用场景

---

## 🚀 部署步骤

### 本地测试:
```bash
# 1. 修改代码
nano app_pro.py
nano recipe_consultant.py

# 2. 创建secrets文件
mkdir .streamlit
echo 'ANTHROPIC_API_KEY = "sk-ant-你的密钥"' > .streamlit/secrets.toml

# 3. 运行测试
streamlit run app_pro.py
```

### GitHub部署:
```bash
# 1. 提交修改
git add .
git commit -m "✨ 添加虫洞风格分析"
git push

# 2. Streamlit Cloud会自动重新部署
# 3. 在App设置中添加ANTHROPIC_API_KEY secret
```

---

## 💡 常见问题

### Q1: API密钥如何获取?
A: 访问 https://console.anthropic.com → API Keys → Create Key

### Q2: 每次调用AI要钱吗?
A: 是的,按token计费。每次约$0.01-0.02,可以设置月度限额

### Q3: 不想用AI可以吗?
A: 可以!不勾选"启用AI"就用基础建议,完全免费

### Q4: 暗色主题太暗了怎么办?
A: 使用版本A(快速修复),保持原来的亮色主题

### Q5: 能同时显示3个食材吗?
A: 可以!但AI建议目前只支持2个食材配对,3个食材会分别两两分析

---

## 📞 需要帮助?

如果遇到问题:
1. 检查代码缩进(Python对缩进敏感)
2. 查看Streamlit控制台的错误信息
3. 确认所有文件都在同一目录
4. 测试API密钥是否有效

---

**推荐路径**: 先用版本A快速修复,测试功能是否满足需求,再考虑是否升级到完整的虫洞版本。

祝你升级顺利! 🌀✨
