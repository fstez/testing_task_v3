from locust import HttpUser, task, between
import random
import string

def random_user():
    # Genereerib juhusliku kasutajanime
    return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def fast_page(self):
        self.client.get("/fast")
    
    @task
    def medium_page(self):
        self.client.get("/medium")
    
    @task
    def slow_page(self):
        self.client.get("/slow")
    
    @task
    def register(self):
        uname = random_user()
        pw = "testpass123"
        self.client.post("/api/register", json={"username": uname, "password": pw})
    
    @task
    def login(self):
        uname = "testuser" # testuser peab olema olemas! Või loo jooksvalt
        pw = "testpass123"
        self.client.post("/api/login", json={"username": uname, "password": pw})
    
    @task
    def create_todo(self):
        todo = {"title": "Test ülesanne", "description": "Automaatne", "priority": "medium"}
        self.client.post("/api/todos", json=todo)
    
    @task
    def get_todos(self):
        self.client.get("/api/todos")
    
    @task
    def update_todo(self):
        # Eeldab olemasolevat todo id-d (1), testimiseks võib olla vaja salvestada id!
        self.client.put("/api/todos/1", json={"title": "Uuendatud", "completed": True})
    
    @task
    def delete_todo(self):
        self.client.delete("/api/todos/1")
    
    @task
    def change_password(self):
        self.client.post("/api/change-password", json={"old_password": "testpass123", "new_password": "testpass456"})