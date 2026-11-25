"""
카페 키오스크 - main.py (조립 담당)

흐름: 메뉴판 출력 → 메뉴/온도(1.HOT 2.ICE)/수량 선택 → [1.더 담기 / 2.결제하기] → 결제(카드/현금) → 다음 손님

사용하는 팀원 모듈
    menu.py    : print_menu(), get_menu_by_id(), is_valid_temperature(), normalize_temperature()
    order.py   : create_order(), Order.add_item(), Order.summary(), Order.is_empty()
    payment.py : calculate_total(), process_payment()
"""

import menu
import order
import payment


# ---------------------------------------------------------------
# 입력 도우미
# ---------------------------------------------------------------
def ask_number(prompt, min_value, max_value):
    """min_value~max_value 사이 정수를 입력받을 때까지 반복해서 묻는다."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and min_value <= int(text) <= max_value:
            return int(text)
        print(f"{min_value}~{max_value} 사이의 숫자를 입력해주세요.")


def ask_temperature(name):
    """온도를 숫자로 입력받는다. 1 → HOT, 2 → ICE"""
    print(f"\n{name} 온도를 선택하세요.")
    print("1. HOT  2. ICE")
    choice = ask_number("번호 입력: ", 1, 2)
    return menu.HOT if choice == 1 else menu.ICE


def ask_yes_no(prompt):
    return input(prompt).strip().lower() in ("y", "yes", "예", "네", "ㅇ")


# ---------------------------------------------------------------
# 주문
# ---------------------------------------------------------------
def take_order():
    """메뉴를 골라 Order 객체를 채워서 반환한다."""
    current = order.create_order()
    max_id = len(menu.MENU)

    while True:
        print()
        menu.print_menu()

        # 장바구니가 비었을 때와 아닐 때 0번의 의미를 다르게 보여준다
        if current.is_empty():
            prompt = "\n주문할 메뉴 번호를 입력하세요 (0: 주문 취소): "
        else:
            prompt = "\n추가할 메뉴 번호를 입력하세요 (0: 추가 없이 결제하기): "

        menu_id = ask_number(prompt, 0, max_id)
        if menu_id == 0:
            return current

        name = menu.get_menu_by_id(menu_id)["name"]
        temperature = ask_temperature(name)
        quantity = ask_number(f"{name} 수량을 입력하세요: ", 1, 99)

        item = current.add_item(name, temperature, quantity)
        print(f"\n→ {name} [{temperature}] {quantity}잔 담았습니다. "
              f"({item['total_price']:,}원)")
        print(f"   현재 합계: {current.total:,}원")

        # 담은 직후, 다음 행동을 명확하게 묻는다
        print("\n1. 메뉴 더 담기  2. 주문 끝내고 결제하기")
        if ask_number("번호 입력: ", 1, 2) == 2:
            return current


def to_payment_format(current):
    """order.py의 주문 항목을 payment.py가 받는 형식으로 바꾼다.

    order.py   : {"name", "temperature", "quantity", ...}
    payment.py : {"name", "temp", "qty"}
    """
    return [
        {"name": item["name"], "temp": item["temperature"], "qty": item["quantity"]}
        for item in current.items
    ]


# ---------------------------------------------------------------
# 결제
# ---------------------------------------------------------------
def checkout(current):
    """결제를 진행한다. 성공하면 True, 손님이 취소하면 False."""
    pay_items = to_payment_format(current)
    total = payment.calculate_total(pay_items)

    while True:
        print(f"\n결제 금액: {total:,}원")
        print("1. 카드  2. 현금  0. 결제 취소")
        choice = ask_number("결제 수단을 선택하세요: ", 0, 2)

        if choice == 0:
            return False

        if choice == 1:
            if payment.process_payment(pay_items, "카드"):
                return True
        else:
            paid = ask_number("받은 금액을 입력하세요: ", 0, 10_000_000)
            if payment.process_payment(pay_items, "현금", paid=paid):
                return True

        print("결제에 실패했습니다. 다시 시도해주세요.")


# ---------------------------------------------------------------
# 메인
# ---------------------------------------------------------------
def main():
    print("=" * 32)
    print("   카페 키오스크에 오신 걸 환영합니다")
    print("=" * 32)

    while True:
        current = take_order()

        if current.is_empty():
            print("\n주문한 메뉴가 없습니다.")
        else:
            print()
            print(current.summary())

            if checkout(current):
                current.status = "준비 중"
                print(f"\n결제가 완료되었습니다. 주문 번호는 {current.order_number}번입니다.")
            else:
                print("\n주문이 취소되었습니다.")

        if not ask_yes_no("\n새 주문을 하시겠습니까? (y/n): "):
            print("이용해주셔서 감사합니다.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n키오스크를 종료합니다.")
