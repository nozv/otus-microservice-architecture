import uvicorn
from typing import Annotated
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi import APIRouter 
from src.schemas import SUserUpd, SUserGet, SUser, UserDAO
from src.db import get_session

router = APIRouter(prefix="/api/v1")
app = FastAPI(docs_url="/api/v1")

@router.get("/users")
async def get_all_users(session = Depends(get_session)) -> list[SUserGet]:
    return await UserDAO.get_all_users(session=session)
    
@router.get("/user/{user_id}")
async def find_user_by_id(user_id: int, session = Depends(get_session)) -> SUserGet:
    try:
        user = await UserDAO.find_user_by_id(user_id, session=session)
        return user
    except IndexError:
        raise HTTPException(status_code=404)

@router.post("/user/")
async def create_user(user: SUser, session = Depends(get_session)) -> Response:
    try:
        user_id = await UserDAO.create_user(user, session=session)
        return JSONResponse({"id": user_id})
    except ValueError:
        return HTTPException(status_code=409, detail="Incorrect username")

@router.put("/user/{user_id}")
async def update_user(user_id: int, user: SUserUpd, session = Depends(get_session)) -> SUserGet:
    try:
        user = await UserDAO.update_user(user_id, user, session)
        return user
    except IndexError:
        raise HTTPException(status_code=404)
    
@router.delete("/user/{user_id}")
async def delete_user(user_id: int, session = Depends(get_session)) -> Response:
    try:
        await UserDAO.delete_user(user_id, session)
        return Response(status_code=200)
    except IndexError:
        raise HTTPException(status_code=404)
    

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
