from fastapi import Depends, HTTPException, status, FastAPI

app = FastAPI()

# Fake authentication function
def get_current_user(api_key: str = "mysecurekey"):
    if api_key != "mysecurekey":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return {"user": "admin"}

# Inject authentication into routes using `Depends`
@app.get("/secure-data")
async def secure_data(user: dict = Depends(get_current_user)):
    return {"message": "This is secured", "user": user}
