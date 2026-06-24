"""
结果展示组件 — 渲染生成结果及操作按钮
"""

import streamlit as st
import storage


def render_result(keyword, content, style, word_count, emoji_level, model_name):
    """渲染生成结果，包含复制和下载功能

    Args:
        keyword: 关键词
        content: 生成的完整 markdown 内容
        style: 风格参数
        word_count: 字数参数
        emoji_level: emoji 浓度参数
        model_name: 使用的模型
    """
    if not content:
        return

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
            key=f'dl_{hash(content)}',
            use_container_width=True,
        )

    # 复制 — 用 st.code 提供自带复制按钮的代码块
    with col2:
        st.download_button(
            '📋 复制（下载TXT）', content,
            file_name=f'{keyword}_文案.txt',
            mime='text/plain',
            key=f'copy_{hash(content)}',
            use_container_width=True,
        )

    # 收藏按钮
    with col3:
        if f'fav_saved_{hash(content)}' not in st.session_state:
            st.session_state[f'fav_saved_{hash(content)}'] = False

        if st.button('⭐ 收藏', key=f'fav_{hash(content)}', use_container_width=True):
            # 解析标题
            titles = _extract_titles(content)
            rid = storage.save(keyword, titles, content, style, word_count, emoji_level, model_name)
            storage.toggle_favorite(rid)
            st.session_state[f'fav_saved_{hash(content)}'] = True
            st.toast('已收藏！可在侧边栏历史中查看', icon='⭐')

    if st.session_state.get(f'fav_saved_{hash(content)}', False):
        st.success('⭐ 已加入收藏')


def _extract_titles(content):
    """从 markdown 内容中提取标题列表"""
    titles = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped and stripped[0].isdigit() and '. ' in stripped[:4]:
            titles.append(stripped.split('. ', 1)[1])
    return titles if titles else ['标题提取失败']
