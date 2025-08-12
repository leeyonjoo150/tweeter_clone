# tweeter_clone
# 🐦 프롬프트 트위터

LLM 프롬프트를 공유하는 트위터 클론 웹 애플리케이션

## 🚀 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py

**업데이트 및 푸시**

```bash
git add README.md
git commit -m "📝 Add README with project description"
git push

"""
📁 data/
├── users.csv    → 사용자 정보
├── posts.csv    → 게시글 정보
└── likes.csv    → 좋아요 정보

🔗 관계:
- posts.user_id → users.user_id (누가 썼는지)
- likes.post_id → posts.post_id (어떤 글에)
- likes.user_id → users.user_id (누가 좋아요했는지)
"""

# posts.csv
"""
post_id,user_id,content,timestamp
post_001,user_001,"ChatGPT 코딩 팁...",2024-08-11 14:30:00
post_002,user_002,"번역 프롬프트 공유",2024-08-11 15:45:00
"""

# likes.csv
"""
like_id,user_id,post_id,timestamp
like_001,user_002,post_001,2024-08-11 14:32:00
like_002,user_001,post_002,2024-08-11 15:50:00
"""