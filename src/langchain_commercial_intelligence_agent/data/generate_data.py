from pathlib import Path
import random
import sqlite3
from datetime import date


SEED = 42
rng = random.Random(SEED)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "commercial.db"


REGIONS = [
    (1, "Sudeste"),
    (2, "Sul"),
    (3, "Nordeste"),
    (4, "Centro-Oeste"),
]


SALESPEOPLE = [
    (1, "Ana Martins", 1, "2022-03-14"),
    (2, "Bruno Oliveira", 1, "2023-01-09"),
    (3, "Carla Souza", 1, "2021-08-23"),
    (4, "Daniel Rocha", 2, "2022-11-07"),
    (5, "Eduarda Lima", 2, "2023-05-15"),
    (6, "Felipe Santos", 3, "2022-06-20"),
    (7, "Gabriela Alves", 3, "2024-02-12"),
    (8, "Henrique Costa", 4, "2021-10-04"),
    (9, "Isabela Mendes", 4, "2023-07-17"),
    (10, "João Ribeiro", 1, "2022-09-05"),
]


PRODUCTS = [
    (1, "Analytics Basic", "Analytics", 500.00),
    (2, "Analytics Pro", "Analytics", 1200.00),
    (3, "CRM Basic", "CRM", 650.00),
    (4, "CRM Pro", "CRM", 1100.00),
    (5, "CRM Enterprise", "CRM", 2000.00),
    (6, "Automation Starter", "Automation", 750.00),
    (7, "Automation Pro", "Automation", 1400.00),
    (8, "Automation Platform", "Automation", 2500.00),
]


MONTHLY_SALES_COUNT = {
    1: 180,
    2: 195,
    3: 210,
    4: 225,
    5: 240,
    6: 255,
    7: 270,
    8: 285,
    9: 220,
}

SALESPERSON_WEIGHTS = {
    1: 1.10,
    2: 0.95,
    3: 1.15,
    4: 1.00,
    5: 0.95,
    6: 0.90,
    7: 0.70,
    8: 0.90,
    9: 0.95,
    10: 1.30,
}

SEPTEMBER_SALESPERSON_MULTIPLIERS = {
    1: 0.85,
    2: 0.95,
    3: 0.65,
    4: 0.70,
    5: 0.95,
    6: 1.00,
    7: 0.85,
    8: 1.05,
    9: 1.00,
    10: 1.10,
}

PRODUCT_WEIGHTS = {
    1: 1.10,
    2: 1.35,
    3: 1.00,
    4: 1.05,
    5: 0.85,
    6: 0.95,
    7: 1.05,
    8: 1.10,
}

SEPTEMBER_PRODUCT_MULTIPLIERS = {
    1: 1.00,
    2: 0.55,
    3: 1.00,
    4: 0.95,
    5: 0.85,
    6: 1.00,
    7: 1.05,
    8: 1.30,
}

SEGMENT_SALES_WEIGHTS = {
    "SMB": 1.00,
    "Mid-Market": 1.20,
    "Enterprise": 1.50,
}

SEPTEMBER_SEGMENT_MULTIPLIERS = {
    "SMB": 1.00,
    "Mid-Market": 0.90,
    "Enterprise": 0.60,
}

REGION_SALES_WEIGHTS = {
    1: 1.40,
    2: 1.10,
    3: 0.90,
    4: 0.75,
}

SEPTEMBER_REGION_MULTIPLIERS = {
    1: 0.60,
    2: 0.90,
    3: 1.00,
    4: 1.20,
}

CUSTOMER_COUNT = 80

CUSTOMER_SEGMENTS = [
    "SMB",
    "Mid-Market",
    "Enterprise",
]

CUSTOMER_SEGMENT_WEIGHTS = [
    0.50,
    0.30,
    0.20,
]

CUSTOMER_REGION_IDS = [
    1,
    2,
    3,
    4,
]

CUSTOMER_REGION_WEIGHTS = [
    0.45,
    0.25,
    0.18,
    0.12,
]

COMPANY_PREFIXES = [
    "Nova",
    "Prime",
    "Atlas",
    "Nexus",
    "Vitta",
    "Horizonte",
    "Vertex",
    "Orion",
    "Alpha",
    "Integra",
]

COMPANY_SUFFIXES = [
    "Tech",
    "Solutions",
    "Logistica",
    "Industria",
    "Digital",
    "Comercio",
    "Servicos",
    "Group",
]

BASE_MONTHLY_TARGETS = {
    1: 85000.00,   # Ana Martins
    2: 72000.00,   # Bruno Oliveira
    3: 90000.00,   # Carla Souza
    4: 76000.00,   # Daniel Rocha
    5: 70000.00,   # Eduarda Lima
    6: 68000.00,   # Felipe Santos
    7: 65000.00,   # Gabriela Alves
    8: 68000.00,   # Henrique Costa
    9: 70000.00,   # Isabela Mendes
    10: 88000.00,  # João Ribeiro
}

