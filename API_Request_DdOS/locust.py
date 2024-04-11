from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    # def on_start(self):
    #     self.client.post("/auth/sign-in", {
    #         "Email": "admin@gmail.com",
    #         "Password": "123123123"
    #     })

    def on_start(self):
        self.client.get("/get-message?key=Order&value=Linh")
        #self.client.get("/save_message?get=2&text=Linh")
        #self.client.get("/just_send_request")
        
    
    @task
    def index(self):
        self.client.get("/")

        
    # @task
    # def about(self):
    #     self.client.get("/api/auth/require-token")