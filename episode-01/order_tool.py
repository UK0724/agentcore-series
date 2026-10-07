"""An actual local tool example. No LLM, cloud deployment, or AWS API call."""
ORDERS = {
    "1042": {
        "order_id": "1042",
        "customer_id": "demo-customer",
        "item": "Mechanical keyboard",
        "status": "Out for delivery",
        "total_inr": 2400,
    }
}


def get_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": "Order not found", "order_id": order_id}
    return dict(order)


if __name__ == "__main__":
    import json
    print(json.dumps(get_order("1042"), indent=2))
