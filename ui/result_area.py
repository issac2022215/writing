"""
结果展示组件 — 渲染生成结果及操作按钮
"""

import streamlit as st
import storage


def render_result(keyword, content, style, word_count, emoji_level, model_name, record_id: int = 0):
    """渲染生成结果，包含复制和下载功能

    Args:
        keyword: 关键词
        content: 生成的完整 markdown 内容
        style: 风格参数
        word_count: 字数参数
        emoji_level: emoji 浓度参数
        model_name: 使用的模型
        record_id: 已自动保存的记录 id，收藏按钮直接切换收藏状态
    """
    if not content:
        return

    # 使用 session_state 计数器生成唯一 widget key，避免 hash() 跨会话不稳定
    if '_widget_counter' not in st.session_state:
        st.session_state._widget_counter = 0
    st.session_state._widget_counter += 1
    widget_key = str(st.session_state._widget_counter)

    st.markdown('---')
    st.markdown(content)
    st.markdown('---')

    col1, col2, col3 = st.columns(3)

    # 下载按钮
    with col1:
        st.download_button(
            '📥 下载', content,
            file_name=f'{keyword}_文案.md',
            mime='text/markdown',
            key=f'dl_{widget_key}',
            use_container_width=True,
        )

    # 复制 — 用 st.code 提供自带复制按钮的代码块
    with col2:
        st.download_button(
            '📋 复制（下载TXT）', content,
            file_name=f'{keyword}_文案.txt',
            mime='text/plain',
            key=f'copy_{widget_key}',
            use_container_width=True,
        )

    # 收藏按钮（不重复保存，直接切换已保存记录的收藏状态）
    with col3:
        if record_id > 0:
            if st.button('⭐ 收藏', key=f'fav_{widget_key}', use_container_width=True):
                storage.toggle_favorite(record_id)
                st.toast('已收藏！可在侧边栏历史中查看', icon='⭐')
        else:
            # 兼容无 record_id 的场景（极少发生）
            if st.button('⭐ 收藏', key=f'fav_{widget_key}', use_container_width=True):
                titles = extract_titles(content)
                rid = storage.save(keyword, titles, content, style, word_count, emoji_level, model_name)
                storage.toggle_favorite(rid)
                st.toast('已收藏！可在侧边栏历史中查看', icon='⭐')


def extract_titles(content):
    """从 markdown 内容中提取标题列表"""
    titles = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped and stripped[0].isdigit() and '. ' in stripped[:4]:
            titles.append(stripped.split('. ', 1)[1])
    return titles if titles else ['标题提取失败']
