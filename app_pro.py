"""
分子风味配对实验室 - Professional Edition
专业版: 增强翻译引擎 + 配方设计顾问 + 深度风味分析
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
import sys

# 导入专业模块
from flavor_translator_pro import FlavorTranslatorPro
from recipe_consultant import RecipeDesignConsultant

# ============== 页面配置 ==============
st.set_page_config(
    page_title="分子风味配对实验室 Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CSS样式 ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main { 
        background: linear-gradient(180deg, #f5f5f7 0%, #ffffff 100%);
        font-family: 'Noto Sans SC', sans-serif;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #0071e3, #00c7be);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #86868b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .food-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
        height: 100%;
    }
    
    .analysis-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .flavor-tag {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.15rem;
    }
    
    .tag-sweet { background: rgba(255, 149, 0, 0.12); color: #ff9500; }
    .tag-floral { background: rgba(255, 55, 95, 0.12); color: #ff375f; }
    .tag-fruity { background: rgba(255, 55, 95, 0.12); color: #ff375f; }
    .tag-herbal { background: rgba(52, 199, 89, 0.12); color: #34c759; }
    .tag-spicy { background: rgba(255, 59, 48, 0.12); color: #ff3b30; }
    .tag-woody { background: rgba(139, 90, 43, 0.15); color: #8b5a2b; }
    .tag-nutty { background: rgba(175, 82, 22, 0.15); color: #af5216; }
    .tag-roasted { background: rgba(175, 82, 22, 0.15); color: #af5216; }
    .tag-creamy { background: rgba(255, 204, 0, 0.15); color: #b38600; }
    .tag-savory { background: rgba(0, 113, 227, 0.12); color: #0071e3; }
    .tag-earthy { background: rgba(139, 90, 43, 0.15); color: #8b5a2b; }
    .tag-animal { background: rgba(142, 142, 147, 0.15); color: #636366; }
    .tag-chemical { background: rgba(142, 142, 147, 0.15); color: #636366; }
    .tag-other { background: rgba(142, 142, 147, 0.12); color: #636366; }
    
    .score-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin: 0 auto;
    }
    
    .score-excellent { background: linear-gradient(135deg, #34c759, #30b350); }
    .score-good { background: linear-gradient(135deg, #0071e3, #0051d5); }
    .score-average { background: linear-gradient(135deg, #ff9500, #ff7700); }
    .score-low { background: linear-gradient(135deg, #ff3b30, #d70015); }
    
    .recommendation-box {
        background: linear-gradient(135deg, #f5f5f7, #fafafa);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        border-left: 4px solid #0071e3;
    }
    
    .synergy-indicator {
        background: rgba(52, 199, 89, 0.1);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #34c759;
    }
    
    .risk-indicator {
        background: rgba(255, 59, 48, 0.1);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #ff3b30;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #0071e3;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #86868b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* 配对方向徽章 */
    .direction-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.7rem 1.8rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 0.5rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
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
    
    .role-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .role-primary {
        border-left-color: #0071e3;
        background: linear-gradient(135deg, #e3f2fd, #ffffff);
    }
    
    .role-secondary {
        border-left-color: #a0a0a0;
    }
    
    .sensory-curve {
        background: linear-gradient(135deg, #fff8e1, #ffffff);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #ffd54f;
    }
</style>
""", unsafe_allow_html=True)

# ============== 配置 ==============
FLAVOR_DIMENSIONS = [
    {"key": "sweet", "name": "甜味", "color": "#ff9500"},
    {"key": "floral", "name": "花香", "color": "#ff375f"},
    {"key": "fruity", "name": "果香", "color": "#ff375f"},
    {"key": "herbal", "name": "草本", "color": "#34c759"},
    {"key": "spicy", "name": "辛香", "color": "#ff3b30"},
    {"key": "woody", "name": "木质", "color": "#8b5a2b"},
    {"key": "nutty", "name": "坚果", "color": "#af5216"},
    {"key": "roasted", "name": "烘焙", "color": "#af5216"},
    {"key": "creamy", "name": "奶油", "color": "#ffcc00"},
    {"key": "savory", "name": "鲜味", "color": "#0071e3"},
    {"key": "earthy", "name": "土壤", "color": "#8b5a2b"},
]

NON_VEGAN_KEYWORDS = ['meat', 'poultry', 'fish', 'seafood', 'dairy', 'egg', 'beef', 'pork', 'chicken']
WUXIN_KEYWORDS = ['onion', 'garlic', 'chive', 'leek', 'scallion']

