# 🔧 代码补丁文件 - 直接复制使用

## 补丁1: recipe_consultant.py 新增方法

将以下代码添加到 `RecipeDesignConsultant` 类的末尾(在最后一个方法之后):

```python
    def analyze_pairing_direction(self, item1, item2):
        """
        智能判断配对方向: 风味相近 vs 风味对比
        返回详细的方向分析
        """
        families1 = self.translator.analyze_flavor_profile(item1.get('flavor_profiles', ''))
        families2 = self.translator.analyze_flavor_profile(item2.get('flavor_profiles', ''))
        
        # 计算相似度
        common_families = set(families1.keys()) & set(families2.keys())
        total_families = set(families1.keys()) | set(families2.keys())
        
        if len(total_families) == 0:
            similarity = 0
        else:
            similarity = len(common_families) / len(total_families)
        
        # 判断方向
        if similarity >= 0.6:
            direction = "harmony"
            direction_cn = "🌀 分子共鸣型 (风味相近)"
            description = "两者共享多个风味维度,形成分子共鸣,适合融合创作"
            badge_color = "harmony"
        elif similarity <= 0.3:
            direction = "contrast"
            direction_cn = "⚡ 极光碰撞型 (风味对比)"
            description = "风味维度差异显著,形成极光效应,可创造层次记忆点"
            badge_color = "contrast"
        else:
            direction = "balanced"
            direction_cn = "🎯 维度补偿型 (平衡)"
            description = "部分共鸣、部分对比,通过维度补偿实现平衡"
            badge_color = "balanced"
        
        return {
            "direction": direction,
            "direction_cn": direction_cn,
            "description": description,
            "similarity": similarity * 100,
            "common_count": len(common_families),
            "unique1_count": len(families1) - len(common_families),
            "unique2_count": len(families2) - len(common_families),
            "badge_color": badge_color
        }
    
    def determine_roles(self, item1, item2):
        """
        确定主辅基调
        基于风味复杂度和强度判断谁是主角
        """
        # 计算复杂度评分
        complexity1 = len(item1.get('flavor_families', {})) * 10
        complexity2 = len(item2.get('flavor_families', {})) * 10
        
        # 计算强度评分(基于分子数量)
        intensity1 = item1.get('molecules_count', 0) * 0.1
        intensity2 = item2.get('molecules_count', 0) * 0.1
        
        # 综合评分
        score1 = complexity1 + intensity1
        score2 = complexity2 + intensity2
        
        # 判断主辅
        if abs(score1 - score2) < 15:  # 差距小,平等关系
            return {
                "type": "equal",
                "primary": None,
                "secondary": None,
                "ratio": "1:1",
                "description": f"{item1['cn_name']} 与 {item2['cn_name']} 势均力敌,建议等比例使用,形成双主角格局"
            }
        elif score1 > score2:
            # item1是主角
            ratio_value = score1 / score2 if score2 > 0 else 2
            if ratio_value >= 2.0:
                ratio = "3:1"
            elif ratio_value >= 1.5:
                ratio = "2:1"
            else:
                ratio = "3:2"
            
            return {
                "type": "primary_secondary",
                "primary": item1,
                "secondary": item2,
                "ratio": ratio,
                "description": f"🎼 {item1['cn_name']} 作为【主基调】,提供核心风味框架; {item2['cn_name']} 作为【辅助层】,提升香气频率与记忆点"
            }
        else:
            # item2是主角
            ratio_value = score2 / score1 if score1 > 0 else 2
            if ratio_value >= 2.0:
                ratio = "3:1"
            elif ratio_value >= 1.5:
                ratio = "2:1"
            else:
                ratio = "3:2"
            
            return {
                "type": "primary_secondary",
                "primary": item2,
                "secondary": item1,
                "ratio": ratio,
                "description": f"🎼 {item2['cn_name']} 作为【主基调】,提供核心风味框架; {item1['cn_name']} 作为【辅助层】,提升香气频率与记忆点"
            }
    
    def generate_sensory_curve(self, item1, item2, direction_info, roles):
        """
        生成感官演变曲线
        描述入口、中段、尾韵的体验
        """
        if direction_info['direction'] == 'harmony':
            # 相近型配对
            curve = {
                "entry": f"入口即感受到 {item1['cn_name']} 与 {item2['cn_name']} 的分子共鸣,风味边界模糊,形成统一的味觉频率",
                "middle": f"中段两者融合深化,共享的风味分子产生叠加效应,强度提升,口腔充盈感明显",
                "finish": f"尾韵绵延悠长,融合风味在鼻后腔持续震荡,留下和谐的记忆印记"
            }
        elif direction_info['direction'] == 'contrast':
            # 对比型配对
            if roles['type'] == 'equal':
                curve = {
                    "entry": f"入口瞬间,{item1['cn_name']} 与 {item2['cn_name']} 形成戏剧性碰撞,两股风味各自独立yet共存",
                    "middle": f"中段出现对峙与对话,形成动态平衡,口腔左右两侧可能感知不同维度",
                    "finish": f"尾韵交替闪现,{item1['cn_name']} 与 {item2['cn_name']} 轮流占据意识,形成层次记忆"
                }
            else:
                primary_name = roles['primary']['cn_name']
                secondary_name = roles['secondary']['cn_name']
                curve = {
                    "entry": f"入口以 {primary_name} 的主基调铺底,{secondary_name} 作为尖锐的香气探针瞬间穿刺",
                    "middle": f"中段 {primary_name} 稳定展开,{secondary_name} 在其中游走,形成明暗对比与层次感",
                    "finish": f"尾韵 {primary_name} 逐渐淡化,{secondary_name} 的挥发性分子在鼻后腔持续闪现,留下悬念"
                }
        else:
            # 平衡型配对
            curve = {
                "entry": f"入口温和,{item1['cn_name']} 与 {item2['cn_name']} 以相近但不同的频率共同展开",
                "middle": f"中段出现互补与增强,共鸣部分加深,差异部分形成立体感",
                "finish": f"尾韵平衡收束,既有融合的温暖感,又保留各自的特征尾音"
            }
        
        return curve
```

