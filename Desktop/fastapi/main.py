from fastapi import FastAPI, Depends, Header, Path, HTTPException, status
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

async def get_db_session():
    print("get DB session")
    session = {"data": {1: {"name": "item one"}, 2: {"name": "item two"}}}
    try:
        yield session
    finally:
        print("DB session closed") 

DBsession = Annotated[dict, Depends(get_db_session)]

async def get_user(token: Annotated[str | None, Header()] = None):
    print("Checking Auth...")
    user = {"user_name": "test_user"}
    return user

CurrentUser = Annotated[dict, Depends(get_user)]

class ItemCreate(BaseModel):
    name: str
    price: float | None = None


@app.get("/item/{item_id}")
async def read_item(
    item_id: Annotated[int,  Path(ge=1)], 
    db: DBsession
    ):
    print("reading items...")
    if item_id not in db["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item is not present")
    return {"id": item_id, **db["data"][item_id]}


@app.post("/item")
async def create_item(
    item: ItemCreate,
    db: DBsession,
    user: CurrentUser
    ):
    print(f"User {user['user_name']} creating item {item.name}")
    new_id = max(db["data"].keys() or [0]) + 1
    db["data"][new_id] = item.model_dump()
    return {"id": new_id, **item.model_dump()}
