from locust import HttpUser, task, between

class APILoadTest(HttpUser):
    wait_time = between(1, 5)  # Simulates wait time between requests

    @task
    def send_purchase_request(self):
        """Simulate a purchase request to the API Gateway."""
        payload = {
            "buyer_id": "123",
            "product_id": "456",
            "number_of_installments": 3,
            "total_amount": 150.75,
            "purchase_date": "2024-01-01"
        }
        with self.client.post("/purchase", json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                response.success()
