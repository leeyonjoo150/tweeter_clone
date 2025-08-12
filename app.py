import streamlit as st
from auth import show_auth_page, logout_user
from user_manager import UserManager
from post_manager import PostManager

# 페이지 설정
st.set_page_config(
    page_title="프롬프트 트위터",
    page_icon="🐦",
    layout="wide"
)

# app.py에서 홈 페이지 부분
def show_home_page(current_user, post_mgr, user_mgr):
    """홈 화면 - 실제 게시글 목록"""
    st.header("📝 최근 프롬프트")

    # 게시글 불러오기
    posts_with_likes = post_mgr.get_posts_with_likes()

    if len(posts_with_likes) == 0:
        st.info("📝 아직 작성된 프롬프트가 없습니다. 첫 번째 프롬프트를 작성해보세요!")
        if st.button("✍️ 글쓰기로 이동"):
            st.session_state.menu = "✍️ 글쓰기"
            st.rerun()
        return

    # 사용자 이름 가져오기 위해 users와 조인
    users_df = user_mgr.load_users()
    posts_display = posts_with_likes.merge(
        users_df[['user_id', 'username']],
        on='user_id',
        how='left'
    )

    # 게시글 하나씩 표시
    for idx, post in posts_display.iterrows():
        with st.container():
            # 프로필 이미지와 정보
            col1, col2 = st.columns([1, 11])

            with col1:
                st.image("https://images.unsplash.com/photo-1743449661678-c22cd73b338a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxmZWF0dXJlZC1waG90b3MtZmVlZHwzfHx8ZW58MHx8fHx8", width=50)

            with col2:
                # 사용자 정보와 액션 버튼
                col_info, col_action = st.columns([8, 4])

                with col_info:
                    time_str = post['timestamp'].split(' ')[1][:5]  # HH:MM 형식
                    st.markdown(f"**{post['username']}** • {time_str}")

                with col_action:
                    # 삭제 버튼 (작성자만)
                    if post['user_id'] == current_user['user_id']:
                        if st.button("🗑️", key=f"del_{post['post_id']}", help="삭제"):
                            if post_mgr.delete_post(post['post_id'], current_user['user_id']):
                                st.success("게시글이 삭제되었습니다!")
                                st.rerun()

                # 게시글 내용
                st.markdown(post['content'])

                # 좋아요 버튼
                is_liked = post_mgr.is_liked_by_user(current_user['user_id'], post['post_id'])
                like_emoji = "❤️" if is_liked else "🤍"
                like_count = int(post['like_count'])

                if st.button(f"{like_emoji} {like_count}", key=f"like_{post['post_id']}"):
                    liked = post_mgr.toggle_like(current_user['user_id'], post['post_id'])
                    if liked:
                        st.success("좋아요!")
                    else:
                        st.info("좋아요 취소")
                    st.rerun()

        st.divider()

def show_write_page(current_user, post_mgr):
    """글쓰기 페이지"""
    st.header("✍️ 새 프롬프트 작성")

    st.markdown("💡 **다른 사람들이 실제로 사용할 수 있는 프롬프트를 공유해보세요!**")

    # 글쓰기 폼
    with st.form("write_form", clear_on_submit=True):
        content = st.text_area(
            "프롬프트 내용",
            placeholder="어떤 상황에서 사용하는 프롬프트인지, 어떻게 사용하는지 자세히 설명해주세요...",
            height=200
        )

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button("🚀 게시하기", type="primary")

        if submitted:
            if content.strip():
                success = post_mgr.create_post(current_user['user_id'], content.strip())

                if success:
                    st.success("프롬프트가 게시되었습니다! 🎉")
                    st.balloons()
                    import time
                    time.sleep(1.5)  # 1.5초 잠시 멈춤
                    st.session_state.menu = "🏠 홈"
                    st.rerun()
                else:
                    st.error("게시 중 오류가 발생했습니다.")
            else:
                st.error("내용을 입력해주세요!")

    st.divider()

    # 프롬프트 작성 가이드
    with st.expander("📝 좋은 프롬프트 작성 팁"):
        st.markdown("""
        **효과적인 프롬프트 작성법:**

        1. **구체적으로 작성하기**
        ```
        ❌ "코딩 도와줘"
        ✅ "파이썬으로 웹 크롤링 코드를 작성해주세요. 에러 처리와 주석도 포함해주세요."
        ```

        2. **사용 상황 설명하기**
        ```
        ✅ "ChatGPT에게 번역을 요청할 때 이 프롬프트를 사용하면 더 자연스러운 번역을 받을 수 있어요."
        ```

        3. **예시 포함하기**
        ```
        ✅ "예시: '안녕하세요'를 영어로 번역해주세요 → Hello! (친근한 인사)"
        ```
        """)

