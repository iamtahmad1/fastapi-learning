from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException


app = FastAPI()

class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": f"Item with ID {exc.item_id} not found"}
    )

@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int):
    if todo_id != 1:
        raise ItemNotFoundException(todo_id)
    return {"Message": f"To Do Item {todo_id} Found"}