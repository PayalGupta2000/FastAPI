from fastapi import FastAPI, Depends, HTTPException, status
from models.models  import User
from handle_password.security import  create_access_token
from database.db import authenticate_user, create_user, get_user, update_user, delete_user
from Authentication.auth import get_current_user

app = FastAPI()

@app.post("/token")
async def login_for_access_token(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

@app.post("/users/")
async def create_user_endpoint(user: User):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = create_user(user.dict())
    return {"user_id": str(user_id)}

@app.get("/users/{username}", response_model=User)
async def read_user(username: str):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{username}", response_model=User)
async def update_user_endpoint(username: str, user: User):
    existing_user = get_user(username)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    updated_count = update_user(username, update_data)
    if not updated_count:
        raise HTTPException(status_code=500, detail="Could not update user")
    return get_user(username)

@app.delete("/users/{username}", response_model=dict)
async def delete_user_endpoint(username: str):
    existing_user = get_user(username)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_count = delete_user(username)
    if not deleted_count:
        raise HTTPException(status_code=500, detail="Could not delete user")
    return {"message": "User deleted successfully"}
