"""
카페 키오스크 - 메뉴 모듈 (menu.py)

메뉴 데이터와 메뉴 조회/검증/가격 계산 함수를 담당합니다.
모든 메뉴는 HOT / ICE 두 가지 온도를 선택할 수 있습니다.
"""

# ---------------------------------------------------------------------------
# 설정값
# ---------------------------------------------------------------------------

HOT = "HOT"
ICE = "ICE"
TEMPERATURES = (HOT, ICE)

# ICE 선택 시 추가 요금 (팀에서 정책이 정해지면 수정)
ICE_EXTRA_PRICE = 500

# 사용자가 입력할 수 있는 다양한 표현 → 표준 온도값
_TEMPERATURE_ALIASES = {
    "hot": HOT, "h": HOT, "핫": HOT, "뜨거운": HOT, "따뜻한": HOT,
    "ice": ICE, "iced": ICE, "i": ICE, "아이스": ICE, "차가운": ICE,
}

# ---------------------------------------------------------------------------
# 메뉴 데이터
# 가격은 임시값입니다. 팀에서 확정된 가격으로 바꿔 주세요.
# ---------------------------------------------------------------------------

MENU = {
    # 커피
    "핸드드립":   {"id": 1,  "category": "커피",   "price": 5000},
    "에스프레소": {"id": 2,  "category": "커피",   "price": 3500},
    "아메리카노": {"id": 3,  "category": "커피",   "price": 4000},
    "라떼":       {"id": 4,  "category": "커피",   "price": 4500},
    "콜드브루":   {"id": 5,  "category": "커피",   "price": 4800},
    # 라떼(논커피)
    "초코라떼":   {"id": 6,  "category": "논커피", "price": 4800},
    "딸기라떼":   {"id": 7,  "category": "논커피", "price": 5000},
    # 차
    "유자차":     {"id": 8,  "category": "차",     "price": 4500},
    "대추차":     {"id": 9,  "category": "차",     "price": 5000},
    "율무차":     {"id": 10, "category": "차",     "price": 4000},
    "쌍화차":     {"id": 11, "category": "차",     "price": 5000},
    "페퍼민트티": {"id": 12, "category": "차",     "price": 4000},
}


# ---------------------------------------------------------------------------
# 조회 함수
# ---------------------------------------------------------------------------

def get_categories():
    """카테고리 목록을 메뉴 등록 순서대로 반환합니다. 예: ['커피', '논커피', '차']"""
    categories = []
    for info in MENU.values():
        if info["category"] not in categories:
            categories.append(info["category"])
    return categories


def get_menu_names(category=None):
    """메뉴 이름 목록을 반환합니다. category를 주면 해당 카테고리만 반환합니다."""
    if category is None:
        return list(MENU.keys())
    return [name for name, info in MENU.items() if info["category"] == category]


def get_menu_list():
    """전체 메뉴를 딕셔너리 리스트로 반환합니다 (화면 출력/API 응답용)."""
    return [
        {
            "id": info["id"],
            "name": name,
            "category": info["category"],
            "price": info["price"],
            "temperatures": list(TEMPERATURES),
        }
        for name, info in MENU.items()
    ]


def get_menu(name):
    """메뉴 이름으로 메뉴 정보를 반환합니다. 없으면 ValueError."""
    if not is_valid_menu(name):
        raise ValueError(f"존재하지 않는 메뉴입니다: {name}")
    info = MENU[name]
    return {"id": info["id"], "name": name, "category": info["category"],
            "price": info["price"], "temperatures": list(TEMPERATURES)}


def get_menu_by_id(menu_id):
    """메뉴 번호(id)로 메뉴 정보를 반환합니다. 없으면 ValueError."""
    for name, info in MENU.items():
        if info["id"] == menu_id:
            return get_menu(name)
    raise ValueError(f"존재하지 않는 메뉴 번호입니다: {menu_id}")


# ---------------------------------------------------------------------------
# 검증 함수
# ---------------------------------------------------------------------------

def is_valid_menu(name):
    """메뉴판에 있는 메뉴인지 확인합니다."""
    return name in MENU


def normalize_temperature(temperature):
    """'ice', '아이스', 'Hot' 같은 입력을 'HOT' / 'ICE'로 바꿉니다. 잘못된 값이면 ValueError."""
    if not isinstance(temperature, str):
        raise ValueError(f"온도는 문자열이어야 합니다: {temperature!r}")
    key = temperature.strip().lower()
    if key.upper() in TEMPERATURES:
        return key.upper()
    if key in _TEMPERATURE_ALIASES:
        return _TEMPERATURE_ALIASES[key]
    raise ValueError(f"온도는 HOT 또는 ICE만 선택할 수 있습니다: {temperature}")


def is_valid_temperature(temperature):
    """HOT / ICE로 해석 가능한 값인지 확인합니다."""
    try:
        normalize_temperature(temperature)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# 가격 / 주문 항목
# ---------------------------------------------------------------------------

def get_price(name, temperature=HOT):
    """메뉴 1잔 가격을 반환합니다. ICE는 ICE_EXTRA_PRICE가 더해집니다."""
    menu = get_menu(name)
    temp = normalize_temperature(temperature)
    extra = ICE_EXTRA_PRICE if temp == ICE else 0
    return menu["price"] + extra


def make_order_item(name, temperature, quantity=1):
    """
    주문 담당 모듈에 넘길 주문 항목을 만듭니다.

    반환 예:
    {'menu_id': 3, 'name': '아메리카노', 'temperature': 'ICE',
     'quantity': 2, 'unit_price': 4000, 'total_price': 8000}
    """
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
        raise ValueError(f"수량은 1 이상의 정수여야 합니다: {quantity!r}")
    menu = get_menu(name)
    temp = normalize_temperature(temperature)
    unit_price = get_price(name, temp)
    return {
        "menu_id": menu["id"],
        "name": name,
        "temperature": temp,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": unit_price * quantity,
    }


# ---------------------------------------------------------------------------
# 출력
# ---------------------------------------------------------------------------

def format_menu_board():
    """키오스크 화면용 메뉴판 문자열을 만듭니다."""
    lines = ["===== MENU (HOT / ICE) ====="]
    for category in get_categories():
        lines.append(f"\n[{category}]")
        for name in get_menu_names(category):
            info = MENU[name]
            hot_price = get_price(name, HOT)
            ice_price = get_price(name, ICE)
            if hot_price == ice_price:
                price_text = f"{hot_price:,}원"
            else:
                price_text = f"HOT {hot_price:,}원 / ICE {ice_price:,}원"
            lines.append(f"{info['id']:>2}. {name:<6} {price_text}")
    return "\n".join(lines)


def print_menu():
    """메뉴판을 콘솔에 출력합니다."""
    print(format_menu_board())


if __name__ == "__main__":
    # 직접 실행했을 때 간단히 동작 확인
    print_menu()
    print()
    print(make_order_item("아메리카노", "ice", 2))