---

## 补丁2: app_pro.py CSS样式增强

在 `app_pro.py` 的 `<style>` 标签内添加(约在第235行之前):

```css
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
        transition: transform 0.3s ease;
    }
    
    .direction-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    .badge-harmony {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1d1d1f;
        border: 2px solid #84fab0;
    }
    
    .badge-contrast {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #1d1d1f;
        border: 2px solid #fa709a;
    }
    
    .badge-balanced {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 2px solid #667eea;
    }
    
    /* 角色卡片 */
    .role-card {
        background: linear-gradient(135deg, #f5f5f7, #ffffff);
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
        background: linear-gradient(135deg, #f5f5f5, #ffffff);
    }
    
    /* 感官曲线卡片 */
    .sensory-curve {
        background: linear-gradient(135deg, #fff8e1, #ffffff);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #ffd54f;
    }
```

---

## 补丁3: app_pro.py 侧边栏中文显示

找到 `app_pro.py` 约第686-692行的食材选择代码,替换为:

```python
    # 🔥 新版: 完全中文显示
    # 创建显示映射: "中文名 · English Name"
    food_display_map = {}
    for item in lab.data:
        food_display_map[item['name']] = f"{item['cn_name']} · {item['name']}"
    
    selected_names = st.multiselect(
        "选择 2 种食材进行深度分析:",
        options=[item['name'] for item in lab.data],
        format_func=lambda x: food_display_map.get(x, x),  # ✨ 关键改动
        max_selections=2,
        default=[],
        help="选择两种食材,系统将分析它们的分子共鸣与风味碰撞"
    )
```

---

## 补丁4: app_pro.py 双食材分析部分

