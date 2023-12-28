from locust import FastHttpUser, task, constant, SequentialTaskSet, events
import locust_plugins.listeners
import random
from common import api, utils

class NormalUser(FastHttpUser):
    host = "https://dummyjson.com"
    
    @events.init.add_listener
    def on_locust_init(environment, **kwargs):
        # make sure this is the last request event handler you register, as later ones will not get triggered
        # if there is a failure
        locust_plugins.listeners.InterruptTaskOnFail(environment)
    
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = constant(5)
        
        def on_start(self):
            self.username, self.password = utils.get_user_data()
            self.api = api.Api(self.client)
            
        @task
        def login(self):
            with self.api.login(self.username, self.password, "1_login") as response:
                try:
                    # Verify
                    if response.json()['token'] == None:
                        response.failure(f"Cannot login \n Response: {response.text}")
                    # Correlate token
                    self.header = {
                        'Authorization': f'Bearer {response.json()['token']}', 
                        'Content-Type': 'application/json'
                    }
                except Exception as error:
                    response.failure(f"An exception occurred: {error} \n Response: {response.text}")

        @task
        def view_products(self):
            with self.api.view_products(self.header, "2_view_product_list") as response:
                try:
                    # Verify
                    if response.json()['products'] == None:
                        response.failure(f"Incorrect data \n Response: {response.text}")
                    # Correlate product
                    products = response.json()['products']
                    product = random.choice(products)
                    self.product_id = product['id']
                    self.product_name = product['title']
                except Exception as error:
                    response.failure(f"An exception occurred: {error} \n Response: {response.text}")
        
        @task
        def view_product(self):
            with self.api.view_product_by_id(self.header, self.product_id, "3_view_product") as response:
                try:
                    # Verify
                    if response.json()['title'] != self.product_name:
                        response.failure("Incorrect data" 
                                        + f"\n ID: {self.product_id}"
                                        + f"\n Title: {self.product_name}"
                                        + f"\n Response: {response.text}")
                except Exception as error:
                    response.failure(f"An exception occurred: {error} \n Response: {response.text}")
