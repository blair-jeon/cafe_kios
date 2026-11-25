"""카페 키오스크 주문 모듈

주문(Order) 객체를 생성하고, 주문 항목을 추가하며, 주문 상태를 관리합니다.
menu.py의 make_order_item(), get_price(), normalize_temperature()를 사용합니다.
"""

from menu import make_order_item, normalize_temperature


class Order:
    """단일 주문을 나타냅니다."""

    def __init__(self, order_number: int):
        self.order_number: int = order_number
        self.items: list[dict] = []
        self.total: int = 0
        self.status: str = "주문 접수"  # 주문 접수 -> 준비 중 -> 완료

    def add_item(self, name: str, temperature: str, quantity: int) -> dict:
        """주문 항목을 추가하고 총 금액을 갱신합니다.

        Parameters
        ----------
        name : str
            메뉴 이름
        temperature : str
            HOT/ICE (menu.normalize_temperature로 정규화됨)
        quantity : int
            수량

        Returns
        -------
        dict
            추가된 주문 항목 정보 (make_order_item 반환값)
        """
        item = make_order_item(name, temperature, quantity)
        self.items.append(item)
        self.total += item["total_price"]
        return item

    def summary(self) -> str:
        """주문 내역을 사람이 읽기 쉬운 문자열로 반환합니다."""
        lines = [f"주문 번호: {self.order_number}"]
        for item in self.items:
            lines.append(
                f"  - {item['name']} [{item['temperature']}] x{item['quantity']} = "
                f"{item['total_price']:,}원"
            )
        lines.append(f"  총 합계: {self.total:,}원")
        return "\n".join(lines)

    def is_empty(self) -> bool:
        """주문 항목이 하나도 없으면 True를 반환합니다."""
        return len(self.items) == 0


# 주문 번호 생성기 (프로그램 전체에서 1 증가)
_ORDER_COUNTER = 1000


def create_order() -> Order:
    """새 주문 객체를 생성하고 순차적인 주문 번호를 부여합니다."""
    global _ORDER_COUNTER
    _ORDER_COUNTER += 1
    return Order(_ORDER_COUNTER)
