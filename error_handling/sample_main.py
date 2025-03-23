from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int):
    if todo_id != 1:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return {"Message": f"To Do Item {todo_id} Found"}

#Test
# curl -X GET http://127.0.0.1:8000/todo/1
# curl -X GET http://127.0.0.1:8000/todo/2
