from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"tem_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "I am the current user"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}


from enum import Enum

class Priority(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"

@app.get("/priority/{priority_name}")
async def get_prority(priority_name: Priority):
    if priority_name == priority_name.high:
        return {"priority_is": priority_name}
    return {"all_priority": list(Priority)}


@app.get("/files/{file_path:path}")
async def get_files(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def get_all_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip+limit]


@app.get("/item/{item_id}")
async def all_items(item_id: str, q: str | None = None, short: bool = False):
    if q:
        return {"item_id": item_id, "q": q}
    if not short:
        return {"description": "This is a short description"}
    return {"item_id": item_id}


@app.get("/user/{user_id}/item/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: str | None = None, need_desc: bool = False):
    item = {"item_id": item_id, "user_id": user_id}
    if q:
        item.update({"q": q})
    if need_desc:
        item.update({"need_dec": "This item needs a description"})
    return item
    

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None


@app.post("/item-pydantic/")
async def create_items(item: Item):
    item_dict = item.dict()
    if item.tax:
        item_price = f"Name of the item is {item.name}, it has a total price of {item.price + item.tax}"
        item_dict.update({"total_desc":item_price})
    else:
        item_price = f"Name of the item is {item.name}, it has a total price of {item.price}"
        item_dict.update({"total_desc": item_price})
    return item_dict


@app.put("/item-pydantic/{item_id}")
async def update_items(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@app.put("/item-pydantic-new/{item_id}")
async def update_items(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


from fastapi import Query
from typing import Annotated

@app.put("/item-pydantic-new-query-parm/{item_id}")
async def update_items(item_id: int, item: Item, q: Annotated[str | None , Query(min_length=10)]= None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items-multi-val/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=10)]= None):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-multi-val-regex/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=10, pattern = "^fixedquery$")] = None
    ):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-multi-val-fixed/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=10)] = "fixedquery"
    ):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-multi-val-req/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=10)]
    ):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-multi-query-list/")
async def red_items(
    q: Annotated[list[str] | None, Query()] = None
):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-multi-query-list-def/")
async def red_items(
    q: Annotated[list[str], Query()] = ["one", "two", "three"]
):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-addition-metadata/")
async def read_items(
    q: Annotated[str | None, Query(
        title = "Query to read data",
        description = "Query string for the items to search in the database that have a good match",
        min_length = 3,
        alias="item-query")] = None
    ):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-addition-metadata-deprecated/")
async def read_items(
    q: Annotated[str | None, Query(
        title = "Query to read data",
        description = "Query string for the items to search in the database that have a good match",
        min_length = 3,
        alias="item-query",
        pattern="^fixedquery$",
        deprecated=True)] = None
    ):
    data = {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}
    if q:
        data.update({"q": q})
    return data


@app.get("/items-include-in-schema/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = "hello",
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}


from pydantic import AfterValidator
import random

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_validation(id: str):
    if not id.startswith(("isbn", "imdb")):
        raise ValueError("Invalid ID format")
    return id

@app.get("/item-custom-validation")
async def get_valid_items(
    id: Annotated[str | None, AfterValidator(check_validation)] = None
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
