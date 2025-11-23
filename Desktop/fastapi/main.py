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


from fastapi import Path

@app.get("/items-with-path/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)],
    size: Annotated[float, Query(ge=1, le=100)],
    q: Annotated[str | None, Query(min_length=3, max_length=1000)] = None,
    ):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if size:
        result.update({"size":size})
    return result


from typing import Literal, Annotated
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    model_config= {"extra": "forbid"}
    limit: int = Field(100, ge=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items-based-literal")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.post("/item-multi-params/{item_id}")
async def send_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=100)],
    user: User,
    item: Item = None,
    q: str | None = None,
):
    results= {"item_id": item_id}
    results.update({"user": user})
    if item:
        results.update({"item": item})
    if q:
        results.update({"q":q})
    return results


from fastapi import Body

@app.put("/items-update-body/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.put("/items-embed-body/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title = "The ID of the item to look for")],
    item: Annotated[Item, Body(embed=True)]
):
    results = {"item_id": item_id, "item": item}
    return results


class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", description="The description of the iem", max_length= 100) 
    price: float = Field(default=0.0, title="the price of the item", ge=0.0, le=1000.0)
    tax: float = Field(default=0.0, title="the tax of the item", ge=0.0, le=100.0)

@app.put("/items-field-params/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to fetch")],
    item: Annotated[Item, Body(embed=True)]
):
    result = {"item_id": item_id, "items": item}
    return item


from typing import Union, List, Set

class Item(BaseModel):
    name: Union[str, None]
    description: str | None = Field(default=None, title="The description of the item", description="The description of the iem", max_length= 100) 
    price: float = Field(default=0.0, title="the price of the item", ge=0.0, le=1000.0)
    tax: float = Field(default=0.0, title="the tax of the item", ge=0.0, le=100.0)
    tags: List[str] = []
    unique_tags: Set[str] = set()

@app.put("/items-field-params-list-set/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to fetch")],
    item: Annotated[Item, Body(embed=True)]
):
    result = {"item_id": item_id, "items": item}
    return result


# nested pydantic models

from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: Union[str, None]

class Item(BaseModel):
    name: Union[str, None]
    description: str | None = Field(default=None, title="The description of the item", description="The description of the item", max_length= 100) 
    price: float = Field(default=0.0, title="the price of the item", ge=0.0, le=1000.0)
    tax: float = Field(default=0.0, title="the tax of the item", ge=0.0, le=100.0)
    tags: List[str] = Field(default_factory=list)
    unique_tags: Set[str] = Field(default_factory=set)
    image: Union[Image, None] = Field(default=None)
    images: List[Union[Image, None]] = Field(default=None)

@app.put("/items-field-params-list-set-with-image/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to fetch")],
    item: Annotated[Item, Body(embed=True)]
):
    result = {"item_id": item_id, "items": item}
    return result



# deeply nested pydantic models

from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: Union[str, None]

class Item(BaseModel):
    name: Union[str, None]
    description: str | None = Field(default=None, title="The description of the item", description="The description of the item", max_length= 100) 
    price: float = Field(default=0.0, title="the price of the item", ge=0.0, le=1000.0)
    tax: float = Field(default=0.0, title="the tax of the item", ge=0.0, le=100.0)
    tags: List[str] = Field(default_factory=list)
    unique_tags: Set[str] = Field(default_factory=set)
    image: Union[Image, None] = Field(default=None)
    images: List[Union[Image, None]] = Field(default=None)

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: Union[float, None]
    item: List[Item]

@app.post("/offers/")
async def create_offer(
    offer: Annotated[Offer, Body(embed=True)]
):
    return offer


# create multiple list of images

class Image(BaseModel):
    url: HttpUrl
    name: str | None = None

@app.post("/images/multiple/")
async def create_images(
    index_weights: Union[dict[int, float], None] = Body(default=None),
    images: List[Image] = Body(default_factory=list)
):
    return {"image":images, "weights": index_weights}


# add example using model config

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": 
            [
                {
                "name": "laptop",
                "description": "description of item",
                "price": 1000.10,
                "tax": 10.10
                }
            ]
        }
    }

@app.put("/items-with-modelcongig-examples/{item_id}")
async def update_item(
    item_id: int,
    item: Item
):
    result = {"item_id": item_id, "item": item}
    return result

# add example using pydantic Field

class Item(BaseModel):
    name: str = Field(examples=["laptop"])
    description: Union[str, None] = Field(default=None, examples=["The description of the laptop config"])
    price: float = Field(examples=[1000.10])
    tax: float | None = Field(default=None, examples=[10.10])

@app.put("/items-with-pydantic-examples/{item_id}")
async def update_item(
    item_id: int,
    item: Item
):
    result = {"item_id": item_id, "item": item}
    return result


# add examples with fastapi Body using Annotated

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float | None = None

@app.put("/items-examples-with-body/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[Item, 
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
    )]
):
    return {"item_id": item_id, "item": item}


# examples with openAPI for more example in /docs


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items-example-with-openAPI/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


# more data types in Body

from uuid import UUID
from datetime import datetime, timedelta, time

@app.put("/items-moredatatypes/{item_id}")
async def read_item(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()]
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_datetime
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }

# more datatypes with pydantic

class Item(BaseModel):
    item_id: UUID = Field(examples=["acde070d-8c4c-4f0d-9d8a-162843c10333"])
    start_datetime: datetime = Field(examples=["2025-11-23T17:45:00-05:00"])
    end_datetime: datetime = Field(examples=["2025-11-23T17:45:00-05:10"])
    process_after: timedelta = Field(examples=["0:00:45.123456"])
    repeat_at: time = Field(examples=["00:05:10"])

@app.put("/items-with-pydantic-more-datatypes/{item_id}")
async def update_item(
    item_id: UUID,
    item: Item
):
    start_process = item.start_datetime + item.process_after
    duration = item.end_datetime - item.start_datetime
    result = {"item_id": item_id, "item":item}
    result.update({"start_process":start_process})
    result.update({"duration":duration})
    return result


# store cookies

from fastapi import Cookie

@app.get("/get-users-session/")
async def get_session(
    session_id: Annotated[str | None, Cookie()] = None
):
    return {"session_id": session_id}


# set Headers

from fastapi import Header

@app.get("/get-users-headers/")
async def get_session(
    header: Annotated[str | None, Header()] = None
):
    return {"header": header}


# set multiple Headers

from fastapi import Header

@app.get("/get-multiple-headers/")
async def get_session(
    x_token: Annotated[List[str] | None, Header()] = None
):
    return {"X-Token values": x_token}