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

# Cookies with pydantic models

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    session_id: str
    click_tracker: str | None = None
    ads_tracker: str | None = None

@app.get("/items-cookies-pydantic/")
async def get_cookies(
    cookies: Annotated[Cookies, Cookie()]
):
    return cookies

# The above way doesnt work, Pydantic models cannot be auto-populated from cookies because they require a JSON object, and cookies do not support nested structures


class Cookies(BaseModel):
    session_id: str
    click_tracker: str | None = None
    ads_tracker: str | None = None

@app.get("/items-cookies-pydantic-new/")
async def get_cookies(
    session_id: Annotated[str, Cookie()],
    click_tracker: Annotated[str | None, Cookie()] = None,
    ads_tracker: Annotated[str | None, Cookie()] = None,
):
    return Cookies(
        session_id=session_id,
        click_tracker=click_tracker,
        ads_tracker=ads_tracker,
    )


# Headers with pydantic model

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    x_tag: List[str] = []

@app.get("/multiple_headers_pydantic/")
async def get_multiple_headers(
    headers: Annotated[CommonHeaders, Header()]
):
    return headers


# response model

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float 
    tax: float | None = None
    tag: List[str] = []

@app.post("/items-with-response-model/", response_model= Item)
async def create_item(item: Item) -> Item:
    return item

@app.get("/items-with-response-model/", response_model= List[Item])
async def read_item() -> Item:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# email validator and input and output models
from pydantic import EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = Field(default=None)

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = Field(default=None)

@app.post("/get-userid-password/", response_model=UserOut)
async def get_user(user_input: UserIn) -> UserOut:
    return user_input


# filter data (password) in fastapi with interetance

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = Field(default=None)    

class UserIn(BaseUser):
    password: str

@app.post("/create-user-with-inheritance/", response_model=BaseUser)
async def create_user(user: UserIn):
    return user

# fast API Response and Redirect Responses

from fastapi import Response
from fastapi.responses import RedirectResponse, JSONResponse

@app.get("/use-response-in-output/")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=EEDYFSwegvM")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

# get redirect response
@app.get("/teleport-redirect-response/")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# disable the responsemodel for multple output like dict or a pydantic type output

@app.get("/use-response-in-output-disable-responsemodel/", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=EEDYFSwegvM")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


# only get values other than default values

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/get-items-without-default-set/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_non_default(item_id: str):
    return items[item_id]


# explicitly set response model to include and exclude attributes

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get(
    "/items-explicitly-set-include/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items-explicitly-set-include/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# defining extra models and functions

class BaseUser(BaseModel):
    user_name: str
    email: EmailStr
    
    full_name: str | None = None

class UserIn(BaseUser):
    password: str

class UserOut(BaseUser):
    pass

class UserInDB(BaseUser):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "hash_key" + raw_password

def save_in_db(user_input: UserIn):
    hashed_password = fake_password_hasher(user_input.password)
    user_in_db = UserInDB(**user_input.model_dump(), hashed_password=hashed_password)
    return user_in_db

@app.post("/save-user-details-password-in-db/", response_model=UserOut)
async def save_user(user_in: UserIn):
    save_to_db = save_in_db(user_in)
    print("User saved! ..not really")
    return save_to_db


# multiple output models using Union


class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items-multiple-model-results/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


# status code

from fastapi import status

@app.post("/send-item-with-status-code/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# send form data like password

from fastapi import Form

@app.post("/send-use-login-through-form/")
async def create_user_login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    return {"username": username}


# form pydantic model with config

class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@app.post("/login-with-model-config/", response_model=FormData ,response_model_exclude={"password"})
async def login(data: Annotated[FormData, Form()]):
    return data


# upload files

from fastapi import File, UploadFile

@app.post("/create-files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file": len(file)}

@app.post("/upload-file/")
async def upload_file(file: UploadFile):
    return {"file": file.filename, "content": file.content_type}


# upload multiple files with metadata

from fastapi.responses import HTMLResponse

@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}

@app.get("/view-form-data")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


# both files and forms

@app.post("/files-form-data/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


# HTTP exceptions with custom headers

from fastapi import HTTPException

items = {"foo": "sampleitem"}

@app.get("/item-with-httpexception/{item_id}")
async def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, 
                            detail="Item not found", 
                            headers={"X-Error": "There goes my error"}
                            )
    return {"item": items[item_id]}


# HTTP exceptions with built-in exceptions and validation errors

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items-built-in-exception-handlers/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


# HTTP exceptions with full custom exceptions and validation errors

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(StarletteHTTPException)
async def custom_http_execption_handler(request, exc):
    print(f"This is the custom exception handler : {exc}")  # logging
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "custom_http_error",
            "message": str(exc.detail),
            "status_code": exc.status_code,
        },
    )

@app.exception_handler(RequestValidationError)
async def data_validation_exception_handler(request, exc: RequestValidationError):
    print(f"The Data validation error is as follows: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "messages": exc.errors(),   # list of error details
            "body": exc.body,           # original input (if available)
        },
    )


