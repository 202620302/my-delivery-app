import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="배달의민족 - 우리 동네 맛집", page_icon="🛵", layout="centered")

# 2. 배달의민족 스타일 CSS 적용
st.markdown("""
    <style>
    :root { --baemin-color: #2AC1BC; }
    .stApp { background-color: #F6F6F6; }
    h1, h2, h3 { color: #333333; }
    .stButton>button {
        width: 100%;
        background-color: #2AC1BC !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold;
        padding: 0.5rem;
    }
    .stButton>button:hover { background-color: #229A96 !important; }
    .store-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .badge-ready { background-color: #E2F6F5; color: #2AC1BC; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .badge-preparing { background-color: #EEEEEE; color: #888888; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .event-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #2AC1BC;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 구조 (가게 정보)
STORES = {
    "족발·보쌈": {
        "가게명": "장인 족발 반반 세트", "상태": "OPEN", "rating": "⭐ 4.9", "tip": "2,000원",
        "menu": [
            {"name": "한돈 온족발 (소)", "price": 29000},
            {"name": "직화 불족발 (소)", "price": 31000},
            {"name": "쟁반막국수", "price": 7000}
        ]
    },
    "돈까스·회·일식": {"가게명": "동네 돈카츠 & 연어", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []},
    "고기·구이": {"가게명": "삼겹살 배달 전문점", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []},
    "피자·양식": {"가게명": "치즈 폭탄 피자 가든", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []},
    "치킨": {"가게명": "바삭 후라이드 1988", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []},
    "중식": {"가게명": "황금룡 수타 짜장", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []}
}

# 세션 상태 초기화
if "cart" not in st.session_state: st.session_state.cart = []
if "order_status" not in st.session_state: st.session_state.order_status = None

# --- 4. 사이드바 페이지 네비게이션 메뉴 ---
with st.sidebar:
    st.markdown("<h2 style='color: #2AC1BC;'>메뉴 바로가기</h2>", unsafe_allow_html=True)
    # 라디오 버튼을 이용해 사용자가 페이지를 선택하도록 유도
    page = st.radio("이동할 페이지를 선택하세요", ["🏠 홈 (가게 목록)", "🎁 진행 중인 이벤트", "🙋 고객센터 / FAQ"])
    st.divider()

# --- 5. 페이지별 화면 렌더링 ---

# [페이지 1: 홈 화면]
if page == "🏠 홈 (가게 목록)":
    st.markdown("<h1 style='color: #2AC1BC; font-size: 40px; margin-bottom: 0px;'>🛵 배달의민족</h1>", unsafe_allow_html=True)
    st.write("📍 **의정부시 의정부동** 주변의 맛집 목록입니다.")
    st.divider()

    st.subheader("오늘 어떤 메뉴가 당기시나요? 🍕")
    tabs = st.tabs(list(STORES.keys()))

    for i, category in enumerate(STORES.keys()):
        with tabs[i]:
            store_info = STORES[category]
            if store_info["상태"] == "PREPARING":
                st.markdown(f"""
                <div class="store-card">
                    <span class="badge-preparing">⏱️ 입점 예정</span>
                    <h3 style='margin: 5px 0;'>{store_info['가게명']}</h3>
                    <p style='color: #888888; font-size: 14px; margin: 0;'>현재 서비스 준비 중인 매장입니다. 조금만 기다려주세요!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="store-card">
                    <span class="badge-ready">● 주문 가능</span>
                    <h3 style='margin: 5px 0;'>{store_info['가게명']}</h3>
                    <p style='margin: 0; font-size: 14px; color: #555555;'>평점: {store_info['rating']} | 배달팁: {store_info['tip']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("👇 **아래 메뉴를 장바구니에 담아 테스트해보세요!**")
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

    # 장바구니 기능을 사이드바 하단에 결합
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

    # 주문 진행 상태 애니메이션
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
            time.sleep(1.5)
        if st.button("추가 주문하기"):
            st.session_state.order_status = None
            st.rerun()

# [페이지 2: 이벤트 페이지]
elif page == "🎁 진행 중인 이벤트":
    st.title("🎁 배민 이벤트존")
    st.write("지금만 참여할 수 있는 특별한 혜택을 놓치지 마세요!")
    st.divider()

    st.markdown("""
    <div class="event-card">
        <h3>🎉 신규 가입 첫 주문 10,000원 쿠폰팩</h3>
        <p style='color: #666;'>배민이 처음이신가요? 지금 가입하면 첫 주문 즉시 사용할 수 있는 만원 할인 쿠폰을 드립니다.</p>
        <small style='color: #999;'>기간: 2026.07.01 ~ 2026.07.31</small>
    </div>
    <div class="event-card">
        <h3>🛵 매주 금요일은 배달팁 0원 데이!</h3>
        <p style='color: #666;'>금요일 퇴근길, 어떤 메뉴를 시켜도 배달팁은 배민이 쏩니다! (일부 매장 제외)</p>
        <small style='color: #999;'>기간: 연중무휴</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("쿠폰 전부 받기 🎫"):
        st.balloons()
        st.toast("모든 쿠폰이 발급되었습니다! 홈 화면에서 사용해보세요.")

# [페이지 3: 고객센터 페이지]
elif page == "🙋 고객센터 / FAQ":
    st.title("🙋 무엇을 도와드릴까요?")
    st.write("방구석 배달앱 고객센터입니다. 자주 묻는 질문을 확인해보세요.")
    st.divider()

    with st.expander("❓ 주문을 취소하고 싶어요."):
        st.write("주문 접수 완료 전에는 앱 내에서 직접 취소가 가능합니다. 다만, 가게에서 음식을 조리하기 시작한 이후에는 취소가 어려우니 매장으로 직접 연락해 주셔야 합니다.")
        
    with st.expander("❓ 배달 주소를 잘못 입력했어요."):
        st.write("라이더가 출발하기 전이라면 고객센터 전화를 통해 주소 변경이 가능합니다. 빠르게 전화를 주셔야 조치가 가능합니다.")
        
    with st.expander("❓ 결제 영수증은 어디서 발급받나요?"):
        st.write("[마이배민 -> 주문 내역]에서 각 주문별 전자 영수증 다운로드 및 이메일 발송이 가능합니다.")

    st.divider()
    st.subheader("📞 1:1 빠른 문의")
    st.text_input("이메일 주소", placeholder="답변받으실 이메일을 입력하세요.")
    st.text_area("문의 내용", placeholder="불편하신 점이나 문의사항을 입력해 주세요.")
    if st.button("문의하기 제출"):
        st.success("문의가 성공적으로 접수되었습니다. 담당자가 확인 후 답변드리겠습니다!")
