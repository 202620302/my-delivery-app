import streamlit as st
import time

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(page_title="방구석 배달앱", page_icon="🛵", layout="centered")

# 간단한 CSS로 앱 느낌 내기
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; }
    .css-118g743 { background-color: #f7f9fa; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 세팅 (음식점 및 메뉴)
RESTAURANTS = {
    "네오 피자": [
        {"name": "콤비네이션 피자", "price": 18000},
        {"name": "치즈 오븐 파스타", "price": 7000},
        {"name": "페퍼로니 피자", "price": 19000}
    ],
    "상큼 치킨": [
        {"name": "후라이드 치킨", "price": 17000},
        {"name": "양념 치킨", "price": 18000},
        {"name": "간장 치킨", "price": 18500}
    ],
    "마라 신공": [
        {"name": "마라탕 (기본)", "price": 12000},
        {"name": "꿔바로우", "price": 15000}
    ]
}

# 3. 세션 상태(State) 초기화 - 웹 페이지가 새로고침되어도 데이터 유지 목적
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_store" not in st.session_state:
    st.session_state.current_store = list(RESTAURANTS.keys())[0]
if "order_status" not in st.session_state:
    st.session_state.order_status = None

# 4. 웹 화면 레이아웃 구성
st.title("🛵 방구석 배달 사이트 Prototype")
st.caption("파이썬으로 구현한 초간단 배달 웹 서비스입니다.")

# 카테고리 / 음식점 선택
st.subheader("🏪 어떤 맛집에서 주문할까요?")
selected_store = st.selectbox("가게를 선택하세요", list(RESTAURANTS.keys()))

# 다른 가게를 선택하면 장바구니 초기화 방지 및 현재 가게 업데이트
if selected_store != st.session_state.current_store:
    st.session_state.current_store = selected_store
    st.session_state.cart = []  # 배달앱 특성상 가게가 바뀌면 장바구니를 비움
    st.toast(f"'{selected_store}'로 가게를 변경하여 장바구니가 비워졌습니다.")

# 메뉴판 출력 및 담기 기능 (⚠️ 이 부분의 오타를 수정했습니다!)
st.markdown(f"### 🧾 [{st.session_state.current_store}] 메뉴판")
menu_list = RESTAURANTS[st.session_state.current_store]

for menu in menu_list:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{menu['name']}**")
        st.write(f"{menu['price']:,}원")
    with col2:
        if st.button("담기", key=f"btn_{menu['name']}"):
            st.session_state.cart.append(menu)
            st.toast(f"🛒 {menu['name']}을(를) 장바구니에 담았습니다!")
    st.divider()

# 5. 사이드바 - 장바구니 및 결제 현황
with st.sidebar:
    st.header("🛒 장바구니")
    
    if not st.session_state.cart:
        st.write("장바구니가 비어 있습니다.")
    else:
        total_price = 0
        for idx, item in enumerate(st.session_state.cart):
            st.write(f"- {item['name']} ({item['price']:,}원)")
            total_price += item['price']
        
        st.divider()
        st.subheader(f"총 금액: {total_price:,}원")
        
        if st.button("💳 주문 및 결제하기", type="primary"):
            st.session_state.order_status = "결제 완료"
            st.session_state.cart = [] # 주문 완료 후 장바구니 비우기
            st.rerun()

# 6. 실시간 배달 상태 표시 시뮬레이션
if st.session_state.order_status:
    st.success("🎉 주문이 정상적으로 접수되었습니다!")
    
    status_box = st.empty()
    progress_bar = st.progress(0)
    
    # 배달 단계 시뮬레이션 코드
    steps = [
        ("👨‍🍳 가게에서 음식을 조리하고 있습니다...", 25),
        ("🛵 라이더가 배정을 받고 출발했습니다!", 60),
        ("🏁 배달이 완료되었습니다! 맛있게 드세요! 🎉", 100)
    ]
    
    for text, percentage in steps:
        status_box.markdown(f"### 현재 배달 상태:\n**{text}**")
        progress_bar.progress(percentage)
        time.sleep(2)  # 실제 상황처럼 가상 딜레이 부여
        
    # 시뮬레이션 종료 후 상태 초기화 버튼
    if st.button("새로 주문하기"):
        st.session_state.order_status = None
        st.rerun()
