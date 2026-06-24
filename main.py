"""
小红书爆款文案生成器 — Streamlit 应用入口
"""

import streamlit as st
from openai import AuthenticationError, APITimeoutError, APIError

import config
from prompts import build_system_prompt
from generator import generate_stream

# ── 页面配置 ────────────────────────────────────────

st.set_page_config(page_title='小红书爆款文案生成器', page_icon='🔥', layout='centered')

# ── 按钮样式微调 ────────────────────────────────────

st.markdown(
    """
    <style>
    .stButton > button { margin-top: 27px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ── 侧边栏：API 配置 ────────────────────────────────

with st.sidebar:
    st.subheader('📡 API 配置')
    vendor = st.radio('服务商', ['OpenAI', 'DeepSeek'], key='vendor')

    if vendor == 'OpenAI':
        base_url = config.OPENAI_BASE_URL
        model_options = config.OPENAI_MODELS
    else:
        base_url = config.DEEPSEEK_BASE_URL
        model_options = config.DEEPSEEK_MODELS

    model_name = st.selectbox('模型', model_options, key='model')
    api_key = st.text_input('API Key', type='password', key='api_key')

    st.divider()

    st.subheader('⚙️ 生成参数')
    style = st.selectbox('风格', config.STYLE_OPTIONS,
                         index=config.STYLE_OPTIONS.index(config.DEFAULT_STYLE), key='style')
    word_count = st.radio('字数', list(config.WORD_COUNT_OPTIONS.keys()),
                          index=list(config.WORD_COUNT_OPTIONS.keys()).index(config.DEFAULT_WORD_COUNT),
                          horizontal=True, key='word_count')
    emoji_level = st.radio('Emoji', config.EMOJI_LEVEL_OPTIONS,
                           index=config.EMOJI_LEVEL_OPTIONS.index(config.DEFAULT_EMOJI_LEVEL),
                           horizontal=True, key='emoji_level')

# ── 主区域：输入区 ──────────────────────────────────

st.write('## 小红书爆款文案生成器')
col1, col2 = st.columns([4, 1])
with col1:
    keyword = st.text_input('请输入文案关键词：', key='keyword')
with col2:
    generate_btn = st.button('✨ 生成', type='primary', key='generate_btn')

# ── API Key 校验 ────────────────────────────────────

if not api_key:
    st.error('请提供访问大模型需要的 API Key！！！')
    st.stop()

# ── 生成逻辑 ────────────────────────────────────────

if generate_btn and keyword.strip():
    system_prompt = build_system_prompt(style, word_count, emoji_level)
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': keyword},
    ]

    try:
        st.markdown('---')
        gen = generate_stream(base_url, api_key, model_name, messages)
        output = st.write_stream(gen)
        if output:
            st.markdown('---')
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.download_button(
                    '📋 下载文案', output, file_name=f'{keyword}_文案.md',
                    mime='text/markdown', key='download_btn', use_container_width=True
                )
    except AuthenticationError:
        st.error('API Key 校验失败，请检查是否正确填写')
    except APITimeoutError:
        st.error('请求超时，请检查网络连接后重试')
    except APIError as e:
        status_code = getattr(e, 'status_code', None)
        if status_code == 429:
            st.error('API 额度可能已用完，请检查账户余额')
        elif status_code == 404:
            st.error('所选模型当前不可用，请尝试切换其他模型')
        else:
            st.error(f'调用大模型时出错：{e}')
    except Exception as e:
        st.warning(f'生成过程中出现异常：{e}')