MONTHLY_TARGET_MULTIPLIERS = {
    1: 1.00,
    2: 1.03,
    3: 1.06,
    4: 1.09,
    5: 1.12,
    6: 1.15,
    7: 1.18,
    8: 1.21,
    9: 1.24,
}

def create_schema(connection: sqlite3.Connection) -> None:
    """Create a fresh SQLite schema for the synthetic commercial dataset."""

    cursor = connection.cursor()

    cursor.executescript(
            """
            DROP TABLE IF EXISTS sales;
            DROP TABLE IF EXISTS targets;
            DROP TABLE IF EXISTS customers;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS salespeople;
            DROP TABLE IF EXISTS regions;

            CREATE TABLE regions (
                region_id INTEGER PRIMARY KEY,
                region_name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE salespeople (
                salesperson_id INTEGER PRIMARY KEY,
                salesperson_name TEXT NOT NULL,
                region_id INTEGER NOT NULL,
                hire_date TEXT NOT NULL,

                FOREIGN KEY (region_id)
                    REFERENCES regions(region_id)
            );

            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                segment TEXT NOT NULL
                    CHECK (segment IN ('SMB', 'Mid-Market', 'Enterprise')),
                region_id INTEGER NOT NULL,

                FOREIGN KEY (region_id)
                    REFERENCES regions(region_id)
            );

            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                unit_price REAL NOT NULL
                    CHECK (unit_price > 0)
            );

            CREATE TABLE sales (
                sale_id INTEGER PRIMARY KEY,
                sale_date TEXT NOT NULL,
                salesperson_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL
                    CHECK (quantity > 0),
                unit_price REAL NOT NULL
                    CHECK (unit_price > 0),
                total_amount REAL NOT NULL
                    CHECK (total_amount > 0),

                FOREIGN KEY (salesperson_id)
                    REFERENCES salespeople(salesperson_id),

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id),

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            );

            CREATE TABLE targets (
                target_id INTEGER PRIMARY KEY,
                salesperson_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL
                    CHECK (month BETWEEN 1 AND 12),
                target_amount REAL NOT NULL
                    CHECK (target_amount > 0),

                FOREIGN KEY (salesperson_id)
                    REFERENCES salespeople(salesperson_id),

                UNIQUE (salesperson_id, year, month)
            );
            """
        )


def insert_regions(connection: sqlite3.Connection) -> None:
    """Insert the predefined commercial regions into the database."""

    connection.executemany(
        """
        INSERT INTO regions (
            region_id,
            region_name
        )
        VALUES (?, ?)
        """,
        REGIONS,
    )

def insert_salespeople(connection: sqlite3.Connection) -> None:
    """Insert the predefined salespeople into the database."""

    connection.executemany(
        """
        INSERT INTO salespeople (
            salesperson_id,
            salesperson_name,
            region_id,
            hire_date
        )
        VALUES (?, ?, ?, ?)
        """,
        SALESPEOPLE,
    )

def insert_products(connection: sqlite3.Connection) -> None:
    """Insert the predefined product catalog into the database."""

    connection.executemany(
        """
        INSERT INTO products (
            product_id,
            product_name,
            category,
            unit_price
        )
        VALUES (?, ?, ?, ?)
        """,
        PRODUCTS,
    )

def generate_customers() -> list[tuple[int, str, str, int]]:
    """Generate reproducible synthetic customer records."""

    customers = []

    for customer_id in range(1, CUSTOMER_COUNT + 1):
        segment = rng.choices(
            CUSTOMER_SEGMENTS,
            weights=CUSTOMER_SEGMENT_WEIGHTS,
            k=1,
        )[0]

        region_id = rng.choices(
            CUSTOMER_REGION_IDS,
            weights=CUSTOMER_REGION_WEIGHTS,
            k=1,
        )[0]

        prefix = rng.choice(COMPANY_PREFIXES)
        suffix = rng.choice(COMPANY_SUFFIXES)

        customer_name = f"{prefix} {suffix} {customer_id:03d}"

        customers.append(
            (
                customer_id,
                customer_name,
                segment,
                region_id,
            )
        )

    return customers

def insert_customers(
    connection: sqlite3.Connection,
    customers: list[tuple[int, str, str, int]],
) -> None:
    """Insert generated customers into the database."""

    connection.executemany(
        """
        INSERT INTO customers (
            customer_id,
            customer_name,
            segment,
            region_id
        )
        VALUES (?, ?, ?, ?)
        """,
        customers,
    )

def get_salesperson_weights(month: int) -> list[float]:
    """Return salesperson selection weights for a given month."""

    weights = []

    for salesperson_id in SALESPERSON_WEIGHTS:
        weight = SALESPERSON_WEIGHTS[salesperson_id]

        if month == 9:
            weight *= SEPTEMBER_SALESPERSON_MULTIPLIERS[salesperson_id]

        weights.append(weight)

    return weights

def get_product_weights(month: int) -> list[float]:
    """Return product selection weights for a given month."""

    weights = []

    for product_id in PRODUCT_WEIGHTS:
        weight = PRODUCT_WEIGHTS[product_id]

        if month == 9:
            weight *= SEPTEMBER_PRODUCT_MULTIPLIERS[product_id]

        weights.append(weight)

    return weights

