"""
专业配方设计顾问 - Recipe Design Consultant
为创作者提供科学的风味搭配建议和创作指引
包含虫洞风格的新增方法
"""

from collections import defaultdict
import re


class RecipeDesignConsultant:
    """配方设计顾问 - 提供专业的风味搭配分析和创作建议"""
    
    def __init__(self, translator):
        """初始化设计顾问"""
        self.translator = translator
        
        # 风味搭配原则知识库
        self.pairing_principles = {
            "complementary": {
                "name": "互补原则",
                "description": "选择风味家族不同但互相补充的食材",
                "examples": [
                    "甜味系 + 酸味 = 平衡口感",
                    "奶油系 + 果香系 = 丰富层次",
                    "烘焙系 + 坚果系 = 深度风味"
                ]
            },
            "contrasting": {
                "name": "对比原则",
                "description": "利用强烈对比创造记忆点",
                "examples": [
                    "甜 vs 苦 = 巧克力配咖啡",
                    "辛辣 vs 奶油 = 咖喱配椰奶",
                    "酸 vs 鲜 = 柠檬配海鲜"
                ]
            },
            "layering": {
                "name": "层次原则",
                "description": "构建前调、中调、尾调的立体感",
                "examples": [
                    "前调: 柑橘、薄荷等挥发性香气",
                    "中调: 花香、果香等主体风味",
                    "尾调: 木质、香草等持久基调"
                ]
            },
            "regional": {
                "name": "地域原则",
                "description": "同一地域的食材天然协调",
                "examples": [
                    "地中海: 橄榄油 + 番茄 + 罗勒",
                    "东南亚: 椰子 + 柠檬草 + 辣椒",
                    "中东: 孜然 + 香菜 + 柠檬"
                ]
            }
        }
        
        # 风味协同增效关系
        self.synergy_pairs = {
            ("sweet", "bitter"): {"effect": "平衡", "strength": 0.9},
            ("fruity", "creamy"): {"effect": "融合", "strength": 0.95},
            ("roasted", "nutty"): {"effect": "增强", "strength": 0.85},
            ("spicy", "sweet"): {"effect": "对比", "strength": 0.8},
            ("floral", "fruity"): {"effect": "层次", "strength": 0.9},
            ("herbal", "citrus"): {"effect": "清新", "strength": 0.85},
            ("woody", "spicy"): {"effect": "深度", "strength": 0.8},
            ("savory", "roasted"): {"effect": "鲜美", "strength": 0.9},
        }
        
        # 风险组合
        self.risk_combinations = {
            ("floral", "animal"): {"type": "冲突", "reason": "花香与动物味容易产生违和感"},
            ("fruity", "sulfurous"): {"type": "冲突", "reason": "果香与硫化物不协调"},
            ("sweet", "sulfurous"): {"type": "冲突", "reason": "甜味难以平衡硫味"},
            ("chemical", "fruity"): {"type": "警告", "reason": "化学味可能压制果香"},
            ("metallic", "floral"): {"type": "警告", "reason": "金属味影响花香表达"},
        }
    
    def analyze_pairing(self, item1, item2):
        """深度分析两种食材的搭配关系"""
        profile1 = self.translator.analyze_flavor_profile(item1.get('flavor_profiles', ''))
        profile2 = self.translator.analyze_flavor_profile(item2.get('flavor_profiles', ''))
        
        common_families = set(profile1.keys()) & set(profile2.keys())
        unique1 = set(profile1.keys()) - set(profile2.keys())
        unique2 = set(profile2.keys()) - set(profile1.keys())
        
        synergies = self._find_synergies(profile1, profile2)
        risks = self._identify_risks(profile1, profile2)
        pairing_type = self._determine_pairing_type(common_families, unique1, unique2)
        quality_score = self._calculate_quality_score(
            common_families, synergies, risks, profile1, profile2
        )
        
        return {
            "quality_score": quality_score,
            "pairing_type": pairing_type,
            "common_families": list(common_families),
            "unique_to_first": list(unique1),
            "unique_to_second": list(unique2),
            "synergies": synergies,
            "risks": risks,
            "recommendations": self._generate_recommendations(
                item1, item2, pairing_type, synergies, risks, quality_score
            )
        }
    
    def _find_synergies(self, profile1, profile2):
        """查找风味协同效应"""
        synergies = []
        families1 = set(profile1.keys())
        families2 = set(profile2.keys())
        
        for (fam_a, fam_b), synergy_info in self.synergy_pairs.items():
            if (fam_a in families1 and fam_b in families2) or \
               (fam_b in families1 and fam_a in families2):
                synergies.append({
                    "families": [fam_a, fam_b],
                    "families_cn": [
                        self.translator.get_family_name_cn(fam_a),
                        self.translator.get_family_name_cn(fam_b)
                    ],
                    "effect": synergy_info["effect"],
                    "strength": synergy_info["strength"]
                })
        
        return sorted(synergies, key=lambda x: x["strength"], reverse=True)
    
    def _identify_risks(self, profile1, profile2):
        """识别搭配风险"""
        risks = []
        families1 = set(profile1.keys())
        families2 = set(profile2.keys())
        
        for (fam_a, fam_b), risk_info in self.risk_combinations.items():
            if (fam_a in families1 and fam_b in families2) or \
               (fam_b in families1 and fam_a in families2):
                risks.append({
                    "families": [fam_a, fam_b],
                    "families_cn": [
                        self.translator.get_family_name_cn(fam_a),
                        self.translator.get_family_name_cn(fam_b)
                    ],
                    "type": risk_info["type"],
                    "reason": risk_info["reason"]
                })
        
        return risks
    
    def _determine_pairing_type(self, common, unique1, unique2):
        """判断搭配类型"""
        if len(common) > len(unique1) + len(unique2):
            return {
                "type": "harmonious",
                "name": "和谐型",
                "description": "两种食材风味相似,容易融合"
            }
        elif len(unique1) + len(unique2) > len(common) * 2:
            return {
                "type": "contrasting",
                "name": "对比型",
                "description": "风味差异明显,可创造层次感"
            }
        else:
            return {
                "type": "balanced",
                "name": "平衡型",
                "description": "既有共同点又有差异,平衡协调"
            }
    
    def _calculate_quality_score(self, common, synergies, risks, profile1, profile2):
        """计算配对质量分数"""
        base_score = min(len(common) * 15, 50)
        synergy_bonus = sum(s["strength"] * 20 for s in synergies)
        risk_penalty = sum(20 if r["type"] == "冲突" else 10 for r in risks)
        total_families = len(set(profile1.keys()) | set(profile2.keys()))
        complexity_bonus = min(total_families * 3, 20)
        
        final_score = base_score + synergy_bonus + complexity_bonus - risk_penalty
        return max(0, min(100, final_score))
    
    def _generate_recommendations(self, item1, item2, pairing_type, 
                                 synergies, risks, quality_score):
        """生成配方创作建议"""
        recommendations = {
            "general": [],
            "ratio": None,
            "techniques": [],
            "applications": [],
            "enhancement_tips": []
        }
        
        if quality_score >= 80:
            recommendations["general"].append("⭐ 这是一对优秀的风味搭配,可以直接使用")
        elif quality_score >= 60:
            recommendations["general"].append("✓ 这是一对可行的搭配,需要注意平衡")
        else:
            recommendations["general"].append("⚠️ 这对搭配存在挑战,建议添加第三种食材调和")
        
        if pairing_type["type"] == "harmonious":
            recommendations["ratio"] = "建议比例 1:1,可以等量混合"
            recommendations["techniques"].extend([
                "适合制作奶昔、冰沙等均质产品",
                "可以共同打汁或混合处理",
                "烹饪时可以同步加入"
            ])
        elif pairing_type["type"] == "contrasting":
            recommendations["ratio"] = "建议比例 2:1 或 3:1,让主风味突出"
            recommendations["techniques"].extend([
                "分层处理可以突出差异美感",
                "先后加入以形成风味递进",
                "可以做成双色或分层呈现"
            ])
        else:
            recommendations["ratio"] = "建议比例 1:1 到 2:1 之间,根据口味调整"
            recommendations["techniques"].extend([
                "适合混合制作综合风味产品",
                "可以根据目标调整比例",
                "建议小批量测试找到最佳平衡点"
            ])
        
        if synergies:
            recommendations["enhancement_tips"].append(f"💡 检测到{len(synergies)}个协同效应:")
            for syn in synergies[:3]:
                recommendations["enhancement_tips"].append(
                    f"  • {syn['families_cn'][0]} × {syn['families_cn'][1]} → {syn['effect']}效果"
                )
        
        recommendations["applications"] = self._suggest_applications(item1, item2, pairing_type, quality_score)
        
        return recommendations
    
    def _suggest_applications(self, item1, item2, pairing_type, quality_score):
        """建议应用场景"""
        applications = []
        cat1 = item1.get('category', '').lower()
        cat2 = item2.get('category', '').lower()
        
        if 'fruit' in cat1 or 'fruit' in cat2:
            applications.extend(["果汁或果昔", "水果沙拉", "果酱或果泥"])
        
        if 'vegetable' in cat1 or 'vegetable' in cat2:
            applications.extend(["沙拉或凉拌菜", "蔬菜汁", "炒菜或煮汤"])
        
        if 'herb' in cat1 or 'spice' in cat1 or 'herb' in cat2 or 'spice' in cat2:
            applications.extend(["调味料或香料混合", "腌料或酱汁", "草本茶饮"])
        
        if quality_score >= 80:
            applications.append("高级餐饮创意菜")
        
        return applications[:5]
    
    # ========== 新增方法: 虫洞风格分析 ==========
    
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
        
        # 计算强度评分
        intensity1 = item1.get('molecules_count', 0) * 0.1
        intensity2 = item2.get('molecules_count', 0) * 0.1
        
        # 综合评分
        score1 = complexity1 + intensity1
        score2 = complexity2 + intensity2
        
        # 判断主辅
        if abs(score1 - score2) < 15:
            return {
                "type": "equal",
                "primary": None,
                "secondary": None,
                "ratio": "1:1",
                "description": f"{item1['cn_name']} 与 {item2['cn_name']} 势均力敌,建议等比例使用,形成双主角格局"
            }
        elif score1 > score2:
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


# 测试代码
if __name__ == "__main__":
    print("RecipeDesignConsultant 类已成功定义")
    print("包含以下新方法:")
    print("- analyze_pairing_direction()")
    print("- determine_roles()")
    print("- generate_sensory_curve()")
