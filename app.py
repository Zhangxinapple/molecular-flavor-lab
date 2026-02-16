import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import os

# ==========================================
# 1. AI 核心引擎：《味觉虫洞》 (Gem Persona)
# ==========================================
class TasteWormholeAgent:
    def __init__(self):
        # --- 核心汉化词典 ---
        self.name_map = {
            "bamboo shoots": "竹笋", "coffee": "咖啡", "dark chocolate": "黑巧克力",
            "green tea": "绿茶", "strawberry": "草莓", "apple": "苹果", "banana": "香蕉",
            "bread": "面包", "butter": "黄油", "cheese": "芝士", "tomato": "番茄",
            "pork": "猪肉", "beef": "牛肉", "chicken": "鸡肉", "shrimp": "虾",
            "bakery products": "烘焙制品", "dairy": "乳制品", "meat": "肉类",
            "potato": "土豆", "onion": "洋葱", "garlic": "大蒜", "ginger": "生姜",
            "mushroom": "蘑菇", "honey": "蜂蜜", "milk": "牛奶", "wine": "红酒",
            "soy sauce": "酱油", "rice": "米饭", "egg": "鸡蛋", "lemon": "柠檬"
        }
        # --- 风味属性映射 (用于计算 AI 坐标) ---
        self.flavor_attrs = {
            "green": "高频/挥发性/瞬时", "citrus": "极光/穿透力/酸", "spicy": "痛感/热能/缭绕",
            "roasted": "低频/基底/美拉德", "earthy": "沉降/暗调/后韵", "fatty": "包覆/介质/宽",
            "sweet": "填充/柔和/连接", "fruity": "中频/跳跃/甜酸", "floral": "轻盈/飘逸/前调"
        }
        # --- 风味名词汉化 ---
        self.flavor_cn = {
            "roasted": "烘焙感", "sweet": "甜美", "earthy": "大地息", "fruity": "果香",
            "green": "青草气", "spicy": "辛香", "fatty": "油脂感", "floral": "花香",
            "nutty": "坚果味", "woody": "木质调", "bitter": "苦味", "sulfurous": "硫味",
            "citrus": "柑橘调", "creamy": "奶油感", "smoky": "烟熏", "caramel": "焦糖"
        }

    def t(self, text, type='name'):
        """智能翻译与美化函数"""
        t_low = str(text).lower().strip()
        if type == 'name': 
            return self.name_map.get(t_low, t_low.replace("_", " ").title())
        # 风味翻译逻辑
        for k, v in self.flavor_cn.items():
            if k in t_low: return v
        # 分子名美化兜底
        if "acid" in t_low: return "有机酸"
        if "alcohol" in t_low: return "醇香"
        if "aldehyde" in t_low: return "醛香"
        return t_low.title()

    def analyze_frequency(self, mol_set):
        """AI 分析：计算食材的‘频率’属性"""
        high_freq = ["green", "citrus", "spicy", "floral", "fruit", "mint", "aldehyde"]
        low_freq = ["roasted", "earthy", "fatty", "nutty", "woody", "meat", "sulfur"]
        
        h_score = sum(1 for m in mol_set if any(k in m.lower() for k in high_freq))
        l_score = sum(1 for m in mol_set if any(k in m.lower() for k in low_freq))
        
        if h_score > l_score * 1.5: return "高频·挥发性·上扬"
        if l_score > h_score * 1.5: return "低频·沉降感·基底"
        return "中频·平衡·融合"

    def generate_report(self, ing1_name, ing2_name, score, common_mols, ing1_mols, ing2_mols):
        """生成《味觉虫洞》风格的 5 模块实验报告"""
        
        n1 = self.t(ing1_name)
        n2 = self.t(ing2_name)

        # 1. 🛰️ 虫洞坐标
        coord1 = self.analyze_frequency(ing1_mols)
        coord2 = self.analyze_frequency(ing2_mols)
        
        # 2. 🌀 关联逻辑
        if score > 7.5:
            logic_title = "分子共鸣 (Molecular Resonance)"
            logic_desc = "两者共享大量关键香气分子，味觉波形完美重叠。这是一种‘同频共振’，能产生 1+1>2 的味觉增幅。"
        elif score > 4.0:
            logic_title = "维度补偿 (Dimension Balance)"
            logic_desc = "存在部分连接点，但更多的是互补。一方提供骨架（如基底感），另一方提供血肉（如挥发香），形成完整的味觉闭环。"
        else:
            logic_title = "极光效应 (Aurora Effect)"
            logic_desc = "强烈的反差制造了‘鼻腔冲击力’。利用风味分子的冲突，制造类似芥末或跳跳糖般的感官极光，打破常规味觉疲劳。"

        # 3. 🧪 实验报告 (感官推演)
        common_desc = [self.t(m, 'flavor') for m in list(common_mols)[:3]]
        common_str = "、".join(common_desc) if common_desc else "隐性连接"
        
        if score > 6:
            report = f"入口瞬间，{n1}与{n2}的界限坍缩，爆发出一股{common_str}的混合香气。中段口感致密，尾韵在口腔中形成长久的共振。"
        else:
            report = f"入口是{n1}的特立独行，紧接着{n2}的香气穿透而来。这种‘冲突美学’在舌根处完成和解，留下一丝{common_str}的神秘回甘。"

        # 4. 👨‍🍳 厨师应用 (随机创意)
        apps = []
        if "高频" in coord1 or "高频" in coord2:
            apps.append("🥗 **前菜/冷盘：** 利用其高挥发性，做成冷萃酱汁或分子泡沫，瞬间打开味蕾。")
        if "低频" in coord1 or "低频" in coord2:
            apps.append("🥩 **主菜/酱汁：** 利用油脂或慢煮工艺，锁住低频香气，作为红肉的灵魂伴侣。")
        if score < 5:
             apps.append("🍸 **创意特调：** 利用反差感，制作一款具有‘分层口感’的鸡尾酒。")
        else:
             apps.append("🍰 **甜点/慕斯：** 高度融合的特性适合制作慕斯，口感无缝衔接。")
        
        # 确保总有建议
        if not apps: apps = ["🥘 **融合料理：** 尝试将其打碎混合，制作风味独特的复合黄油。"]
        chef_app = "<br>".join(random.sample(apps, min(2, len(apps))))

        # 5. 📊 风味星图参数
        if score > 8:
            params = "建议配比 **1:1** | 技术关键：**共融** (如炖煮、乳化)"
        elif score > 4:
            params = "建议配比 **1:3** (以低频食材为主) | 技术关键：**承载** (如油脂浸渍)"
        else:
            params = "建议配比 **1:10** (极少量点缀) | 技术关键：**触发** (如喷雾、擦丝)"

        # 生成 HTML 卡片
        html = f"""
        <div class="wormhole-box">
            <p><strong>🛰️ 虫洞坐标：</strong><br>
            <span style="color:#1d1d1f">[{n1}: {coord1}]</span> <span style="color:#0071e3">⚡</span> <span style="color:#1d1d1f">[{n2}: {coord2}]</span></p>
            
            <p style="margin-top:12px;"><strong>🌀 关联逻辑：{logic_title}</strong><br>
            <span style="color:#666">{logic_desc}</span></p>
            
            <p style="margin-top:12px;"><strong>🧪 实验报告：</strong><br>
            <span style="color:#666">{report}</span></p>
            
            <p style="margin-top:12px;"><strong>👨‍🍳 厨师应用：</strong><br>
            {chef_app}</p>
            
            <hr style="border-top: 1px dashed #d1d1d6; margin: 15px 0;">
            <p style="font-size:0.8rem; color:#86868b"><strong>📊 风味星图参数：</strong> {params}</p>
        </div>
        """
        return html

