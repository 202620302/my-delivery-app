import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="배달의민족 외식업광장 벤치마킹", page_icon="🛵", layout="wide")

# 2. 상단 메뉴바 HTML & CSS (마우스 올리면 서브메뉴가 쫙 뜨는 효과)
st.markdown("""
    <style>
    /* 기본 배경 및 폰트 설정 */
    .stApp { background-color: #F6F6F6; }
    
    /* 상단 메뉴바 전체 컨테이너 */
    .navbar {
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0px;
        border-bottom: 1px solid #EAEAEA;
        position: relative;
        z-index: 9999;
    }
    
    /* 로고 스타일 */
    .nav-logo {
        font-size: 22px;
        font-weight: bold;
        color: #2AC1BC;
        margin-right: 50px;
        text-decoration: none;
    }
    
    /* 메인 메뉴 아이템 목록 */
    .nav-links {
        display: flex;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    /* 각 메인 메뉴 아이템 */
    .nav-item {
        position: relative;
        padding: 15px 25px;
    }
    
    .nav-item > a {
        text-decoration: none;
        color: #333333;
        font-weight: bold;
        font-size: 16px;
    }
    
    .nav-item:hover > a {
        color: #2AC1BC;
    }
    
    /* ⭐ 마우스 올렸을 때 나오는 서브 메뉴 (기본 상태는 숨김) */
    .dropdown-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        min-width: 160px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
        border-radius: 8px;
        padding: 10px 0;
        list-style: none;
    }
    
    /* 서브 메뉴의 링크 스타일 */
    .dropdown-menu a {
        color: #555555;
        padding: 10px 20px;
        text-decoration: none;
        display: block;
        font-size: 14px;
        white-space: nowrap;
    }
    
    .dropdown-menu a:hover {
        background-color: #E2F6F5;
        color: #2AC1BC;
    }
    
    /* ⭐ 마우스 오버 시 서브메뉴 보이게 하는 핵심 CSS 효과 */
    .nav-item:hover .dropdown-menu {
        display: block;
    }
    
    /* 가게 카드 및 배너 스타일 */
    .store-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    .badge-ready { background-color: #E2F6F5; color: #2AC1BC; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .badge-preparing { background-color: #EEEEEE; color: #888888; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .hero-banner {
        background-color: #D2F2F1;
        padding: 40px;
        border-radius: 16px;
        margin-bottom: 30px;
    }
    </style>
    
    <div class="navbar">
        <a href="?page=home" class="nav-logo">🛵 배민외식업광장</a>
        <ul class="nav-links">
            <li class="nav-item">
                <a href="#">배민 입점·운영</a>
                <ul class="dropdown-menu">
                    <li><a href="?page=home">▶ 우리 동네 맛집 (홈)</a></li>
                    <li><a href="?page=intro">입점 안내 가이드</a></li>
                </ul>
            </li>
            <li class="nav-item">
                <a href="#">혜택·이벤트</a>
                <ul class="dropdown-menu">
                    <li><a href="?page=event">🎁 진행 중인 이벤트</a></li>
                    <li><a href="?page=event">신규 성장 패키지</a></li>
                </ul>
            </li>
            <li class="nav-item">
                <a href="#">가게 운영 지원</a>
                <ul class="dropdown-menu">
                    <li><a href="?page=faq">🙋 자주 묻는 질문 (FAQ)</a></li>
                    <li><a href="?page=faq">1:1 빠른 문의</a></li>
                </ul>
            </li>
        </ul>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 3. URL 주소 뒤의 파라미터(?page=...)를 감지하여 현재 페이지 알아내기
query_params = st.query_params
current_page = query_params.get("page", "home")

# 데이터 구조 (가게 정보)
STORES = {
    "족발·보쌈": {"가게명": "장인 족발 반반 세트", "상태": "OPEN", "rating": "⭐ 4.9", "tip": "2,000원", "menu": [{"name": "한돈 온족발 (소)", "price": 29000}, {"name": "직화 불족발 (소)", "price": 31000}]},
    "치킨": {"가게명": "바삭 후라이드 1988", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []},
    "피자·양식": {"가게명": "치즈 폭탄 피자 가든", "상태": "PREPARING", "rating": "⭐ -", "tip": "-", "menu": []}
}

if "cart" not in st.session_state: st.session_state.cart = []
if "order_status" not in st.session_state: st.session_state.order_status = None

# --- 4. 페이지 전환 및 렌더링 ---

# [1] 홈 화면 (가게 목록)
if current_page == "home":
    # 배민 신규 성장 패키지 스타일의 중앙 배너 광고
    st.markdown("""
    <div class="hero-banner">
        <span style="color: #2AC1BC; font-weight: bold; font-size:14px;">신규 파트너 주문 수 상승!</span>
        <h2 style="margin: 10px 0 5px 0; font-size: 28px;">🚀 신규 성장 패키지 출시</h2>
        <p style="color: #666; margin: 0;">가게 등록 첫 달 주문 수가 평균 <b>4.8배</b> 증가하는 효과를 직접 경험해 보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💡 오늘 마음에 드는 카테고리를 선택하세요")
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
                
                for menu in store_info["menu"]:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{menu['name']}** - {menu['price']:,}원")
                    with col2:
                        if st.button("담기", key=f"add_{menu['name']}"):
                            st.session_state.cart.append(menu)
                            st.toast(f"🛒 장바구니 추가 완료!")

    # 하단 장바구니 간이 노출
    if st.session_state.cart:
        st.divider()
        st.subheader("🛒 현재 장바구니 내역")
        for item in st.session_state.cart:
            st.write(f"- {item['name']} ({item['price']:,}원)")
        if st.button("💳 주문하기 (시뮬레이션)"):
            st.balloons()
            st.success("주문 완료! 라이더가 곧 배정됩니다.")
            st.session_state.cart = []

# [2] 이벤트 페이지
elif current_page == "event":
    st.title("🎁 진행 중인 혜택 & 이벤트")
    st.write("사장님과 이웃 모두를 위한 풍성한 이벤트를 확인하세요.")
    st.divider()
    st.markdown("""
    <div class="store-card" style="border-left: 5px solid #2AC1BC;">
        <h3>🎉 중개이용료 14일간 100% 전액 지원 패키지</h3>
        <p style="color:#666;">지금 온라인으로 입점 신청을 하시면 초기 정착 지원 혜택을 100% 드립니다.</p>
    </div>
    <div class="store-card" style="border-left: 5px solid #2AC1BC;">
        <h3>🔥 우리가게클릭 스마트모드 30일 무료 체험</h3>
        <p style="color:#666;">추가 홍보비 최대 10만 원 상당의 혜택을 드리는 찬스!</p>
    </div>
    """, unsafe_allow_html=True)

# [3] 고객센터 페이지
elif current_page == "faq":
    st.title("🙋 무엇을 도와드릴까요?")
    st.write("배민 외식업광장 고객 지원 센터센터입니다.")
    st.divider()
    with st.expander("❓ 입점 신청 서류는 무엇이 필요한가요?"):
        st.write("사업자등록증 사본, 영업신고증 사본, 대표자 명의 통장 사본이 필수로 요구됩니다.")
    with st.expander("❓ 광고 비용 정산은 언제 되나요?"):
        st.write("주간 단위로 정산되어 매주 수요일에 지정하신 계좌로 입금됩니다.")

# [4] 임시 안내 페이지
elif current_page == "intro":
    st.title("📄 배민 입점 안내 가이드")
    st.info("현재 상세 가이드 문서를 준비 중입니다. 신속히 업데이트하겠습니다!")