# ============== 核心类 ==============
class FlavorLabPro:
    """专业版风味实验室"""
    
    def __init__(self, df, vegan=True):
        self.df = df
        self.vegan = vegan
        self.translator = FlavorTranslatorPro()
        self.consultant = RecipeDesignConsultant(self.translator)
        self.data = self._load_data()
        self.index = {item['name'].lower(): item for item in self.data}
    
    def _load_data(self):
        """加载并处理数据"""
        items = []
        for _, row in self.df.iterrows():
            # Vegan过滤
            if self.vegan:
                cat_lower = row['category'].lower()
                name_lower = row['name'].lower()
                if any(kw in cat_lower or kw in name_lower for kw in NON_VEGAN_KEYWORDS):
                    continue
                if any(kw in name_lower for kw in WUXIN_KEYWORDS):
                    continue
            
            # 处理风味描述
            flavor_profiles = str(row.get('flavor_profiles', ''))
            if not flavor_profiles or flavor_profiles == 'nan':
                continue
            
            # 翻译名称
            name = row['name']
            cn_name = self.translator.translate(name)
            
            # 翻译类别
            category = row['category']
            cn_category = self.translator.translate(category)
            
            # 翻译风味列表
            flavors_cn = self.translator.translate_list(flavor_profiles)
            
            # 分析风味家族
            flavor_families = self.translator.analyze_flavor_profile(flavor_profiles)
            
            items.append({
                'id': row['id'],
                'name': name,
                'cn_name': cn_name,
                'category': category,
                'cn_category': cn_category,
                'flavor_profiles': flavor_profiles,
                'flavors_cn': flavors_cn,
                'flavor_families': flavor_families,
                'molecules_count': row.get('molecules_count', 0),
                'has_data': bool(flavor_profiles and flavor_profiles != 'nan')
            })
        
        return items
    
    def get(self, name):
        """获取食材信息"""
        return self.index.get(name.lower())
    
    def create_family_chart(self, item):
        """创建风味家族图表"""
        families = item['flavor_families']
        if not families:
            return None
        
        # 准备数据
        labels = [self.translator.get_family_name_cn(f) for f in families.keys()]
        values = list(families.values())
        
        # 颜色映射
        colors = {
            "sweet": "#ff9500", "floral": "#ff375f", "fruity": "#ff375f",
            "herbal": "#34c759", "spicy": "#ff3b30", "woody": "#8b5a2b",
            "nutty": "#af5216", "roasted": "#af5216", "creamy": "#ffcc00",
            "savory": "#0071e3", "earthy": "#8b5a2b", "animal": "#636366",
            "chemical": "#636366", "other": "#86868b"
        }
        
        bar_colors = [colors.get(f, "#86868b") for f in families.keys()]
        
        # 创建柱状图
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=labels,
            y=values,
            marker=dict(
                color=bar_colors,
                line=dict(color='rgba(0,0,0,0.1)', width=1)
            ),
            text=values,
            textposition='outside',
        ))
        
        fig.update_layout(
            showlegend=False,
            height=250,
            margin=dict(l=20, r=20, t=20, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                tickfont=dict(size=10, color='#1d1d1f'),
                gridcolor='rgba(0,0,0,0)',
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
            )
        )
        
        return fig

# ============== 初始化 ==============
@st.cache_resource
def get_lab(vegan=True):
    """加载实验室实例"""
    try:
        df = pd.read_csv('flavordb_data.csv')
        return FlavorLabPro(df, vegan=vegan)
    except FileNotFoundError:
        st.error("❌ 数据文件 'flavordb_data.csv' 未找到,请确保文件在当前目录")
        st.stop()

