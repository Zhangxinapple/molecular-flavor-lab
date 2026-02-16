import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import os

# ==========================================
# 1. 核心 AI 引擎：《味觉虫洞》 (Gem Persona)
# ==========================================
class TasteWormholeAgent:
    def __init__(self):
        # 汉化词典：涵盖高频食材与风味
        self.name_map = {
            "bamboo shoots": "竹笋", "coffee": "咖啡", "dark chocolate": "黑巧克力",
            "green tea": "绿茶", "strawberry": "草莓", "apple": "苹果", "banana": "香蕉",
            "bread": "面包", "butter": "黄油", "cheese": "芝士", "tomato": "番茄",
            "pork": "猪肉", "beef": "牛肉", "chicken": "鸡肉", "shrimp": "虾",
            "onion": "洋葱", "garlic": "大蒜", "ginger": "生姜", "lemon": "柠檬",
            "bakery products": "烘焙制品", "dairy": "乳制品", "meat": "肉类"
        }
        self.flavor_cn = {
            "roasted": "烘焙感", "sweet": "甜美", "earthy": "大地息", "fruity": "果香",
            "green": "青草气", "spicy": "辛香", "fatty": "油脂感", "floral": "花香",
            "nutty": "坚果味", "woody": "木质调", "bitter": "苦味", "sulfurous": "硫味",
            "citrus": "柑橘调", "creamy": "奶油感", "smoky": "烟熏", "caramel": "焦糖"
        }

    def t(self, text, type='name'):
        t_low = str(text).lower().strip()
        if type == 'name': return self.name_map.get(t_low, t_low.replace("_", " ").title())
        for k, v in self.flavor_cn.items():
            if k in t_low: return v
        return t_low.title()

    def analyze_frequency(self, profile_text):
        """分析食材的'频率'属性 (基于描述文本)"""
        high = ["green", "citrus", "floral", "fruit", "herbal", "fresh"]
        low = ["roasted", "earthy", "fatty", "woody", "smoky", "nutty"]
        h_score = sum(1 for k in high if k in profile_text.lower())
        l_score = sum(1 for k in low if k in profile_text.lower())
        return "高频·挥发性·上扬" if h_score >= l_score else "低频·沉降感·基底"

    def generate_report(self, n1, n2, score, common_mols, profile1, profile2):
        """生成《味觉虫洞》Gem 设定的 5 模块报告"""
        c1, c2 = self.analyze_frequency(profile1), self.analyze_frequency(profile2)
        
        # 🌀 关联逻辑
        if score > 7.5:
            logic_t, logic_d = "分子共鸣", "两者共享核心香气分子，味觉波形完美重叠。这是一种‘同频共振’。"
        elif score > 4.0:
            logic_t, logic_d = "维度补偿", "存在连接点但互补性更强。一方提供骨架，另一方提供血肉。"
        else:
            logic_t, logic_d = "极光效应", "强烈的反差制造了‘鼻腔冲击力’，打破常规味觉疲劳。"

        # 🧪 实验报告
        report = f"入口瞬间，{self.t(n1)}与{self.t(n2)}的界限坍缩。中段口感致密，尾韵在共鸣点处完成和解。"

        # 👨‍🍳 厨师应用 (安全选择)
        apps = [
            "🥗 **前菜：** 利用高挥发性，做成冷萃酱汁或分子泡沫。",
            "🥩 **主菜：** 利用油脂介质锁住低频香气，作为主食材底色。",
            "🍸 **饮品：** 提取其香气精粹，利用反差感制作分层口感。"
        ]
        chef_app = random.choice(apps)

        return f"""
        <div class="wormhole-box">
            <p><strong>🛰️ 虫洞坐标：</strong><br>[{self.t(n1)}: {c1}] ⚡ [{self.t(n2)}: {c2}]</p>
            <p style="margin-top:8px;"><strong>🌀 关联逻辑：{logic_t}</strong><br><span style="color:#666;">{logic_d}</span></p>
            <p style="margin-top:8px;"><strong>🧪 实验报告：</strong><br><span style="color:#666;">{report}</span></p>
            <p style="margin-top:8px;"><strong>👨‍🍳 厨师应用：</strong><br>{chef_app}</p>
            <hr style="border-top: 1px dashed #ccc; margin:10px 0;">
            <p style="font-size:0.75rem; color:#86868b"><strong>📊 风味星图参数：</strong> 配比 1:{max(1, int(11-score))} | 技术：{'共融' if score > 7 else '触发'}</p>
        </div>
        """

