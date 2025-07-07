# 🏆 Contestant Scoring and Ranking System
## 选手评分排名系统

A modern web-based contestant scoring and ranking system built with Streamlit. This system allows judges to score contestants and automatically calculates rankings based on the scoring rules.

基于Streamlit构建的现代化选手评分排名系统，支持评委打分和自动排名计算。

## ✨ Features | 功能特点

- 🏃‍♂️ **Contestant Management** | 选手信息管理
- 🎯 **Multi-Judge Scoring** | 多评委评分系统  
- 📊 **Automatic Score Calculation** | 自动得分计算
- 🏆 **Real-time Rankings** | 实时排名显示
- 💾 **JSON Data Storage** | JSON数据持久化
- 🎨 **Modern UI Design** | 现代化界面设计

## 🎮 Demo | 演示

![System Interface](https://img.shields.io/badge/Status-Running-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Python](https://img.shields.io/badge/Python-3.7+-blue)

## 🚀 Quick Start | 快速开始

### Prerequisites | 环境要求
- Python 3.7+
- pip package manager

### Installation | 安装

1. **Clone the repository | 克隆仓库**
   ```bash
   git clone https://github.com/yy13213/score.git
   cd score
   ```

2. **Install dependencies | 安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application | 运行应用**
   ```bash
   streamlit run main.py
   ```

4. **Access the system | 访问系统**
   
   Open your browser and navigate to: `http://localhost:8501`
   
   在浏览器中打开：`http://localhost:8501`

## 📋 How to Use | 使用方法

### Step 1: Add Contestants | 第一步：添加选手
- Click "1️⃣ 选手信息录入" (Contestant Information Input)
- Enter contestant name and phone number
- Save the information

### Step 2: Input Scores | 第二步：录入分数  
- Click "2️⃣ 评委分数录入" (Judge Score Input)
- Select a contestant from the dropdown
- Enter scores from 10 judges (0-100 points each)
- Save the scores

### Step 3: View Scores | 第三步：查看得分
- Click "3️⃣ 选手得分" (Contestant Scores)
- View detailed scoring information for each contestant

### Step 4: Check Rankings | 第四步：查看排名
- Click "4️⃣ 选手排名" (Contestant Rankings)  
- View the final rankings with medal indicators

## 🎯 Scoring Rules | 评分规则

- Each contestant is scored by **10 judges**
- Score range: **0-100 points**
- Final score calculation: **Remove highest and lowest scores, then calculate average of remaining 8 scores**
- Rankings are sorted by final scores in **descending order**

每位选手由10位评委评分，分数范围0-100分。最终得分计算方法：去掉一个最高分和一个最低分，计算剩余8个分数的平均值。

## 📁 Project Structure | 项目结构

```
score/
├── main.py              # Main application file | 主应用程序
├── data_manager.py      # Data management module | 数据管理模块  
├── requirements.txt     # Dependencies | 依赖包列表
├── contestants.json     # Contestant data (generated) | 选手数据
├── scores.json          # Score data (generated) | 评分数据
├── README.md           # Project documentation | 项目说明
└── 使用说明.md         # Chinese user manual | 中文使用说明
```

## 🛠️ Technical Stack | 技术栈

- **Frontend**: Streamlit
- **Data Processing**: Pandas  
- **Data Storage**: JSON
- **Language**: Python 3.7+

## 📱 Screenshots | 界面截图

The system features a modern, responsive design with:
- 🎨 Clean and intuitive interface
- 📊 Real-time data visualization
- 🏆 Beautiful ranking displays with medal indicators
- 📱 Mobile-friendly responsive layout

系统具有现代化响应式设计，包含直观界面、实时数据可视化和精美的排名显示。

## 🤝 Contributing | 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献代码！请随时提交Pull Request。

## 📄 License | 许可证

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact | 联系方式

If you have any questions or suggestions, please feel free to reach out!

如有任何问题或建议，请随时联系！

---

⭐ **Star this repository if you find it helpful!** | **如果您觉得有用，请给个星标！** 