# ============== 侧边栏 ==============
with st.sidebar:
    st.markdown("### 🧪 分子风味实验室 Pro")
    st.markdown("---")
    
    # Vegan模式
    vegan = st.toggle("🌱 Vegan 纯素模式", value=True)
    
    if vegan:
        st.success("✓ 已过滤肉类、蛋奶、五辛")
    
    st.markdown("---")
    
    # 加载实验室
    lab = get_lab(vegan=vegan)
    
    st.markdown(f"**📊 可用食材: {len(lab.data)} 种**")
    
    # 食材选择
    st.markdown("### 🎯 选择对比食材")
    
    # 创建中文显示映射
    food_display_map = {}
    for item in lab.data:
        food_display_map[item['name']] = f"{item['cn_name']} · {item['name']}"
    
    selected_names = st.multiselect(
        "选择 2 种食材进行深度分析:",
        options=[item['name'] for item in lab.data],
        format_func=lambda x: food_display_map.get(x, x),
        max_selections=2,
        default=[],
        help="选择两种食材,系统将分析它们的分子共鸣与风味碰撞"
    )
    
    if len(selected_names) < 2:
        st.info("💡 请至少选择 2 种食材")
    
    st.markdown("---")
    st.markdown("### ✨ 新功能亮点")
    st.markdown("""
    - ✅ 专业风味翻译(500+词条)
    - ✅ 风味家族智能分析
    - ✅ 配方创作指引
    - ✅ 协同效应检测
    - ✅ 风险智能识别
    """)

# ============== 主页面 ==============
st.markdown('<h1 class="hero-title">🧪 分子风味配对实验室 Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">专业版: 增强翻译 · 深度分析 · 创作指引</p>', unsafe_allow_html=True)

