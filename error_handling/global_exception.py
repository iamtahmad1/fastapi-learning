from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"error": exc.detail, "path": request.url.path}
  )  

@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int):
    if todo_id != 1:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return {"Message": f"To Do Item {todo_id} Found"}