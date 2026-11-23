from flask import Flask, request, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Read database settings from environment variables.
DB_HOST = os.getenv("DB_HOST", "database")
DB_NAME = os.getenv("DB_NAME", "ecommerce")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_connection():
    """Create a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


def initialize_database():
    """Create the orders table when the service starts."""

    # Retry because PostgreSQL may take time to start.
    for attempt in range(15):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    customer_name VARCHAR(100),
                    product_id INTEGER,
                    quantity INTEGER,
                    total_price DECIMAL(10,2)
                );
            """)

            connection.commit()
            cursor.close()
            connection.close()

            print("Database initialized successfully")
            return

        except Exception as error:
            print(f"Database connection attempt " f"{attempt + 1} failed: {error}")
            time.sleep(2)

    raise RuntimeError("Could not connect to database")


@app.route("/orders", methods=["POST"])
def create_order():
    """Validate and save a new customer order."""

    data = request.get_json(silent=True) or {}

    customer_name = data.get("customer_name")
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    total_price = data.get("total_price")

    # Check that the required order fields are provided.
    if not all([customer_name, product_id, quantity, total_price]):
        return jsonify({"error": "Missing required order information"}), 400

    try:
        product_id = int(product_id)
        quantity = int(quantity)
        total_price = float(total_price)

        if quantity <= 0 or total_price <= 0:
            raise ValueError("Quantity and price must be positive")

        connection = get_connection()
        cursor = connection.cursor()

        # Parameterized SQL keeps input values separate from the query.
        cursor.execute(
            """
                INSERT INTO orders
                (customer_name, product_id, quantity, total_price)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """,
            (customer_name, product_id, quantity, total_price),
        )

        order_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()

        return (
            jsonify({"message": "Order created successfully", "order_id": order_id}),
            201,
        )

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid order information"}), 400

    except Exception:
        app.logger.exception("Order creation failed")

        return jsonify({"error": "Could not create order"}), 500


@app.route("/orders", methods=["GET"])
def get_orders():
    """Retrieve saved orders, newest first."""

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, customer_name, product_id,
                   quantity, total_price
            FROM orders
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        orders = []

        for row in rows:
            orders.append(
                {
                    "id": row[0],
                    "customer_name": row[1],
                    "product_id": row[2],
                    "quantity": row[3],
                    "total_price": float(row[4]),
                }
            )

        cursor.close()
        connection.close()

        return jsonify(orders)

    except Exception:
        app.logger.exception("Could not retrieve orders")

        return jsonify({"error": "Could not retrieve orders"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Check whether PostgreSQL is reachable."""

    try:
        connection = get_connection()
        connection.close()

        return jsonify(
            {"status": "healthy", "service": "order-service", "database": "connected"}
        )

    except Exception:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "service": "order-service",
                    "database": "disconnected",
                }
            ),
            503,
        )


if __name__ == "__main__":
    # Initialize the database before accepting requests.
    initialize_database()

    app.run(host="0.0.0.0", port=5002)
