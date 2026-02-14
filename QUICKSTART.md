# 🚀 快速开始指南

## 方式一：本地运行（推荐）

### 步骤 1：准备环境

确保已安装 Python 3.9+：

```bash
python --version
```

### 步骤 2：创建项目文件夹

```bash
mkdir molecular-flavor-lab
cd molecular-flavor-lab
```

### 步骤 3：下载项目文件

从 `/mnt/okcomputer/output/molecular_flavor_lab/` 下载以下文件：

- `app.py` - 主应用
- `flavordb_data.csv` - 数据集
- `requirements.txt` - 依赖列表

### 步骤 4：安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# Windows 激活
venv\Scripts\activate

# Mac/Linux 激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 5：运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

---

## 方式二：Docker 运行

### 创建 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### 构建并运行

```bash
docker build -t molecular-flavor-lab .
docker run -p 8501:8501 molecular-flavor-lab
```

---

## 方式三：Streamlit Cloud 部署（免费）

### 步骤 1：推送到 Github

```bash
# 初始化仓库
git init

# 添加文件
git add .
git commit -m "Initial commit"

# 在 Github 创建新仓库，然后关联
git remote add origin https://github.com/YOUR_USERNAME/molecular-flavor-lab.git
git branch -M main
git push -u origin main
```

### 步骤 2：部署到 Streamlit Cloud

1. 访问 https://streamlit.io/cloud
2. 用 Github 账号登录
3. 点击 "New App"
4. 选择你的仓库
5. 主文件路径填 `app.py`
6. 点击 Deploy

**免费额度：** 1GB 存储 + 1GB 内存

---

## 常见问题

### Q1: 提示 "ModuleNotFoundError"

**解决：** 确保在虚拟环境中安装依赖

```bash
# 重新激活环境
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 重新安装
pip install -r requirements.txt
```

### Q2: 端口被占用

**解决：** 指定其他端口

```bash
streamlit run app.py --server.port 8502
```

### Q3: 数据文件找不到

**解决：** 确保 `flavordb_data.csv` 和 `app.py` 在同一目录

```bash
ls -la
# 应该看到 app.py 和 flavordb_data.csv
```

### Q4: 如何更新数据

**解决：** 替换 `flavordb_data.csv` 文件，保持相同格式

---

## 项目结构

```
molecular-flavor-lab/
├── app.py              # 主应用（必须）
├── flavordb_data.csv   # 数据集（必须）
├── requirements.txt    # 依赖（必须）
├── README.md          # 说明文档
├── SCORING_SYSTEM.md  # 评分系统说明
└── venv/              # 虚拟环境（自动生成）
```

---

## 下一步

1. ✅ 本地运行成功
2. 🎨 自定义 UI 样式（修改 app.py 中的 CSS）
3. 🔧 调整评分参数（修改算法权重）
4. 📊 添加更多数据（扩展 CSV 文件）
5. 🚀 部署上线（Streamlit Cloud / 自有服务器）

---

## 需要帮助？

- 📖 查看 `README.md` 了解项目详情
- 📊 查看 `SCORING_SYSTEM.md` 了解评分算法
- 🐛 提交 Issue 到 Github

---

<p align="center">
🧪 分子风味配对实验室 | Molecular Flavor Lab<br>
<sub>让科学指导烹饪</sub>
</p>
