"""
侧边栏组件 — API 配置 + 生成参数
"""

import streamlit as st
import config


def render_sidebar():
    """渲染侧边栏，返回配置字典

    Returns:
        dict: {
            'vendor': str,        # 服务商名称
            'base_url': str,      # API 端点
            'model_name': str,    # 模型名称
            'api_key': str,       # API 密钥
            'style': str,         # 文案风格
            'word_count': str,    # 字数范围
            'emoji_level': str,   # emoji 浓度
        }
    """
    st.sidebar.subheader('📡 API 配置')

    vendor = st.sidebar.radio('服务商', ['OpenAI', 'DeepSeek'], key='sidebar_vendor')

    if vendor == 'OpenAI':
        base_url = config.OPENAI_BASE_URL
        model_options = config.OPENAI_MODELS
    else:
        base_url = config.DEEPSEEK_BASE_URL
        model_options = config.DEEPSEEK_MODELS

    model_name = st.sidebar.selectbox('模型', model_options, key='sidebar_model')
    api_key = st.sidebar.text_input('API Key', type='password', key='sidebar_api_key')

    st.sidebar.divider()

    st.sidebar.subheader('⚙️ 生成参数')
    style = st.sidebar.selectbox(
        '风格', config.STYLE_OPTIONS,
        index=config.STYLE_OPTIONS.index(config.DEFAULT_STYLE),
        key='sidebar_style'
    )
    word_count = st.sidebar.radio(
        '字数', list(config.WORD_COUNT_OPTIONS.keys()),
        index=list(config.WORD_COUNT_OPTIONS.keys()).index(config.DEFAULT_WORD_COUNT),
        horizontal=True, key='sidebar_word_count'
    )
    emoji_level = st.sidebar.radio(
        'Emoji', config.EMOJI_LEVEL_OPTIONS,
        index=config.EMOJI_LEVEL_OPTIONS.index(config.DEFAULT_EMOJI_LEVEL),
        horizontal=True, key='sidebar_emoji'
    )

    return {
        'vendor': vendor,
        'base_url': base_url,
        'model_name': model_name,
        'api_key': api_key,
        'style': style,
        'word_count': word_count,
        'emoji_level': emoji_level,
    }
