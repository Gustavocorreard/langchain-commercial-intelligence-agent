import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "commercial.db"


def validate_table_counts(connection: sqlite3.Connection) -> None:
    """Validate record counts for all core tables."""

    tables = [
        "regions",
        "salespeople",
        "customers",
        "products",
        "sales",
        "targets",
    ]

    print("\nTABLE COUNTS")

    for table in tables:
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count}")


def validate_monthly_sales(connection: sqlite3.Connection) -> None:
    """Show monthly sales volume and revenue."""

    rows = connection.execute(
        """
        SELECT
            strftime('%m', sale_date) AS month,
            COUNT(*) AS sales_count,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        GROUP BY month
        ORDER BY month
        """
    ).fetchall()

    print("\nMONTHLY SALES")

    for month, sales_count, revenue in rows:
        print(
            f"Month {month} | "
            f"Sales: {sales_count} | "
            f"Revenue: {revenue}"
        )

def validate_revenue_by_region(connection: sqlite3.Connection) -> None:
    """Compare August and September revenue by customer region."""

    rows = connection.execute(
        """
        SELECT
            r.region_name,
            strftime('%m', s.sale_date) AS month,
            ROUND(SUM(s.total_amount), 2) AS revenue
        FROM sales AS s
        JOIN customers AS c
            ON s.customer_id = c.customer_id
        JOIN regions AS r
            ON c.region_id = r.region_id
        WHERE strftime('%m', s.sale_date) IN ('08', '09')
        GROUP BY
            r.region_name,
            month
        ORDER BY
            r.region_name,
            month
        """
    ).fetchall()

    print("\nREVENUE BY REGION - AUGUST VS SEPTEMBER")

    for region_name, month, revenue in rows:
        print(
            f"{region_name} | "
            f"Month {month} | "
            f"Revenue: {revenue}"
        )

def validate_revenue_by_segment(connection: sqlite3.Connection) -> None:
    """Compare August and September revenue by customer segment."""

    rows = connection.execute(
        """
        SELECT
            c.segment,
            strftime('%m', s.sale_date) AS month,
            ROUND(SUM(s.total_amount), 2) AS revenue
        FROM sales AS s
        JOIN customers AS c
            ON s.customer_id = c.customer_id
        WHERE strftime('%m', s.sale_date) IN ('08', '09')
        GROUP BY
            c.segment,
            month
        ORDER BY
            c.segment,
            month
        """
    ).fetchall()

    print("\nREVENUE BY SEGMENT - AUGUST VS SEPTEMBER")

    for segment, month, revenue in rows:
        print(
            f"{segment} | "
            f"Month {month} | "
            f"Revenue: {revenue}"
        )

def validate_revenue_by_product(connection: sqlite3.Connection) -> None:
    """Compare August and September revenue by product."""

    rows = connection.execute(
        """
        SELECT
            p.product_name,
            strftime('%m', s.sale_date) AS month,
            COUNT(*) AS sales_count,
            SUM(s.quantity) AS units_sold,
            ROUND(SUM(s.total_amount), 2) AS revenue
        FROM sales AS s
        JOIN products AS p
            ON s.product_id = p.product_id
        WHERE strftime('%m', s.sale_date) IN ('08', '09')
        GROUP BY
            p.product_name,
            month
        ORDER BY
            p.product_name,
            month
        """
    ).fetchall()

    print("\nREVENUE BY PRODUCT - AUGUST VS SEPTEMBER")

    for product_name, month, sales_count, units_sold, revenue in rows:
        print(
            f"{product_name} | "
            f"Month {month} | "
            f"Transactions: {sales_count} | "
            f"Units: {units_sold} | "
            f"Revenue: {revenue}"
        )

def validate_revenue_by_salesperson(connection: sqlite3.Connection) -> None:
    """Compare August and September revenue by salesperson."""

    rows = connection.execute(
        """
        SELECT
            sp.salesperson_name,
            strftime('%m', s.sale_date) AS month,
            COUNT(*) AS sales_count,
            ROUND(SUM(s.total_amount), 2) AS revenue
        FROM sales AS s
        JOIN salespeople AS sp
            ON s.salesperson_id = sp.salesperson_id
        WHERE strftime('%m', s.sale_date) IN ('08', '09')
        GROUP BY
            sp.salesperson_name,
            month
        ORDER BY
            sp.salesperson_name,
            month
        """
    ).fetchall()

    print("\nREVENUE BY SALESPERSON - AUGUST VS SEPTEMBER")

    for salesperson_name, month, sales_count, revenue in rows:
        print(
            f"{salesperson_name} | "
            f"Month {month} | "
            f"Transactions: {sales_count} | "
            f"Revenue: {revenue}"
        )

def validate_target_achievement(connection: sqlite3.Connection) -> None:
    """Compare September actual revenue against salesperson targets."""

    rows = connection.execute(
        """
        SELECT
            sp.salesperson_name,
            ROUND(SUM(s.total_amount), 2) AS actual_revenue,
            ROUND(t.target_amount, 2) AS target_amount,
            ROUND(
                SUM(s.total_amount) / t.target_amount * 100,
                2
            ) AS achievement_rate
        FROM sales AS s
        JOIN salespeople AS sp
            ON s.salesperson_id = sp.salesperson_id
        JOIN targets AS t
            ON t.salesperson_id = s.salesperson_id
            AND t.year = CAST(strftime('%Y', s.sale_date) AS INTEGER)
            AND t.month = CAST(strftime('%m', s.sale_date) AS INTEGER)
        WHERE strftime('%Y-%m', s.sale_date) = '2026-09'
        GROUP BY
            sp.salesperson_name,
            t.target_amount
        ORDER BY
            achievement_rate DESC
        """
    ).fetchall()

    print("\nTARGET ACHIEVEMENT - SEPTEMBER")

    for salesperson_name, actual_revenue, target_amount, achievement_rate in rows:
        status = (
            "Above target"
            if achievement_rate >= 100
            else "Below target"
        )

        print(
            f"{salesperson_name} | "
            f"Actual: {actual_revenue} | "
            f"Target: {target_amount} | "
            f"Achievement: {achievement_rate}% | "
            f"{status}"
        )

def main() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        validate_table_counts(connection)
        validate_monthly_sales(connection)
        validate_revenue_by_region(connection)
        validate_revenue_by_segment(connection)
        validate_revenue_by_product(connection)
        validate_revenue_by_salesperson(connection)
        validate_target_achievement(connection)

        
if __name__ == "__main__":
    main()