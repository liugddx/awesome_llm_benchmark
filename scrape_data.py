import asyncio
import json
import re
from crawl4ai import AsyncWebCrawler
from openai import OpenAI

async def extract_markdown_to_json(markdown_data: str, prompt: str = None) -> dict:
    """
    利用大模型将 markdown 数据转换为 JSON 格式。
    如果不传入 prompt，则使用默认的提词：
    "请将以下的 markdown 数据转换为有效的 JSON 格式，要求只输出 JSON 数据，并尽可能完整地保留所有关键信息。"
    """
    if prompt is None:
        prompt = (
            "请将以下的 markdown 中的table取出来并转换为有效的 JSON 格式，如果上下文不够则压缩json,如果json超过10条则返回10条"
            "要求只输出 JSON 数据，格式为`[{}]`,并尽可能完整地保留所有关键信息。"
        )
    full_prompt = f"{prompt}\n\nMarkdown:\n{markdown_data}"

    # openai API 调用为同步接口，此处借助 run_in_executor 转换为异步调用
    loop = asyncio.get_event_loop()
    client = OpenAI(
        api_key='your key',
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model="deepseek-r1-250120",
            messages=[
                {"role": "system", "content": "你是一个提取并转换数据的助手，请严格按照要求只输出 JSON。"},
                {"role": "user", "content": full_prompt},
            ],
            temperature=0,
        )
    )

    # 从返回结果中提取消息内容（注意使用 .content 而非下标访问）
    text = response.choices[0].message.content.strip()

    # 处理返回的 JSON 被代码块格式包裹的问题
    # 移除起始的 ```json 和结尾的 ```
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except Exception as e:
        # 若转换失败，则返回错误信息及大模型返回的原始文本
        data = {"error": f"JSON解析失败：{e}", "raw_output": text}
    return data


async def scrape_chatbot_arena():
    url = "https://web.lmarena.ai/leaderboard"
    async with AsyncWebCrawler() as crawler:
        print("正在抓取 Chatbot Arena 数据...")
        result = await crawler.arun(url=url)
        markdown_data = result.markdown
        json_data = await extract_markdown_to_json(markdown_data)
        with open(f"chatbot_arena_data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print("Chatbot Arena 数据抓取完成，并已保存为 chatbot_arena_data.json")


async def scrape_ai_benchmark():
    url = "https://openlm.ai/chatbot-arena/"
    async with AsyncWebCrawler() as crawler:
        print("正在抓取 AI Benchmark 数据...")
        result = await crawler.arun(url=url)
        markdown_data = result.markdown
        json_data = await extract_markdown_to_json(markdown_data)
        with open(f"ai_benchmark_data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print("AI Benchmark 数据抓取完成，并已保存为 ai_benchmark_data.json")


async def scrape_aider_llm():
    url = "https://aider.chat/docs/leaderboards/"
    async with AsyncWebCrawler() as crawler:
        print("正在抓取 Aider LLM 数据...")
        result = await crawler.arun(url=url)
        markdown_data = result.markdown
        json_data = await extract_markdown_to_json(markdown_data)

        with open(f"aider_llm_data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print("Aider LLM 数据抓取完成，并已保存为 aider_llm_data.json")


async def main():

    await scrape_chatbot_arena()
    await scrape_ai_benchmark()
    await scrape_aider_llm()
    print("所有数据抓取完成。")


if __name__ == "__main__":
    from datetime import datetime
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')
    # 创建 文件夹 按照日期
    import os
    if not os.path.exists(formatted_date):
        os.makedirs(formatted_date)
    asyncio.run(main())