def choose_customer(
    customers: list[tuple[int, str, str, int]],
    month: int,
) -> tuple[int, str, str, int]:
    """Choose a customer using segment and region weighted probabilities."""

    customer_weights = []

    for customer in customers:
        _, _, segment, region_id = customer

        weight = (
            SEGMENT_SALES_WEIGHTS[segment]
            * REGION_SALES_WEIGHTS[region_id]
        )

        if month == 9:
            weight *= (
                SEPTEMBER_SEGMENT_MULTIPLIERS[segment]
                * SEPTEMBER_REGION_MULTIPLIERS[region_id]
            )

        customer_weights.append(weight)

    return rng.choices(
        customers,
        weights=customer_weights,
        k=1,
    )[0]

def generate_quantity(segment: str) -> int:
    """Generate sale quantity according to customer segment."""

    quantity_ranges = {
        "SMB": (1, 3),
        "Mid-Market": (2, 5),
        "Enterprise": (3, 8),
    }

    minimum, maximum = quantity_ranges[segment]

    return rng.randint(minimum, maximum)

def generate_sale_price(base_price: float) -> float:
    """Generate a realistic transaction price around the catalog price."""

    variation = rng.uniform(-0.05, 0.03)

    sale_price = base_price * (1 + variation)

    return round(sale_price, 2)

def generate_sale_date(year: int, month: int) -> str:
    """Generate a random valid date within a given month."""

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    first_day = date(year, month, 1)

    days_in_month = (next_month - first_day).days

    random_day = rng.randint(1, days_in_month)

    return date(year, month, random_day).isoformat()

def generate_sales(
    customers: list[tuple[int, str, str, int]],
) -> list[tuple[int, str, int, int, int, int, float, float]]:
    """Generate synthetic commercial sales for January through September 2026."""

    sales = []
    sale_id = 1

    salesperson_ids = list(SALESPERSON_WEIGHTS.keys())
    product_ids = list(PRODUCT_WEIGHTS.keys())

    product_lookup = {
        product_id: {
            "name": product_name,
            "category": category,
            "unit_price": unit_price,
        }
        for product_id, product_name, category, unit_price in PRODUCTS
    }

    for month, sales_count in MONTHLY_SALES_COUNT.items():
        salesperson_weights = get_salesperson_weights(month)
        product_weights = get_product_weights(month)

        for _ in range(sales_count):
            salesperson_id = rng.choices(
                salesperson_ids,
                weights=salesperson_weights,
                k=1,
            )[0]

            customer = choose_customer(customers, month)

            customer_id = customer[0]
            segment = customer[2]

            product_id = rng.choices(
                product_ids,
                weights=product_weights,
                k=1,
            )[0]

            base_price = product_lookup[product_id]["unit_price"]

            quantity = generate_quantity(segment)
            unit_price = generate_sale_price(base_price)

            total_amount = round(
                quantity * unit_price,
                2,
            )

            sale_date = generate_sale_date(
                year=2026,
                month=month,
            )

            sales.append(
                (
                    sale_id,
                    sale_date,
                    salesperson_id,
                    customer_id,
                    product_id,
                    quantity,
                    unit_price,
                    total_amount,
                )
            )

            sale_id += 1

    return sales

def insert_sales(
    connection: sqlite3.Connection,
    sales: list[tuple[int, str, int, int, int, int, float, float]],
) -> None:
    """Insert generated sales into the database."""

    connection.executemany(
        """
        INSERT INTO sales (
            sale_id,
            sale_date,
            salesperson_id,
            customer_id,
            product_id,
            quantity,
            unit_price,
            total_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sales,
    )

def generate_targets() -> list[tuple[int, int, int, int, float]]:
    """Generate monthly sales targets for each salesperson."""

    targets = []
    target_id = 1

    for month, multiplier in MONTHLY_TARGET_MULTIPLIERS.items():
        for salesperson_id, base_target in BASE_MONTHLY_TARGETS.items():
            target_amount = round(
                base_target * multiplier,
                2,
            )

            targets.append(
                (
                    target_id,
                    salesperson_id,
                    2026,
                    month,
                    target_amount,
                )
            )

            target_id += 1

    return targets

def insert_targets(
    connection: sqlite3.Connection,
    targets: list[tuple[int, int, int, int, float]],
) -> None:
    """Insert generated salesperson targets into the database."""

    connection.executemany(
        """
        INSERT INTO targets (
            target_id,
            salesperson_id,
            year,
            month,
            target_amount
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        targets,
    )

def generate_database() -> None:
    """Generate the complete synthetic commercial SQLite database."""

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    customers = generate_customers()
    sales = generate_sales(customers)
    targets = generate_targets()

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        create_schema(connection)

        insert_regions(connection)
        insert_salespeople(connection)
        insert_products(connection)
        insert_customers(connection, customers)
        insert_sales(connection, sales)
        insert_targets(connection, targets)

        connection.commit()

    print(f"Database generated successfully: {DATABASE_PATH}")

if __name__ == "__main__":
    generate_database()