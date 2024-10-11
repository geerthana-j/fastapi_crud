from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from typing import List, Optional

app = FastAPI()

# Replace with your actual MongoDB connection string
client = MongoClient("mongodb+srv://geerthikumar:f3rk02JZjpHfJ3z4@cluster0.3o1mx9f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# MongoDB setup
db = client.fastapi_db
items_collection = db.items
clock_in_collection = db.clock_in_records

# Pydantic models
class Item(BaseModel):
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: str  # format YYYY-MM-DD

class ClockInRecord(BaseModel):
    email: EmailStr
    location: str

# Convert ObjectId to str
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"],
        "insert_date": item["insert_date"],
    }

def clock_in_record_helper(record) -> dict:
    return {
        "id": str(record["_id"]),
        "email": record["email"],
        "location": record["location"]
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>API Documentation</title>
        </head>
        <body>
            <h1>Welcome to the FastAPI Application</h1>
            <p>You can view the API documentation at <a href="/docs">this link</a>.</p>
        </body>
    </html>
    """

# Item APIs
@app.post("/items", response_model=dict)
def create_item(item: Item):
    item_data = item.dict()
    item_data['expiry_date'] =  datetime.fromisoformat(item_data['expiry_date'])
    item_data["insert_date"] = datetime.now()
    result = items_collection.insert_one(item_data)  # Correctly await the function
    return {"id": str(result.inserted_id)}

@app.get("/items/filter", response_model=List[dict])
def filter_items(email: Optional[str] = None, expiry_date: Optional[str] = None, 
                       insert_date: Optional[str] = None, quantity: Optional[int] = None):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt":  datetime.fromisoformat(expiry_date)}
    if insert_date:
        query["insert_date"] = {"$gt": datetime.fromisoformat(insert_date)}
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}
    
    print(query)

    aggregation_pipeline = [
        {"$match": query},  
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    
    aggregation_result = []
    for doc in items_collection.aggregate(aggregation_pipeline):
        aggregation_result.append(doc)

    return aggregation_result
    

@app.get("/items/{item_id}", response_model=dict)
def read_item(item_id: str):
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(item)


@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    result = items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

@app.put("/items/{item_id}", response_model=dict)
def update_item(item_id: str, item: Item):
    updated_item = {k: v for k, v in item.dict().items()}
    if 'insert_date' in updated_item:
        updated_item.pop('insert_date')
    result = items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated"}

# Clock-In APIs
@app.post("/clock-in", response_model=dict)
def create_clock_in(record: ClockInRecord):
    record_data = record.dict()
    record_data["insert_datetime"] = datetime.now()
    result = clock_in_collection.insert_one(record_data)
    return {"id": str(result.inserted_id)}


@app.get("/clock-in/filter", response_model=List[dict])
def filter_clock_in(email: Optional[str] = None, location: Optional[str] = None, 
                          insert_datetime: Optional[str] = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": datetime.fromisoformat(insert_datetime)}
    
    records = []
    for record in clock_in_collection.find(query):
        records.append(record)
    result = []
    for record in records:
        result.append(clock_in_record_helper(record))
    return result

@app.get("/clock-in/{record_id}", response_model=dict)
def read_clock_in(record_id: str):
    print(f'Record Id {record_id}')
    record = clock_in_collection.find_one({"_id": ObjectId(record_id)})
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return clock_in_record_helper(record)


@app.delete("/clock-in/{record_id}")
def delete_clock_in(record_id: str):
    result = clock_in_collection.delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}

@app.put("/clock-in/{record_id}", response_model=dict)
def update_clock_in(record_id: str, record: ClockInRecord):
    updated_record = {k: v for k, v in record.dict().items()}
    if 'insert_datetime' in updated_record:
        updated_record.pop('insert_datetime')
    result = clock_in_collection.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record updated"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
