"""
小红书爆款文案生成器 — Streamlit 应用入口
"""

import streamlit as st
from openai import AuthenticationError, APITimeoutError, APIError

from prompts import build_system_prompt
from generator import generate_stream
from ui.sidebar import render_sidebar
from ui.input_area import render_input_area
from ui.result_area import render_result
import storage

# ── 页面配置 ────────────────────────────────────────

st.set_page_config(page_title='小红书爆款文案生成器', page_icon='🔥', layout='centered')

# ── 按钮样式 ────────────────────────────────────────

st.markdown(
    """
    <style>
    .stButton > button { margin-top: 27px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ── 侧边栏 ──────────────────────────────────────────

sidebar_config = render_sidebar()

# ── 侧边栏：历史记录 ────────────────────────────────

with st.sidebar:
    st.divider()
    st.subheader('📋 历史记录')

    history_search = st.text_input('搜索历史...', key='history_search', placeholder='按关键词搜索')
    records = storage.search(history_search, limit=30)

    if not records:
        st.caption('暂无历史记录')
    else:
        for rec in records:
            fav_icon = '⭐ ' if rec['is_favorite'] else ''
            label = f"{fav_icon}{rec['keyword']}"
            col_rec, col_del = st.columns([5, 1])
            with col_rec:
                if st.button(label, key=f'hist_{rec["id"]}', use_container_width=True):
                    st.session_state['viewing_history'] = rec
            with col_del:
                if st.button('🗑', key=f'del_{rec["id"]}'):
                    storage.delete(rec['id'])
                    st.rerun()

# ── 主区域 ──────────────────────────────────────────

keyword, generate_btn = render_input_area()

# 查看历史记录
if 'viewing_history' in st.session_state and st.session_state.viewing_history:
    rec = st.session_state.viewing_history
    st.markdown('---')
    st.info(f'📖 正在查看历史记录：**{rec["keyword"]}**（{rec["created_at"]}）')
    st.markdown(rec['content'])
    if st.button('❌ 关闭', key='close_history'):
        del st.session_state['viewing_history']
        st.rerun()
    st.stop()

# API Key 校验
if not sidebar_config['api_key']:
    st.error('请提供访问大模型需要的 API Key！！！')
    st.stop()

# ── 生成逻辑 ────────────────────────────────────────

if generate_btn and keyword.strip():
    system_prompt = build_system_prompt(
        sidebar_config['style'],
        sidebar_config['word_count'],
        sidebar_config['emoji_level'],
    )
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': keyword},
    ]

    try:
        gen = generate_stream(
            sidebar_config['base_url'],
            sidebar_config['api_key'],
            sidebar_config['model_name'],
            messages,
        )
        output_parts = []

        def _tracked_gen():
            for chunk in gen:
                output_parts.append(chunk)
                yield chunk

        output = st.write_stream(_tracked_gen())

        if output:
            # 自动保存到历史
            from ui.result_area import extract_titles
            titles = extract_titles(output)
            record_id = storage.save(
                keyword, titles, output,
                sidebar_config['style'],
                sidebar_config['word_count'],
                sidebar_config['emoji_level'],
                sidebar_config['model_name'],
            )
            # 更新最近关键词列表（用于快捷回看）
            if 'recent_keywords' not in st.session_state:
                st.session_state.recent_keywords = []
            if keyword not in st.session_state.recent_keywords:
                st.session_state.recent_keywords.insert(0, keyword)
                st.session_state.recent_keywords = st.session_state.recent_keywords[:6]

            # 渲染结果操作区
            render_result(
                keyword, output,
                sidebar_config['style'],
                sidebar_config['word_count'],
                sidebar_config['emoji_level'],
                sidebar_config['model_name'],
                record_id=record_id,
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
        # 流式中断 — 已累积的内容仍然显示给用户
        if 'output_parts' in locals() and output_parts:
            st.markdown(''.join(output_parts))
        st.warning(f'生成过程中出现异常：{e}')