@app.get("/item-with-full-custom-http-validation-exceptions/{item_id}")
async def get_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Not allowed to access")
    return {"item_id": item_id}


# path operation parameters 

# 1) Enum for tag values in the data
class ItemTag(str, Enum):
    items = "items"
    users = "users"

# 2) Request/response model
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    # list of enum tags, optional
    tags: List[ItemTag] = Field(default_factory=list)

@app.post(
    "/send-item-details-with-tags/",
    response_model=Item,
    tags=["items"],  # docs grouping (could also be [ItemTag.items.value])
    summary="Create a new item",
    response_description="Created an item",
    deprecated=True,
)
async def create_an_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get(
    "/get-items-details-with-tags/",
    summary="Gets all items",
    description="Gets all items with all the information, name, description, price, tax and a set of unique tags",
    tags=["items"],  # docs group
)
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get(
    "/get-users-details-with-tags/",
    summary="Gets all users",
    tags=["users"],  # docs group
)
async def read_users():
    return [{"username": "johndoe"}]


# Encoding as JSON for DB compatibility which only accepts JSON

from fastapi.encoders import jsonable_encoder

fake_db= {}

class Item(BaseModel):
    name: str
    description: str | None = None
    timestamp: datetime

@app.put("/db-update-with-json/{id}")
async def update_db_item(id: str, item: Item):
    json_for_db = jsonable_encoder(item)
    fake_db[id] = json_for_db
    return fake_db


# using patch to only update the required field instead of everything using put, by only fetching the records we need

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items-get-for-patch/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items-get-for-patch/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


# Dependancy injection

from fastapi import Depends

async def common_parameters(q : str, skip : int = 0, limit : int = 100):
    return {"q": q, "skip": skip, "limit": limit}

common_deps = Annotated[dict, Depends(common_parameters)]

@app.get("/items-get-common-parameters/")
async def read_items(common: common_deps):
    return common

@app.get("/users-get-common-parameters/")
async def read_users(common: common_deps):
    return common

# using class to define a dependancy (any callable can be used as a dependacy)

class CommonParameters:
    def __init__(self, q: str, skip : int = 0, limit : int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/get-items-with-class-dependacies/")
# async def read_items(commons: Annotated[CommonParameters, Depends(CommonParameters)]):
# or we could just write
async def read_items(commons: Annotated[CommonParameters, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    selected_items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": selected_items})
    return response


# dependancies and sub-dependancies, use use_cache to store in cache

def query_extractor(q : str | None = None):
    return q

def query_or_cookie_extractor(
        q: Annotated[str, Depends(query_extractor)],
        last_query: Annotated[str | None, Cookie()] = None
        ):
    if not q:
        return last_query
    return q

@app.get("/get-items-with-multiple-subqueries/")
async def read_items(
    query_or_cookie: Annotated[str, Depends(query_or_cookie_extractor, use_cache=False)],
    ):
    return {"query_or_cookie": query_or_cookie}

# multiple dependancies in path operation decorator where execution isnt needed

async def validate_token(x_token: Annotated[str, Header()]):
    if x_token != "secret_token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")
    

async def validate_key(x_key: Annotated[str, Header()]):
    if x_key != "secret_key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid")
    return x_key

@app.get("/get-items-after-validation/", dependencies=[Depends(validate_key), Depends(validate_token)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

# can also define dependancies for the whole application like the below example

# from fastapi import Depends, FastAPI, Header, HTTPException
# from typing_extensions import Annotated


# async def verify_token(x_token: Annotated[str, Header()]):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def verify_key(x_key: Annotated[str, Header()]):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key


# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


# @app.get("/items/")
# async def read_items():
#     return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


# @app.get("/users/")
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


# dependancy with yield

data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}

class OwnerError(Exception):
    pass

def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")
    
@app.get("/items-with-yield/{item_id}")
async def get_items(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item

# dependancy with yeild and scope = Function for execution of yeild before sending response to client

def get_username():
    try:
        yield "Rick"
    finally:
        print("Cleanup up before response is sent")

@app.get("/users-with-scope-function/me")
def get_user_me(username: Annotated[str, Depends(get_username, scope="function")]):
    return username

# dependancy with yeild and scope = request (default) for execution of yeild after sending response to client

def get_username():
    try:
        yield "Rick"
    finally:
        print("Cleanup up after response is sent")

@app.get("/users-with-scope-request/me")
def get_user_me(username: Annotated[str, Depends(get_username, scope="request")]):
    return username

#       INFO   Waiting for application startup.
#       INFO   Application startup complete.
# Cleanup up before response is sent
#       INFO   127.0.0.1:53888 - "GET /users-with-scope-function/me HTTP/1.1" 200
#       INFO   127.0.0.1:53888 - "GET /users-with-scope-request/me HTTP/1.1" 200
# Cleanup up after response is sent

