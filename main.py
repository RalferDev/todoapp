import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from Item import Item
import ItemService

# comando da shell per avviare: uvicorn main:app --reload
# per usare swagger usare http://127.0.0.1:8000/docs#/

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Metodo per il caricamento della View
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "hello": "lota"})


# Metodo per il caricamento della View
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Metodo per il caricamento della View
@app.get("/create", response_class=HTMLResponse)
def create_item_form(request: Request):
    return templates.TemplateResponse("create_item.html", {"request": request})


# Metodo per il caricamento della View
@app.get("/get", response_class=HTMLResponse)
def get_item_form(request: Request):
    return templates.TemplateResponse("get_item.html", {"request": request, "item": None})


# Metodo per il caricamento della View
@app.get("/update", response_class=HTMLResponse)
def update_item_form(request: Request):
    return templates.TemplateResponse("update_item.html", {"request": request})


# Metodo per il caricamento della View
@app.get("/delete", response_class=HTMLResponse)
def delete_item_form(request: Request):
    return templates.TemplateResponse("delete_item.html", {"request": request, "item": None})

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("error.html", {"request": request}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse("error.html", {"request": request}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/items", response_class=HTMLResponse)
async def list_items_view(request: Request, limit: int = Query(10, alias="limit")):
    items = await ItemService.list_items(limit)
    return templates.TemplateResponse("list_items.html", {"request": request, "items": items})


@app.get("/get_item", response_class=HTMLResponse)
async def get_item_view(request: Request, item_text: str = Query(...)):
    item = await ItemService.get_item(item_text)
    return templates.TemplateResponse("get_item.html", {"request": request, "item": item})


@app.post("/create_item", response_class=HTMLResponse)
async def create_item(request: Request, text: str = Form(...), is_done: bool = Form(False)):
    item = Item(text=text, is_done=is_done)
    result = await ItemService.create_item(item)
    if result:
        return templates.TemplateResponse("create_item.html", {"request": request, "item": item})
    else:
        raise HTTPException(status_code=500, detail="Errore nella creazione dell'elemento")


@app.post("/update_item", response_class=HTMLResponse)
async def update_item(request: Request, text: str = Form(...), is_done: bool = Form(False)):
    item = Item(text=text, is_done=is_done)
    result = await ItemService.update_item(item)
    if result:
        return templates.TemplateResponse("update_item.html", {"request": request, "item": item})
    else:
        raise HTTPException(status_code=500, detail="Errore nell'aggiornamento dell'elemento")


@app.post("/delete_item", response_class=HTMLResponse)
async def delete_item_view(request: Request, text: str = Form(...)):
    result = await ItemService.delete_item(text)
    if result:
        return templates.TemplateResponse("delete_item.html", {"request": request, "item": result})
    else:
        raise HTTPException(status_code=404, detail=f"item with text '{text}' not found")


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
