
# 大模型基准测试数据抓取与展示

## 项目简介

本项目旨在抓取多个大模型基准测试网站的数据，并将其展示在一个前端页面中。项目包括以下功能：
1. 从 Chatbot Arena、AI Benchmark 和 Aider LLM 网站抓取数据。
2. 将抓取的数据转换为 JSON 格式并保存。
3. 在前端页面中展示抓取的数据，支持选项卡切换查看不同来源的数据。
4. 汇总热门基准测试数据并展示。

## 文件结构

- `scrape_data.py`：包含抓取数据的脚本。
- `index.html`：前端页面，用于展示抓取的数据。
- `chatbot_arena_data.json`、`ai_benchmark_data.json`、`aider_llm_data.json`、`popular_benchmark_data.json`：抓取的数据文件。

## 环境依赖

- Python 3.7+
- `crawl4ai` 库
- `openai` 库
- 一个支持异步的 Web 爬虫库（如 `aiohttp`）

## 安装与使用

### 1. 克隆项目

```bash
git clone https://github.com/liugddx/awesome_llm_benchmark.git
cd awesome_llm_benchmark
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 OpenAI API 或者兼容的 API 密钥

在 `scrape_data.py` 文件中，替换 `your key` 为你的 OpenAI API 密钥或者兼容的API密钥。

### 4. 运行数据抓取脚本

```bash
python scrape_data.py
```

### 5. 启动本地服务器查看前端页面

你可以使用任何静态文件服务器来查看 `index.html` 文件

![Chatbot_Arena.png](image/Chatbot_Arena.png)

## 数据展示

前端页面 `index.html` 包含四个选项卡，分别展示从 Chatbot Arena、AI Benchmark、Aider LLM 和热门基准测试汇总抓取的数据。页面加载时会自动抓取并展示最新的数据。
