from fastapi import HTTPException

from DbConnection import collection
from Item import Item


async def create_item(item: Item):
    result = await collection.insert_one(item.model_dump())
    if result.acknowledged:
        return item
    else:
        raise HTTPException(status_code=500, detail="Errore nella creazione dell'elemento")


async def list_items(limit: int):
    items_cursor = collection.find().limit(limit)
    items = await items_cursor.to_list(length=limit)
    return items


async def get_item(item_text: str):
    item = await collection.find_one({"text": item_text})
    if item:
        return Item(**item)
    else:
        raise HTTPException(status_code=404, detail=f"item {item_text} not found")


async def update_item(item: Item):
    result = await collection.update_one({"text": item.text}, {"$set": item.model_dump()})
    if result.matched_count:
        return item
    else:
        raise HTTPException(status_code=404, detail=f"item with text '{item.text}' not found")


async def delete_item(text: str):
    result = await collection.find_one_and_delete({"text": text})
    if result:
        return Item(**result)
    else:
        raise HTTPException(status_code=404, detail=f"item with text '{text}' not found")