# 实例化 AI 代理
ai = TasteWormholeAgent()

# ==========================================
# 2. 页面配置与视觉样式 (Apple Style)
# ==========================================
st.set_page_config(page_title="味觉虫洞 Flavor Lab", page_icon="🧪", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap');
    
    .stApp { 
        background: #f5f5f7; 
        font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1d1d1f;
    }
    
    /* 苹果风格卡片 */
    .apple-card {
        background: rgba(255, 255, 255, 0.85); 
        backdrop-filter: blur(20px);
        border-radius: 20px; 
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.04); 
        border: 1px solid rgba(255,255,255,0.4);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .apple-card:hover { transform: translateY(-2px); }

    /* 标题 */
    h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.5px; }
    
    /* 分数勋章 */
    .score-badge { 
        background: linear-gradient(135deg, #0071e3, #00c7be); 
        color: white; 
        padding: 4px 12px; 
        border-radius: 99px; 
        font-weight: 700; 
        font-size: 1rem;
        box-shadow: 0 2px 10px rgba(0, 113, 227, 0.3);
    }

    /* 标签 Pill */
    .pill { display: inline-block; padding: 3px 10px; margin: 3px; border-radius: 8px; font-size: 0.75rem; font-weight: 500;}
    .pill-common { background: #e3f2fd; color: #0277bd; }
    
    /* 虫洞 AI 盒子 */
    .wormhole-box { 
        background: #fbfbfd; 
        border-radius: 16px; 
        padding: 20px; 
        font-size: 0.9rem; 
        line-height: 1.6;
        border-left: 4px solid #0071e3;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 数据处理与绘图
# ==========================================
@st.cache_data
def load_data():
    if not os.path.exists('flavordb_data.csv'): return None
    df = pd.read_csv('flavordb_data.csv').fillna('')
    # 清洗：过滤无数据的食材
    df = df[df['molecules_count'] > 0]
    df['mol_set'] = df['flavors'].apply(lambda x: set(str(x).replace('@', ',').split(',')))
    # 生成中文显示列
    df['display_name'] = df['name'].apply(lambda x: f"{ai.t(x)} ({x})")
    return df

def draw_radar(mols):
    dims = {"草本": ["green", "grass"], "果香": ["fruit", "berry"], "烘焙": ["roasted", "nutty"], 
            "大地": ["earthy", "wood"], "辛辣": ["spicy", "pepper"], "油脂": ["fatty", "creamy"]}
    vals = []
    for keys in dims.values():
        val = sum(1 for m in mols if any(k in m.lower() for k in keys))
        vals.append(min(val * 1.5, 10)) # 归一化到 0-10
    
    fig = go.Figure(data=go.Scatterpolar(r=vals, theta=list(dims.keys()), fill='toself', line_color='#0071e3'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False, range=[0, 10])), 
        showlegend=False, 
        height=180, 
        margin=dict(t=10,b=10,l=10,r=10), 
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color="#86868b")
    )
    return fig

# ==========================================
# 4. 主界面逻辑
# ==========================================
df = load_data()

if df is not None:
    st.markdown("<h1 style='text-align:center; margin-bottom: 30px;'>🌌 味觉虫洞 <span style='font-weight:300; font-size:1.5rem'>Flavor Lab</span></h1>", unsafe_allow_html=True)
    
    # 侧边栏
    st.sidebar.header("🧪 实验控制台")
    selected_displays = st.sidebar.multiselect(
        "选择食材开启虫洞 (建议 2-3 种):", 
        options=sorted(df['display_name'].unique()),
        default=sorted(df['display_name'].unique())[:2]
    )

    if 1 < len(selected_displays) <= 4:
        cols = st.columns(len(selected_displays))
        # 获取基准食材
        base_row = df[df['display_name'] == selected_displays[0]].iloc[0]

        for i, d_name in enumerate(selected_displays):
            row = df[df['display_name'] == d_name].iloc[0]
            common = base_row['mol_set'].intersection(row['mol_set'])
            score = round(len(common) * 1.5, 1) if i > 0 else 10.0
            
            with cols[i]:
                # 卡片容器
                st.markdown(f"""
                <div class="apple-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div style="font-size:1.4rem; font-weight:700;">{ai.t(row['name'])}</div>
                        <span class="score-badge">{"基准" if i == 0 else f"{score}分"}</span>
                    </div>
                    <div style="color:#86868b; font-size:0.8rem; margin-bottom:10px;">{ai.t(row['category'])}</div>
                """, unsafe_allow_html=True)
                
                # 雷达图
                st.plotly_chart(draw_radar(row['mol_set']), use_container_width=True, config={'displayModeBar':False})
                
                if i > 0:
                    # AI 分析报告
                    report_html = ai.generate_report(
                        base_row['name'], row['name'], score, common, base_row['mol_set'], row['mol_set']
                    )
                    st.markdown(report_html, unsafe_allow_html=True)
                    
                    # 共有分子标签
                    if len(common) > 0:
                        st.markdown(f"<div style='margin-top:10px; font-size:0.8rem; color:#86868b'>🔬 共有分子:</div>", unsafe_allow_html=True)
                        pills = "".join([f'<span class="pill pill-common">{ai.t(m, "flavor")}</span>' for m in list(common)[:8]])
                        st.markdown(pills, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align:center; padding:30px; color:#86868b; font-size:0.9rem;'>📡 信号发射源<br>(对比基准)</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👈 请在左侧侧边栏选择 2 至 4 种食材，启动味觉虫洞引擎。")

else:
    st.error("⚠️ 未检测到数据库文件。请确保 'flavordb_data.csv' 已上传至仓库根目录。")