def show_profile_page(current_user, post_mgr, user_mgr):
    """프로필 페이지 - 간단 버전"""
    st.header("👤 내 프로필")

    # 기본 정보
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("https://images.unsplash.com/photo-1743449661678-c22cd73b338a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxmZWF0dXJlZC1waG90b3MtZmVlZHwzfHx8ZW58MHx8fHx8", width=100)

    with col2:
        st.markdown(f"### {current_user['username']}")
        st.markdown(f"**가입일:** {current_user['created_at']}")

    st.divider()

    # 내가 쓴 글 목록
    st.subheader("📝 내가 작성한 프롬프트")

    posts_with_likes = post_mgr.get_posts_with_likes()
    my_posts = posts_with_likes[posts_with_likes['user_id'] == current_user['user_id']]

    if len(my_posts) > 0:
        st.info(f"총 {len(my_posts)}개의 프롬프트를 작성했습니다.")

        for idx, post in my_posts.iterrows():
            with st.container():
                col1, col2 = st.columns([8, 4])

                with col1:
                    # 내용 미리보기 (100자)
                    preview = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
                    st.markdown(f"**{preview}**")
                    st.caption(f"작성: {post['timestamp']} • 좋아요: {int(post['like_count'])}개")

                with col2:
                    if st.button("🗑️ 삭제", key=f"profile_del_{post['post_id']}"):
                        if post_mgr.delete_post(post['post_id'], current_user['user_id']):
                            st.success("삭제되었습니다!")
                            st.rerun()

            st.divider()
    else:
        st.info("📝 아직 작성한 프롬프트가 없습니다.")
        if st.button("✍️ 첫 프롬프트 작성하기"):
            st.session_state.menu = "✍️ 글쓰기"
            st.rerun()

# 매니저 초기화
@st.cache_resource
def init_managers():
    return UserManager(), PostManager()

user_mgr, post_mgr = init_managers()

# Session State 초기화 (새 접속시 자동 로그아웃)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'menu' not in st.session_state:
    st.session_state.menu = "🏠 홈"

# 로그인 체크
if not st.session_state.logged_in:
    # 로그인하지 않은 경우
    show_auth_page()

else:
    # 로그인한 경우 - 메인 앱
    current_user = st.session_state.current_user

    # 헤더
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🐦 프롬프트 트위터")
        st.markdown(f"**{current_user['username']}님 환영합니다!** ✨")
    with col2:
        if st.button("🚪 로그아웃"):
            logout_user()

    # 사이드바 메뉴
    # st.sidebar.title("📋 메뉴")
    # st.sidebar.markdown(f"👤 **{current_user['username']}**")
    # st.sidebar.markdown(f"🆔 {current_user['user_id']}")

    # menu = st.sidebar.selectbox(
    #     "페이지 선택",
    #     ["🏠 홈", "✍️ 글쓰기", "👤 프로필", "📊 데이터 확인"]
    # )

    # 메뉴
    menu = st.sidebar.selectbox(
        "📋 메뉴",
        ["🏠 홈", "✍️ 글쓰기", "👤 프로필"],
        index=["🏠 홈", "✍️ 글쓰기", "👤 프로필"].index(st.session_state.menu)
    )

    # 메뉴 변경 감지
    if menu != st.session_state.menu:
        st.session_state.menu = menu
        st.rerun()

     # 페이지 표시
    if menu == "🏠 홈":
        show_home_page(current_user, post_mgr, user_mgr)
    elif menu == "✍️ 글쓰기":
        show_write_page(current_user, post_mgr)
    elif menu == "👤 프로필":
        show_profile_page(current_user, post_mgr, user_mgr)

    # 메인 콘텐츠
    # if menu == "🏠 홈":
    #     st.header("📝 최근 프롬프트")

    #     # 샘플 게시글 (3단계에서 실제 데이터로 교체)
    #     st.info("💡 3단계에서 실제 게시글 기능이 구현됩니다!")

    #     with st.container():
    #         col1, col2 = st.columns([1, 10])
    #         with col1:
    #             st.image("https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=50&h=50&fit=crop&crop=face", width=50)
    #         with col2:
    #             st.markdown(f"**{current_user['username']}** • 방금 전")
    #             st.markdown("로그인 시스템이 완성되었습니다! 🎉")
    #             st.button("❤️ 0", key="sample_like")

    # elif menu == "✍️ 글쓰기":
    #     st.header("✍️ 새 프롬프트 작성")
    #     st.info("💡 3단계에서 실제 글쓰기 기능이 구현됩니다!")

    #     content = st.text_area("프롬프트 내용", height=150)
    #     if st.button("게시하기", type="primary"):
    #         if content:
    #             st.success("3단계에서 실제 저장 기능이 추가됩니다! 🎉")
    #         else:
    #             st.error("내용을 입력해주세요.")

    # elif menu == "👤 프로필":
    #     st.header("👤 내 프로필")

    #     col1, col2 = st.columns([1, 3])
    #     with col1:
    #         st.image("https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face", width=100)

    #     with col2:
    #         st.markdown(f"### {current_user['username']}")
    #         st.markdown(f"**사용자 ID:** {current_user['user_id']}")
    #         st.markdown(f"**가입일:** {current_user['created_at']}")

    #     st.divider()

    #     # 활동 통계 (더미 데이터)
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         st.metric("작성한 글", "0")
    #     with col2:
    #         st.metric("받은 좋아요", "0")
    #     with col3:
    #         st.metric("활동일", "1")

    # elif menu == "📊 데이터 확인":
    #     st.header("📊 저장된 데이터 확인")

    #     user_mgr = UserManager()
    #     users_df = user_mgr.load_users()

    #     st.subheader("👥 사용자 목록")

    #     if len(users_df) > 0:
    #         # 비밀번호 숨기기
    #         display_df = users_df.copy()
    #         display_df['password'] = '***'
    #         st.dataframe(display_df, use_container_width=True)

    #         # 간단한 통계
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             st.metric("총 사용자 수", len(users_df))
    #         with col2:
    #             today_users = len(users_df[users_df['created_at'] == current_user['created_at']])
    #             st.metric("오늘 가입자", today_users)
    #     else:
    #         st.warning("등록된 사용자가 없습니다.")