找到 `app_pro.py` 约第750行 `if len(selected_items) == 2:` 部分,
在显示完食材卡片后(约第835行 `st.markdown('</div>', unsafe_allow_html=True)` 之后),
添加以下代码:

```python
    # ========== 虫洞风格配对分析 ==========
    st.markdown("---")
    st.markdown("## 🌀 配对分析", unsafe_allow_html=True)
    
    # 分析配对方向
    direction_info = lab.consultant.analyze_pairing_direction(item1, item2)
    
    # 确定主辅角色
    roles = lab.consultant.determine_roles(item1, item2)
    
    # 原有的深度分析
    analysis = lab.consultant.analyze_pairing(item1, item2)
    
    # ========== 显示配对方向 ==========
    st.markdown(f"""
    <div style="text-align:center;margin:2rem 0;">
        <span class="direction-badge badge-{direction_info['badge_color']}">
            {direction_info['direction_cn']}
        </span>
        <div style="margin-top:1rem;font-size:1rem;color:#666;">
            {direction_info['description']}
        </div>
        <div style="margin-top:0.8rem;font-size:0.95rem;color:#0071e3;font-weight:500;">
            相似度: {direction_info['similarity']:.1f}% | 
            共鸣维度: {direction_info['common_count']} | 
            独特维度: {direction_info['unique1_count']} + {direction_info['unique2_count']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== 主辅基调定位 ==========
    st.markdown("## 🎯 主辅基调定位", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #f5f5f7, #fafafa);border-radius:16px;padding:1.8rem;margin:1.5rem 0;border:2px solid #e0e0e0;">
        <div style="font-size:1.1rem;color:#1d1d1f;margin-bottom:1.2rem;line-height:1.6;">
            {roles['description']}
        </div>
        <div style="font-size:1.8rem;font-weight:700;color:#0071e3;text-align:center;margin-top:1rem;">
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
                    🎼 主基调 (Primary)
                </div>
                <div style="font-size:1.4rem;font-weight:600;color:#1d1d1f;margin:0.8rem 0;">
                    {roles['primary']['cn_name']}
                </div>
                <div style="font-size:0.9rem;color:#666;line-height:1.6;">
                    提供核心风味框架与持久基调,构建味觉记忆的主要坐标系
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="role-card role-secondary">
                <div style="font-size:1.1rem;font-weight:600;color:#666;margin-bottom:0.8rem;">
                    🎵 辅助层 (Supporting)
                </div>
                <div style="font-size:1.4rem;font-weight:600;color:#1d1d1f;margin:0.8rem 0;">
                    {roles['secondary']['cn_name']}
                </div>
                <div style="font-size:0.9rem;color:#666;line-height:1.6;">
                    提升香气频率,制造层次记忆点,发挥"极光穿刺"效应
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========== 感官演变曲线 ==========
    st.markdown("## 🧪 感官演变曲线", unsafe_allow_html=True)
    
    sensory_curve = lab.consultant.generate_sensory_curve(item1, item2, direction_info, roles)
    
    st.markdown(f"""
    <div class="sensory-curve">
        <div style="margin-bottom:1.2rem;">
            <div style="font-size:1rem;font-weight:600;color:#f57c00;margin-bottom:0.5rem;">⚡ 入口 (Entry)</div>
            <div style="color:#333;line-height:1.7;">{sensory_curve['entry']}</div>
        </div>
        
        <div style="margin-bottom:1.2rem;">
            <div style="font-size:1rem;font-weight:600;color:#f57c00;margin-bottom:0.5rem;">🌊 中段 (Middle)</div>
            <div style="color:#333;line-height:1.7;">{sensory_curve['middle']}</div>
        </div>
        
        <div>
            <div style="font-size:1rem;font-weight:600;color:#f57c00;margin-bottom:0.5rem;">💫 尾韵 (Finish)</div>
            <div style="color:#333;line-height:1.7;">{sensory_curve['finish']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## 补丁5: AI功能集成 (可选)

在 `app_pro.py` 文件顶部添加AI函数(在imports之后):

```python
def generate_ai_chef_recommendations(item1, item2, direction, roles, api_key):
    """
    使用Claude API生成专业厨师建议
    按照《味觉虫洞》风格
    """
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""你是《味觉虫洞》实验室的首席风味设计师。请为以下食材组合提供专业建议。

