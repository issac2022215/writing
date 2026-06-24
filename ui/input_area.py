"""
输入区域组件
"""

import streamlit as st


def render_input_area():
    """渲染主区域输入行，返回关键词和按钮点击状态

    Returns:
        tuple[str, bool]: (keyword, button_clicked)
    """
    st.write('## 小红书爆款文案生成器')

    col1, col2 = st.columns([4, 1])
    with col1:
        keyword = st.text_input('请输入文案关键词：', key='input_keyword')
    with col2:
        button = st.button('✨ 生成', type='primary', key='input_generate_btn')

    # 最近关键词快捷回看标签
    recent = st.session_state.get('recent_keywords', [])
    if recent:
        st.caption('最近搜索：')
        tag_cols = st.columns(len(recent))
        for i, kw in enumerate(recent):
            with tag_cols[i]:
                if st.button(kw, key=f'recent_tag_{i}', use_container_width=True):
                    st.session_state.input_keyword = kw
                    st.rerun()

    return keyword, button
