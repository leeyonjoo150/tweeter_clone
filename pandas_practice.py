import pandas as pd
import streamlit as st

def show_pandas_tutorial():
    """pandas CRUD 연습 페이지"""
    st.title("🐼 pandas CRUD 연습")

    # 샘플 데이터
    sample_users = {
        'user_id': ['user_001', 'user_002', 'user_003'],
        'username': ['김개발', '이분석', '박데이터'],
        'password': ['pass1', 'pass2', 'pass3'],
        'created_at': ['2024-08-01', '2024-08-05', '2024-08-10']
    }
    df = pd.DataFrame(sample_users)

    st.subheader("📋 원본 데이터")
    st.dataframe(df)

    # 1. Create (생성)
    st.subheader("➕ CREATE - 데이터 추가")

    new_user = {
        'user_id': 'user_004',
        'username': '신규사용자',
        'password': 'newpass',
        'created_at': '2024-08-11'
    }

    df_with_new = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    st.dataframe(df_with_new)
    st.code("pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)")

    # 2. Read (조회)
    st.subheader("🔍 READ - 데이터 조회")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**특정 사용자 찾기:**")
        user_kim = df[df['username'] == '김개발']
        st.dataframe(user_kim)
        st.code("df[df['username'] == '김개발']")

    with col2:
        st.write("**최근 가입자 찾기:**")
        recent_users = df[df['created_at'] >= '2024-08-05']
        st.dataframe(recent_users)
        st.code("df[df['created_at'] >= '2024-08-05']")

    # 3. Update (수정)
    st.subheader("✏️ UPDATE - 데이터 수정")

    df_updated = df.copy()
    df_updated.loc[df_updated['username'] == '김개발', 'password'] = 'newpass123'

    col1, col2 = st.columns(2)
    with col1:
        st.write("**수정 전:**")
        st.dataframe(df[['username', 'password']])
    with col2:
        st.write("**수정 후:**")
        st.dataframe(df_updated[['username', 'password']])

    st.code("df.loc[df['username'] == '김개발', 'password'] = 'newpass123'")

    # 4. Delete (삭제)
    st.subheader("🗑️ DELETE - 데이터 삭제")

    df_deleted = df[df['username'] != '이분석']  # 이분석 제외

    col1, col2 = st.columns(2)
    with col1:
        st.write("**삭제 전:**")
        st.dataframe(df)
    with col2:
        st.write("**삭제 후:**")
        st.dataframe(df_deleted)

    st.code("df_new = df[df['username'] != '이분석']")

if __name__ == "__main__":
    show_pandas_tutorial()