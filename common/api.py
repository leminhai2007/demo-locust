class Api:
    def __init__(self, client):
        self.client = client

    def login(self, username: str, password: str, group_name: str):
        body = {
                'username': username,
                'password': password
            }
        return self.client.post('/auth/login', json = body, catch_response=True, name=group_name)

    def view_products(self, header, group_name: str):
        return self.client.get('/products', header=header, catch_response=True, name=group_name)

    def view_product_by_id(self, header, product_id, group_name: str):
        return self.client.get(f'/product/{product_id}', header=header, catch_response=True, name=group_name)