## 食材信息
食材1: {item1['cn_name']} ({item1['name']})
食材2: {item2['cn_name']} ({item2['name']})

## 配对分析
- 配对方向: {direction['direction_cn']}
- 相似度: {direction['similarity']:.1f}%
- 角色定位: {roles['description']}
- 建议配比: {roles['ratio']}

## 请提供
1. 👨‍🍳 **厨师应用场景** (3-4个)
   - 场景名称(如: 🍹 分子融合饮品)
   - 具体做法(50-80字)
   - 技术要点(温度/时间/顺序)

2. 📊 **风味星图参数**
   - 精确配比建议
   - 处理顺序
   - 温度控制
   - 时间节点

请使用专业、前卫的语言,包含"频率"、"维度"、"碰撞"、"共振"等术语。"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
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

然后在感官曲线之后添加AI调用部分:

```python
    # ========== AI厨师建议(可选) ==========
    st.markdown("---")
    st.markdown("## 👨‍🍳 专业应用场景", unsafe_allow_html=True)
    
    use_ai = st.checkbox("🤖 启用AI生成专业建议", value=False, 
                         help="需要Anthropic API密钥。不启用时显示基础建议。")
    
    if use_ai:
        api_key_input = st.text_input(
            "输入API密钥",
            type="password",
            help="从 https://console.anthropic.com 获取",
            placeholder="sk-ant-..."
        )
        
        if api_key_input and st.button("🚀 生成AI建议"):
            with st.spinner("🌀 虫洞计算中... AI正在分析分子结构..."):
                ai_result = generate_ai_chef_recommendations(
                    item1, item2, direction_info, roles, api_key_input
                )
            
            if ai_result['success']:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #667eea 10%, #764ba2 100%);
                           color:white;border-radius:16px;padding:2rem;margin:1rem 0;">
                    {ai_result['content']}
                </div>
                """, unsafe_allow_html=True)
                st.success("✅ AI建议生成成功!")
            else:
                st.error(f"❌ AI调用失败: {ai_result['error']}")
                st.info("💡 请检查API密钥是否正确,或稍后重试")
    else:
        # 显示基础建议
        recommendations = analysis['recommendations']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📝 通用建议")
            for tip in recommendations['general']:
                st.markdown(f"- {tip}")
        
        with col2:
            if recommendations['techniques']:
                st.markdown("### 🔧 处理技巧")
                for tech in recommendations['techniques'][:3]:
                    st.markdown(f"- {tech}")
        
        st.info("💡 启用AI功能获取《味觉虫洞》风格的专业建议")
```

---

## ✅ 使用方法

### 方法1: 直接复制粘贴
1. 打开对应的文件
2. 找到指定位置
3. 复制粘贴对应的补丁代码
4. 保存文件
5. 重启应用

### 方法2: 使用git apply
```bash
# 将此文件保存为 patch.txt
git apply patch.txt
```

### 方法3: 手动对照修改
参考每个补丁的说明,在对应位置添加代码

---

## 🎯 验证步骤

修改完成后,运行应用测试:

1. **侧边栏中文**: 下拉菜单应显示 "苹果 · Apple"
2. **配对方向**: 选择两个食材后应显示彩色徽章
3. **主辅基调**: 应显示两个卡片,标明主角和配角
4. **感官曲线**: 应显示入口/中段/尾韵三段描述
5. **AI建议**: 勾选后可输入API密钥并生成

---

祝你升级顺利! 🌀✨
