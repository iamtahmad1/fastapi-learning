from locust import HttpUser, task, between

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user wait time

    @task(3)  # Higher weight to simulate frequent product browsing
    def browse_products(self):
        self.client.get("/products")

    @task(2)  # Simulate adding items to cart
    def add_to_cart(self):
        self.client.post("/add-to-cart", json={"product_id": 1, "quantity": 2})

    @task(1)  # Simulate checkout
    def checkout(self):
        self.client.post("/checkout")