ai = TasteWormholeAgent()

# ==========================================
# 2. 视觉样式 (Apple Style)
# ==========================================
st.set_page_config(page_title="味觉虫洞 Flavor Lab", layout="wide")
st.markdown("""
<style>
    .stApp { background: #f5f5f7; font-family: 'Noto Sans SC', sans-serif; }
    .apple-card { background: white; border-radius: 20px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom:20px; height:100%; }
    .score-badge { background: linear-gradient(90deg, #0071e3, #00c7be); color: white; padding: 4px 12px; border-radius: 12px; font-weight: 700; }
    .wormhole-box { background: #fbfbfd; border-radius: 15px; padding: 15px; border-left: 5px solid #0071e3; margin-top: 10px; font-size: 0.85rem; line-height: 1.5; }
    .pill { display: inline-block; padding: 2px 8px; margin: 2px; border-radius: 6px; font-size: 0.7rem; background: #e3f2fd; color: #0277bd; border: 1px solid #b3e5fc;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 数据处理
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('flavordb_data.csv').fillna('')
        df = df[df['molecules_count'] > 0]
        # 分子集合用于计算得分
        df['mol_set'] = df['flavors'].apply(lambda x: set(str(x).replace('@', ',').split(',')))
        df['display_name'] = df['name'].apply(lambda x: f"{ai.t(x)} ({x})")
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return None

df = load_data()

# ==========================================
# 4. 主界面渲染
# ==========================================
if df is not None:
    st.markdown("<h1 style='text-align:center;'>🌌 味觉虫洞 <span style='font-weight:300'>Flavor Lab</span></h1>", unsafe_allow_html=True)
    
    selected = st.sidebar.multiselect("选择 2-4 种食材开始实验:", options=sorted(df['display_name'].unique()))

    if len(selected) > 1:
        cols = st.columns(len(selected))
        base_row = df[df['display_name'] == selected[0]].iloc[0]

        for i, d_name in enumerate(selected):
            curr_row = df[df['display_name'] == d_name].iloc[0]
            common = base_row['mol_set'].intersection(curr_row['mol_set'])
            score = round(len(common) * 1.5, 1) if i > 0 else 10.0
            
            with cols[i]:
                st.markdown(f"""
                <div class="apple-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                        <span style="font-size:1.2rem; font-weight:700;">{ai.t(curr_row['name'])}</span>
                        <span class="score-badge">{"锚点" if i == 0 else f"{score}分"}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # 雷达图 (基于 flavor_profiles 文本匹配)
                dims = {"草本": "green", "果香": "fruit", "烘焙": "roasted", "大地": "earthy", "辛辣": "spicy", "油脂": "fatty"}
                vals = [min(str(curr_row['flavor_profiles']).lower().count(k) * 3, 10) for k in dims.values()]
                
                fig = go.Figure(data=go.Scatterpolar(r=vals, theta=list(dims.keys()), fill='toself', line_color='#0071e3'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 10])), showlegend=False, height=160, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                if i > 0:
                    # AI 专家报告
                    report_html = ai.generate_report(
                        base_row['name'], curr_row['name'], score, common, 
                        str(base_row['flavor_profiles']), str(curr_row['flavor_profiles'])
                    )
                    st.markdown(report_html, unsafe_allow_html=True)
                    
                    # 共有分子标签 (如果有)
                    if common:
                        st.markdown("<div style='font-size:0.75rem; color:#86868b; margin-top:5px;'>🔬 共有分子:</div>", unsafe_allow_html=True)
                        mols_list = list(common)[:5]
                        st.markdown(" ".join([f'<span class="pill">{ai.t(m, "flavor")}</span>' for m in mols_list]), unsafe_allow_html=True)
                else:
                    st.info("🎯 已选定为味觉锚点。AI 将以此为核心进行虫洞推演。")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:100px; color:#86868b; background:white; border-radius:20px;">
            <h3>🔭 正在扫描风味星图...</h3>
            <p>请在左侧侧边栏选择至少 2 种食材，启动《味觉虫洞》AI 引擎。</p>
        </div>
        """, unsafe_allow_html=True)
