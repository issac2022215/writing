"""
LLM 调用封装模块
封装 OpenAI SDK 的流式调用，将错误类型暴露给调用方处理
"""

from openai import OpenAI


def generate_stream(base_url, api_key, model_name, messages):
    """流式调用大语言模型，逐段返回生成内容

    Args:
        base_url: API 端点地址
        api_key: API 密钥
        model_name: 模型名称
        messages: 对话消息列表，格式为 [{'role': ..., 'content': ...}, ...]

    Yields:
        str: 每次返回的文本片段（可能为空字符串）

    Raises:
        openai.AuthenticationError: API Key 无效
        openai.APITimeoutError: 请求超时
        openai.APIError: 其他 API 错误（含余额不足、模型不可用等）
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    stream = client.chat.completions.create(
        model=model_name,
        temperature=1,
        frequency_penalty=1,
        max_tokens=8192,
        stream=True,
        messages=messages,
    )
    for chunk in stream:
        if chunk.choices:
            yield chunk.choices[0].delta.content or ''
