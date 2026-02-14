# 🧪 分子风味配对实验室 (Molecular Flavor Lab)

基于 FlavorDB 分子风味数据库的食材配对灵感引擎。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 项目简介

分子风味配对实验室是一款基于科学数据的食材配对工具。它通过分析食材的分子风味指纹，
帮助用户发现食材之间的隐藏联系，激发烹饪创意。

### 核心功能

- **🔍 智能搜索** - 支持模糊搜索，快速找到目标食材
- **🔄 同味型叠加 (Consonance)** - 寻找共享最多风味分子的稳健搭配
- **⚡ 对比味型 (Contrast)** - 发现跨类别、跨口感的创意搭配
- **🔬 科学解释** - 了解每种搭配背后的分子原理
- **🚫 黑名单过滤** - 排除不想看到的食材
- **🍳 菜谱建议** - AI 生成的创意烹饪建议

## 📊 数据概览

- **食材总数**: 501
- **风味标签**: 590
- **食材类别**: 33
- **数据来源**: [FlavorDB](https://cosylab.iiitd.edu.in/flavordb/)

## 🚀 快速开始

### 安装依赖

```bash
pip install streamlit pandas
```

### 运行应用

```bash
streamlit run app.py
```

### 访问应用

打开浏览器访问: http://localhost:8501

## 🧪 科学原理

### 同味型叠加 (Consonance)

基于共享风味分子的搭配原理。当两种食材含有大量共同的风味化合物时，
它们会产生和谐、协调的味觉体验。

**经典案例**:
- 番茄 + 罗勒 (共享草本、清新风味)
- 草莓 + 巧克力 (共享果香、焦糖风味)
- 牛肉 + 蘑菇 (共享肉香、泥土风味)

### 对比味型 (Contrast)

基于风味互补的搭配原理。不同风味特征的食材通过对比和平衡，
创造出更丰富、更有层次的味觉体验。

**经典案例**:
- 甜味 + 酸味 (如蜂蜜柠檬)
- 油脂 + 酸性 (如奶油柠檬酱)
- 清新 + 温暖 (如薄荷巧克力)

## 📁 项目结构

```
molecular_flavor_lab/
├── app.py                 # 主应用文件
├── flavordb_data.csv      # FlavorDB 数据集
├── README.md             # 项目说明
└── requirements.txt      # 依赖列表
```

## 🛠️ 技术栈

- **Python** - 核心编程语言
- **Streamlit** - Web 应用框架
- **Pandas** - 数据处理
- **集合运算** - 风味相似度计算

## 📝 算法说明

### 相似度计算

使用 **Jaccard 相似度** + **共同风味数量加权**:

```
score = jaccard * 100 + common_count * 0.5

其中:
- jaccard = |A ∩ B| / |A ∪ B|
- common_count = |A ∩ B|
```

### 对比分数计算

```
total_score = contrast_score + category_bonus + intersection_bonus

其中:
- contrast_score: 互补风味匹配数 * 2
- category_bonus: 跨类别 +10, 优先类别 +15
- intersection_bonus: 适度交集 +8
```

## 🌟 使用场景

1. **家庭烹饪** - 发现新的食材搭配，丰富日常菜单
2. **餐厅研发** - 为新菜品寻找灵感
3. **烘焙创作** - 探索甜点风味组合
4. **调酒实验** - 创造独特的鸡尾酒
5. **食品研发** - 新产品风味设计

## 🗺️ 未来规划

- [ ] AI 菜谱生成（接入 LLM）
- [ ] 可视化风味图谱
- [ ] 用户收藏和历史记录
- [ ] 多语言支持
- [ ] 小程序版本
- [ ] 食材替换建议
- [ ] 营养成分分析

## 📚 参考资料

- [FlavorDB: a database of flavor molecules](https://academic.oup.com/nar/article/46/D1/D1210/4559748)
- [Foodpairing](https://www.foodpairing.com/)
- [The Flavor Equation](https://www.amazon.com/Flavor-Equation-Science-Exceptional-Elements/dp/1452182696)

## 📄 许可证

MIT License

## 🙏 致谢

- 数据来源于 FlavorDB
- 灵感来自 Foodpairing 的科学方法

---

<p align="center">
  🧪 分子风味配对实验室 | Molecular Flavor Lab<br>
  <sub>Powered by FlavorDB | Data-driven Ingredient Pairing</sub>
</p>
