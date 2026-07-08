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
        margin-bottom: 15px;
    }
    .badge-ready {
        background-color: #E2F6F5;
        color: #2AC1BC;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-preparing {
        background-color: #EEEEEE;
        color: #888888;
        padding: 4px 8px;
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
# 에러 유발 가능성이 있는 외부 이미지 주소를 제거하고 깔끔한 타이틀로 대체했습니다.
st.markdown("<h1 style='color: #2AC1BC; font-size: 40px; margin-bottom: 0px;'>🛵 배달의민족</h1>", unsafe_allow_html=True)
st.write("📍 **의정부시 의정부동** 주변의 맛집 목록입니다.")
st.divider()

# 배민 스타일 카테고리 탭 구성
st.subheader("오늘 어떤 메뉴가 당기시나요? 🍕")
tabs = st.tabs(list(STORES.keys()))

for i, category in enumerate(STORES.keys()):
    with tabs[i]:
        store_info = STORES[category]
        
        # 입점 예정인 가게 디자인 처리
        if store_info["상태"] == "PREPARING":
            st.markdown(f"""
            <div class="store-card">
                <span class="badge-preparing">⏱️ 입점 예정</span>
                <h3 style='margin: 5px 0; color: #333333;'>{store_info['가게명']}</h3>
                <p style='color: #888888; font-size: 14px; margin: 0;'>현재 서비스 준비 중인 매장입니다. 조금만 기다려주세요!</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 현재 이용 가능한 유일한 테스트 매장
        else:
            st.markdown(f"""
            <div class="store-card">
                <span class="badge-ready">● 주문 가능</span>
                <h3 style='margin: 5px 0; color: #333333;'>{store_info['가게명']}</h3>
                <p style='margin: 0; font-size: 14px; color: #555555;'>평점: {store_info['rating']} | 배달팁: {store_info['tip']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("👇 **아래 메뉴를 장바구니에 담아 테스트해보세요!**")
            
            # 메뉴 목록 출력 및 장바구니 담기
            for menu in store_info["menu"]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{menu['name']}**")
                    st.write(f"{menu['price']:,}원")
                with col2:
                    if st.button("담기", key=f"add_{menu['name']}"):
                        st.session_state.cart.append(menu)
                        st.toast(f"🛒 장바구니에 {menu['name']} 추가!")
                st.divider()

# 사이드바 - 배민 장바구니 UI
with st.sidebar:
    st.header("🛒 배민 장바구니")
    
    if not st.session_state.cart:
        st.write("장바구니가 비어 있습니다.")
    else:
        total_price = 0
        for item in st.session_state.cart:
            st.write(f"• {item['name']} ({item['price']:,}원)")
            total_price += item['price']
            
        st.divider()
        st.subheader(f"총 결제금액: {total_price:,}원")
        
        if st.button("🛵 배달 주문하기", type="primary"):
            st.session_state.order_status = "접수 완료"
            st.session_state.cart = []
            st.rerun()

# 실시간 배달 애니메이션
if st.session_state.order_status:
    st.balloons()
    st.success("주문이 성공적으로 접수되었습니다!")
    
    status_area = st.empty()
    progress = st.progress(0)
    
    steps = [
        ("👨‍🍳 가게에서 맛있는 음식을 조리하고 있어요!", 30),
        ("🛵 라이더가 음식을 픽업하여 이웃님께 출발했습니다!", 70),
        ("🔔 딩동! 배달이 완료되었습니다. 맛있게 드세요! 🎉", 100)
    ]
    
    for text, percent in steps:
        status_area.markdown(f"### 배민 실시간 현황\n**{text}**")
        progress.progress(percent)
        time.sleep(2)
        
    if st.button("추가 주문하기"):
        st.session_state.order_status = None
        st.rerun()
