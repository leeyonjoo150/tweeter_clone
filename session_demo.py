import streamlit as st

st.title("🧠 Session State 체험")

# 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 로그인 전 화면
if not st.session_state.logged_in:
    st.write("로그인이 필요합니다.")

    username = st.text_input("사용자명")

    if st.button("로그인"):
        if username:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.rerun()  # 페이지 새로고침
        else:
            st.error("사용자명을 입력하세요!")

# 로그인 후 화면
else:
    st.success(f"✅ {st.session_state.current_user}님 환영합니다!")

    if st.button("로그아웃"):
        st.session_state.logged_in = False
        del st.session_state.current_user
        st.rerun()