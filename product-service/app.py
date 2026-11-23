from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200, "stock": 10},
    {"id": 2, "name": "Smartphone", "price": 800, "stock": 15},
    {"id": 3, "name": "Headphones", "price": 100, "stock": 25},
    {"id": 4, "name": "Keyboard", "price": 50, "stock": 30},
]


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Service API</title>
    </head>
    <body>
        <h1>Product Service API</h1>
        <p>Welcome to the E-Commerce Product Microservice.</p>

        <h2>Available Endpoints</h2>
        <ul>
            <li>
                <a href="/products">View All Products</a>
            </li>
            <li>
                <a href="/products/1">View Product 1 (Laptop)</a>
            </li>
            <li>
                <a href="/health">Check Service Health</a>
            </li>
        </ul>
    </body>
    </html>
    """


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "product-service"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
