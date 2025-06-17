import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_API_KEY
stripe.api_key = STRIPE_API_KEY

def convert_rub_to_dollar(amount):
    """Переводит рубли в доллары"""
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)

def create_stripe_price(amount):
    """Определяет цену в страйпе"""
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )
    return price

def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.financial_connections.Session.create(
        success_url="http://127.0.0.1:8000/user/payment/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
