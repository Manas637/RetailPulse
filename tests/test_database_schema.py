import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL


load_dotenv()


def get_engine():
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            f"Missing database environment variables: {missing}"
        )

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    return create_engine(database_url)


def test_required_tables_exist():
    engine = get_engine()
    inspector = inspect(engine)

    actual_tables = set(inspector.get_table_names())

    expected_tables = {
        "customers",
        "orders",
        "order_items",
        "order_payments",
        "order_reviews",
        "products",
        "sellers",
        "geolocation",
        "category_translation",
    }

    assert expected_tables.issubset(actual_tables)


def test_orders_have_customer_foreign_key():
    engine = get_engine()
    inspector = inspect(engine)

    foreign_keys = inspector.get_foreign_keys("orders")

    assert any(
        fk["referred_table"] == "customers"
        and "customer_id" in fk["constrained_columns"]
        for fk in foreign_keys
    )


def test_order_items_have_required_foreign_keys():
    engine = get_engine()
    inspector = inspect(engine)

    foreign_keys = inspector.get_foreign_keys("order_items")

    referenced_tables = {
        fk["referred_table"]
        for fk in foreign_keys
    }

    assert "orders" in referenced_tables
    assert "products" in referenced_tables
    assert "sellers" in referenced_tables