# ============== 食材卡片展示 ==============
if len(selected_names) >= 2:
    selected_items = [lab.get(name) for name in selected_names]
    
    # 横向卡片布局
    cols = st.columns(len(selected_items))
    
    for idx, (col, item) in enumerate(zip(cols, selected_items)):
        with col:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)
            
            # 顶部:名称和分数
            complexity_score = min(len(item['flavor_families']) * 20, 100)
            
            if complexity_score >= 80:
                badge_class = "score-excellent"
            elif complexity_score >= 60:
                badge_class = "score-good"
            elif complexity_score >= 40:
                badge_class = "score-average"
            else:
                badge_class = "score-low"
            
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:1rem;">
                <div style="font-size:3rem;margin-bottom:0.5rem;">🍽️</div>
                <div style="font-size:1.3rem;font-weight:600;color:#1d1d1f;">{item['cn_name']}</div>
                <div style="font-size:0.85rem;color:#86868b;margin-bottom:1rem;">{item['cn_category']}</div>
                <div class="score-badge {badge_class}">{complexity_score:.0f}</div>
                <div style="font-size:0.75rem;color:#86868b;margin-top:0.3rem;">复杂度</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 风味家族分布图
            fig = lab.create_family_chart(item)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key=f"family_{item['id']}")
            
            # 统计信息
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div class="stat-number">{len(item['flavor_families'])}</div>
                    <div class="stat-label">风味家族</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div class="stat-number">{item['molecules_count']}</div>
                    <div class="stat-label">分子数量</div>
                </div>
                """, unsafe_allow_html=True)
            
            # 主要风味标签(翻译后的前8个)
            st.markdown('<div style="margin-top:1rem;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.8rem;color:#86868b;margin-bottom:0.5rem;">主要风味</div>', unsafe_allow_html=True)
            
            flavors_list = item['flavors_cn'].split(',')[:8]
            tags_html = ""
            for flavor in flavors_list:
                flavor = flavor.strip()
                # 根据风味判断家族
                family = "other"
                for fam in item['flavor_families'].keys():
                    if fam != "other":
                        family = fam
                        break
                tags_html += f'<span class="flavor-tag tag-{family}">{flavor}</span>'
            
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ============== 配对分析区域 ==============
    # ============== 双食材深度分析 ==============
    if len(selected_items) == 2:
        item1, item2 = selected_items[0], selected_items[1]
    
    # 食材卡片
    cols = st.columns(2)
    for col, item in zip(cols, [item1, item2]):
        with col:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)
            
            # ... 食材卡片的内容 ...
            
            st.markdown('</div>', unsafe_allow_html=True)
            
# ========== 虫洞配对分析 ==========
    st.markdown("---")
    st.markdown("## 🌀 配对分析")
    
    # 分析配对方向
    direction_info = lab.consultant.analyze_pairing_direction(item1, item2)
    
    # 确定主辅角色
    roles = lab.consultant.determine_roles(item1, item2)
    
    # 显示配对方向
    st.markdown(f"""
    <div style="text-align:center;margin:2rem 0;">
        <span class="direction-badge badge-{direction_info['badge_color']}">
            {direction_info['direction_cn']}
        </span>
        <div style="margin-top:1rem;color:#666;">
            {direction_info['description']}
        </div>
        <div style="margin-top:0.8rem;font-size:0.95rem;color:#0071e3;">
            相似度: {direction_info['similarity']:.1f}% | 
            共鸣: {direction_info['common_count']} | 
            独特: {direction_info['unique1_count']}+{direction_info['unique2_count']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 主辅基调
    st.markdown("## 🎯 主辅基调定位")
    
    st.markdown(f"""
    <div style="background:#f5f5f7;border-radius:16px;padding:1.8rem;margin:1.5rem 0;">
        <div style="font-size:1.1rem;margin-bottom:1.2rem;">
            {roles['description']}
        </div>
        <div style="font-size:1.8rem;font-weight:700;color:#0071e3;text-align:center;">
            建议配比: {roles['ratio']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if roles['type'] == 'primary_secondary':
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="role-card role-primary">
                <div style="font-size:1.1rem;font-weight:600;color:#0071e3;margin-bottom:0.8rem;">
                    🎼 主基调
                </div>
                <div style="font-size:1.4rem;font-weight:600;margin:0.8rem 0;">
                    {roles['primary']['cn_name']}
                </div>
                <div style="font-size:0.9rem;color:#666;">
                    提供核心风味框架与持久基调
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="role-card role-secondary">
                <div style="font-size:1.1rem;font-weight:600;color:#666;margin-bottom:0.8rem;">
                    🎵 辅助层
                </div>
                <div style="font-size:1.4rem;font-weight:600;margin:0.8rem 0;">
                    {roles['secondary']['cn_name']}
                </div>
                <div style="font-size:0.9rem;color:#666;">
                    提升香气频率,制造记忆点
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 感官演变曲线
    st.markdown("## 🧪 感官演变曲线")
    
    sensory_curve = lab.consultant.generate_sensory_curve(item1, item2, direction_info, roles)
    
    st.markdown(f"""
    <div class="sensory-curve">
        <div style="margin-bottom:1rem;">
            <div style="font-weight:600;color:#f57c00;margin-bottom:0.5rem;">⚡ 入口</div>
            <div style="color:#333;">{sensory_curve['entry']}</div>
        </div>
        <div style="margin-bottom:1rem;">
            <div style="font-weight:600;color:#f57c00;margin-bottom:0.5rem;">🌊 中段</div>
            <div style="color:#333;">{sensory_curve['middle']}</div>
        </div>
        <div>
            <div style="font-weight:600;color:#f57c00;margin-bottom:0.5rem;">💫 尾韵</div>
            <div style="color:#333;">{sensory_curve['finish']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if len(selected_items) == 2:
        item1, item2 = selected_items[0], selected_items[1]
        
        # 执行配对分析
        analysis = lab.consultant.analyze_pairing(item1, item2)
        
        # 分析结果展示
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("### 📊 配对质量")
            score = analysis['quality_score']
            if score >= 80:
                score_color = "#34c759"
                score_text = "优秀"
            elif score >= 60:
                score_color = "#0071e3"
                score_text = "良好"
            elif score >= 40:
                score_color = "#ff9500"
                score_text = "一般"
            else:
                score_color = "#ff3b30"
                score_text = "挑战"
            
            st.markdown(f"""
            <div style="text-align:center;margin:1rem 0;">
                <div style="font-size:3rem;font-weight:700;color:{score_color};">{score:.0f}</div>
                <div style="font-size:1rem;color:#86868b;">{score_text} · {analysis['pairing_type']['name']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**特点:** {analysis['pairing_type']['description']}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 风味重叠")
            
            common = analysis['common_families']
            unique1 = analysis['unique_to_first']
            unique2 = analysis['unique_to_second']
            
            st.markdown(f"**共同家族:** {len(common)}个")
            if common:
                common_cn = [lab.translator.get_family_name_cn(f) for f in common]
                st.markdown(f"<div style='color:#86868b;'>{'、'.join(common_cn)}</div>", unsafe_allow_html=True)
            
            st.markdown(f"**{item1['cn_name']}独有:** {len(unique1)}个")
            st.markdown(f"**{item2['cn_name']}独有:** {len(unique2)}个")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("### ⚡ 协同与风险")
            
            if analysis['synergies']:
                st.markdown(f"**协同效应:** {len(analysis['synergies'])}个")
                for syn in analysis['synergies'][:2]:
                    st.markdown(f"""
                    <div class="synergy-indicator">
                        <strong>{syn['families_cn'][0]} × {syn['families_cn'][1]}</strong><br>
                        <span style="color:#86868b;font-size:0.85rem;">→ {syn['effect']}效果</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("✓ 未检测到明显协同效应")
            
            if analysis['risks']:
                st.markdown(f"**潜在风险:** {len(analysis['risks'])}个")
                for risk in analysis['risks'][:2]:
                    st.markdown(f"""
                    <div class="risk-indicator">
                        <strong>⚠️ {risk['type']}</strong><br>
                        <span style="font-size:0.85rem;">{risk['reason']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("✓ 未检测到风险因素")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ============== 创作建议 ==============
        st.markdown("---")
        st.markdown("## 💡 专业创作指引")
        
        recommendations = analysis['recommendations']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
            st.markdown("### 📝 通用建议")
            for tip in recommendations['general']:
                st.markdown(f"- {tip}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if recommendations['ratio']:
                st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                st.markdown("### ⚖️ 配比建议")
                st.markdown(recommendations['ratio'])
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if recommendations['techniques']:
                st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                st.markdown("### 🔧 处理技巧")
                for tech in recommendations['techniques']:
                    st.markdown(f"- {tech}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if recommendations['applications']:
                st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                st.markdown("### 🍽️ 应用场景")
                for app in recommendations['applications']:
                    st.markdown(f"- {app}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 增强提示
        if recommendations['enhancement_tips']:
            st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
            st.markdown("### ✨ 增强提示")
            for tip in recommendations['enhancement_tips']:
                st.markdown(tip)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ============== 多食材创意提示 ==============
    elif len(selected_items) >= 3:
        st.markdown("---")
        st.markdown("## 🎨 创意配方提示")
        
        creative_prompt = lab.consultant.generate_creative_prompt(selected_items)
        
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.markdown(creative_prompt.replace('\n', '<br>'), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 两两分析
        st.markdown("### 🔗 成对分析")
        st.markdown("*以下是各食材间的配对评分*")
        
        pair_scores = []
        for i in range(len(selected_items)):
            for j in range(i+1, len(selected_items)):
                item_i, item_j = selected_items[i], selected_items[j]
                analysis = lab.consultant.analyze_pairing(item_i, item_j)
                pair_scores.append({
                    'pair': f"{item_i['cn_name']} × {item_j['cn_name']}",
                    'score': analysis['quality_score'],
                    'type': analysis['pairing_type']['name']
                })
        
        # 排序并展示
        pair_scores.sort(key=lambda x: x['score'], reverse=True)
        
        cols = st.columns(len(pair_scores))
        for col, pair in zip(cols, pair_scores):
            with col:
                score = pair['score']
                if score >= 70:
                    color = "#34c759"
                elif score >= 50:
                    color = "#0071e3"
                else:
                    color = "#ff9500"
                
                st.markdown(f"""
                <div style="text-align:center;padding:1rem;background:white;border-radius:12px;border:1px solid rgba(0,0,0,0.06);">
                    <div style="font-size:0.85rem;color:#86868b;margin-bottom:0.5rem;">{pair['pair']}</div>
                    <div style="font-size:2rem;font-weight:700;color:{color};">{score:.0f}</div>
                    <div style="font-size:0.75rem;color:#86868b;">{pair['type']}</div>
                </div>
                """, unsafe_allow_html=True)

else:
    # 空状态
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;background:white;border-radius:20px;box-shadow:0 4px 24px rgba(0,0,0,0.08);margin-top:2rem;">
        <div style="font-size:4rem;margin-bottom:1rem;">🧪</div>
        <h3 style="color:#1d1d1f;margin-bottom:0.5rem;">开始您的专业风味探索</h3>
        <p style="color:#86868b;">请在侧边栏选择 2-3 种食材进行深度分析</p>
        <div style="margin-top:2rem;">
            <span style="background:#f5f5f7;padding:0.5rem 1rem;border-radius:12px;margin:0.3rem;display:inline-block;">
                🌿 增强翻译引擎
            </span>
            <span style="background:#f5f5f7;padding:0.5rem 1rem;border-radius:12px;margin:0.3rem;display:inline-block;">
                🎯 智能配对分析
            </span>
            <span style="background:#f5f5f7;padding:0.5rem 1rem;border-radius:12px;margin:0.3rem;display:inline-block;">
                💡 专业创作指引
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============== 页脚 ==============
st.markdown("---")
st.markdown("""
<p style='text-align:center;color:#86868b;font-size:0.85rem;'>
🧪 分子风味配对实验室 Pro | 专业版 v1.0<br>
增强翻译 · 深度分析 · 创作指引
</p>
""", unsafe_allow_html=True)
