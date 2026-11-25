"""PAYMENT.py - 카페 키오스크 결제 로직 (초안)

주문(order) 형식 예시:
    order = [
        {"name": "아메리카노", "temp": "ICE", "qty": 2},
        {"name": "라떼", "temp": "HOT", "qty": 1},
    ]
"""
from menu import get_price

# ---------------------------------------------------------------
# 가격 계산
# ---------------------------------------------------------------
def get_unit_price(name, temp="HOT"):
    """메뉴 1잔의 가격. (menu.py 기준) ."""
    return get_price(name, temp)


def calculate_line_total(item):
    """주문 한 줄(메뉴 + 온도 + 수량)의 금액."""
    qty = item.get("qty", 1)
    if qty <= 0:
        raise ValueError("수량은 1 이상이어야 합니다.")
    return get_unit_price(item["name"], item.get("temp", "HOT")) * qty


def calculate_total(order):
    """주문 전체 합계."""
    if not order:
        raise ValueError("주문 내역이 비어 있습니다.")
    return sum(calculate_line_total(item) for item in order)


# ---------------------------------------------------------------
# 결제 수단별 처리
# ---------------------------------------------------------------
def pay_by_cash(total, paid):
    """현금 결제. 성공 시 거스름돈, 금액 부족 시 None 반환."""
    if paid < total:
        print(f"금액이 부족합니다. ({total - paid:,}원 더 필요)")
        return None
    return paid - total


def pay_by_card(total):
    """카드 결제 (실제 승인 대신 성공으로 처리하는 모의 함수)."""
    print(f"카드 승인 요청: {total:,}원")
    return True


# ---------------------------------------------------------------
# 영수증
# ---------------------------------------------------------------
def print_receipt(order, total, method, paid=None, change=None):
    print("=" * 32)
    print("          영 수 증")
    print("=" * 32)
    for item in order:
        temp = item.get("temp", "HOT")
        qty = item.get("qty", 1)
        line = calculate_line_total(item)
        print(f"{item['name']}({temp}) x{qty}".ljust(20) + f"{line:>8,}원")
    print("-" * 32)
    print("합계".ljust(20) + f"{total:>8,}원")
    print(f"결제수단: {method}")
    if method == "현금":
        print("받은 금액".ljust(20) + f"{paid:>8,}원")
        print("거스름돈".ljust(20) + f"{change:>8,}원")
    print("=" * 32)


# ---------------------------------------------------------------
# 결제 진행 (MAIN.py에서 호출할 함수)
# ---------------------------------------------------------------
def process_payment(order, method, paid=None):
    """
    order : 주문 리스트
    method: "현금" 또는 "카드"
    paid  : 현금일 때 받은 금액
    return: 결제 성공 여부 (True / False)
    """
    total = calculate_total(order)

    if method == "현금":
        if paid is None:
            raise ValueError("현금 결제는 받은 금액(paid)이 필요합니다.")
        change = pay_by_cash(total, paid)
        if change is None:
            return False
        print_receipt(order, total, method, paid, change)
        return True

    if method == "카드":
        if not pay_by_card(total):
            return False
        print_receipt(order, total, method)
        return True

    raise ValueError(f"지원하지 않는 결제수단입니다: {method}")


# ---------------------------------------------------------------
# 단독 테스트용
# ---------------------------------------------------------------
if __name__ == "__main__":
    test_order = [
        {"name": "아메리카노", "temp": "ICE", "qty": 2},
        {"name": "라떼", "temp": "HOT", "qty": 1},
        {"name": "콜드브루", "temp": "ICE", "qty": 1},
    ]
    process_payment(test_order, "현금", paid=20000)
    process_payment(test_order, "카드")
    process_payment(test_order, "현금", paid=10000)  # 금액 부족 케이스