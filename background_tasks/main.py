import time
from fastapi import FastAPI, Request, BackgroundTasks

app = FastAPI()

def log_user_activity(ip: str, endpoint: str, method: str):
    time.sleep(1)  # Simulating a slow log operation
    with open("user_activity_logs.txt", "a") as f:
        f.write(f"IP: {ip}, Method: {method}, Endpoint: {endpoint}\n")

@app.get("/items/")
async def get_items(request: Request, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(log_user_activity, request.client.host, request.url.path, request.method)
    return {"message": "Here are your items!"}

@app.post("/create/")
async def create_item(request: Request, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(log_user_activity, request.client.host, request.url.path, request.method)
    return {"message": "Item created successfully!"}

@app.put("/update/")
async def update_item(request: Request, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(log_user_activity, request.client.host, request.url.path, request.method)
    return {"message": "Item updated successfully!"}

@app.delete("/delete/")
async def delete_item(request: Request, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(log_user_activity, request.client.host, request.url.path, request.method)
    return {"message": "Item deleted successfully!"}