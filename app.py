import streamlit as st
import time

# 1. 페이지 기본 설정 (배민 감성 타이틀)
st.set_page_config(page_title="배달의민족 - 우리 동네 맛집", page_icon="🛵", layout="centered")

# 2. 배달의민족 브랜드 컬러 및 UI 스타일 적용 (CSS)
st.markdown("""
    <style>
    /* 배민 시그니처 민트색 (#2AC1BC) 적용 */
    :root {
        --baemin-color: #2AC1BC;
    }
    .stApp {
        background-color: #F6F6F6;
    }
    h1, h2, h3 {
        color: #333333;
        font-family: 'BMJUA', sans-serif;
    }
    /* 버튼 스타일 조정 */
    .stButton>button {
        width: 100%;
        background-color: #2AC1BC !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #229A96 !important;
    }
    /* 가게 카드 스타일 */
    .store-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .badge-ready {
        background-color: #E2F6F5;
        color: #2AC1BC;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-preparing {
        background-color: #EEEEEE;
        color: #888888;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 배민 카테고리별 실제 운영 및 입점 예정 데이터 구조
STORES = {
    "족발·보쌈": {
        "가게명": "장인 족발 반반 세트",
        "상태": "OPEN",
        "rating": "⭐ 4.9",
        "tip": "2,000원",
        "menu": [
            {"name": "한돈 온족발 (소)", "price": 29000},
            {"name": "직화 불족발 (소)", "price": 31000},
            {"name": "쟁반막국수", "price": 7000}
        ]
    },
    "돈까스·회·일식": {
        "가게명": "동네 돈카츠 & 연어",
        "상태": "PREPARING",
        "rating": "⭐ -",
        "tip": "-",
        "menu": []
    },
    "고기·구이": {
        "가게명": "삼겹살 배달 전문점",
        "상태": "PREPARING",
        "rating": "⭐ -",
        "tip": "-",
        "menu": []
    },
    "피자·양식": {
        "가게명": "치즈 폭탄 피자 가든",
        "상태": "PREPARING",
        "rating": "⭐ -",
        "tip": "-",
        "menu": []
    },
    "치킨": {
        "가게명": "바삭 후라이드 1988",
        "상태": "PREPARING",
        "rating": "⭐ -",
        "tip": "-",
        "menu": []
    },
    "중식": {
        "가게명": "황금룡 수타 짜장",
        "상태": "PREPARING",
        "rating": "⭐ -",
        "tip": "-",
        "menu": []
    }
}

# 세션 상태 초기화
if "cart" not in st.session_state:
    st.session_state.cart = []
if "order_status" not in st.session_state:
    st.session_state.order_status = None

# --- 메인 화면 레이아웃 ---
st.image("https://images.unsplash.com/photo-1526367790999-0150786486a2?w=500&auto=format&fit=crop&q=60", width=120, caption="배달의민족 대리점")
st.title("배달의민족")
st.write("📍 **의정부시 의정부동** 주변의 맛집 목록입니다.")
st.divider()

# 배민 스타일
