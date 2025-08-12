import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="프롬프트 트위터",
    page_icon="🐦",
    layout="wide"
)

# 헤더 영역
st.title("🐦 프롬프트 트위터 v1.1")  # 버전 추가
st.markdown("**유용한 LLM 프롬프트를 공유하는 공간입니다** ✨")  # 이모지 추가

# 사이드바 - 네비게이션
st.sidebar.title("📋 메뉴")
menu = st.sidebar.selectbox(
    "선택하세요",
    ["🏠 홈", "✍️ 글쓰기", "👤 프로필"]
)

# 메인 영역
if menu == "🏠 홈":
    st.header("📝 최근 프롬프트")

    # 샘플 데이터로 게시글 목록 표시
    sample_posts = [
        {
            "user": "AI마스터",
            "content": "ChatGPT로 코딩할 때 이 프롬프트를 쓰면 정말 좋아요!\n\n'다음 코드를 파이썬으로 작성해주세요. 주석도 자세히 달아주시고, 예외처리도 포함해주세요.'",
            "time": "2분 전",
            "likes": 15
        },
        {
            "user": "프롬프트러",
            "content": "번역 프롬프트 공유합니다.\n\n'다음 문장을 자연스러운 한국어로 번역해주세요. 문화적 맥락을 고려해서 의역해도 좋습니다.'",
            "time": "10분 전",
            "likes": 8
        },
        {
            "user": "데이터분석가",
            "content": "데이터 분석 프롬프트 추천!\n\n'이 데이터를 분석해서 인사이트 3가지만 간단히 정리해주세요. 시각화 코드도 파이썬으로 작성해주세요.'",
            "time": "1시간 전",
            "likes": 23
        }
    ]

    # 게시글 표시
    for post in sample_posts:
        with st.container():
            col1, col2 = st.columns([1, 10])

            with col1:
                st.image("https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=50&h=50&fit=crop&crop=face", width=50)

            with col2:
                st.markdown(f"**{post['user']}** • {post['time']}")
                st.markdown(post['content'])

                # 좋아요 버튼 (기능 없이 UI만)
                col_like, col_share = st.columns([1, 8])
                with col_like:
                    st.button(f"❤️ {post['likes']}", key=f"like_{post['user']}")

        st.divider()

elif menu == "✍️ 글쓰기":
    st.header("✍️ 새 프롬프트 작성")

    # 글쓰기 폼
    with st.form("post_form"):
        content = st.text_area(
            "프롬프트를 공유해주세요!",
            placeholder="어떤 상황에서 사용하는 프롬프트인지, 어떤 점이 좋은지 설명해주세요...",
            height=150
        )

        category = st.selectbox(
            "카테고리",
            ["💻 코딩", "📝 글쓰기", "🌍 번역", "📊 데이터분석", "🎨 창작", "📚 학습", "기타"]
        )

        submitted = st.form_submit_button("게시하기", type="primary")

        if submitted:
            if content:
                st.success("프롬프트가 게시되었습니다! 🎉")
                st.balloons()  # 재미있는 효과
            else:
                st.error("내용을 입력해주세요!")

elif menu == "👤 프로필":
    st.header("👤 내 프로필")

    # 프로필 정보 (더미 데이터)
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face", width=100)

    with col2:
        st.markdown("### AI마스터")
        st.markdown("**가입일:** 2024년 1월")
        st.markdown("**작성한 프롬프트:** 12개")
        st.markdown("**받은 좋아요:** 156개")

    st.divider()

    st.subheader("📝 내가 작성한 프롬프트")
    st.info("아직 작성한 프롬프트가 없습니다.")