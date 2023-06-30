from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from ..dependencies import QueryParams
from bson import ObjectId
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta
import json, os

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

client = MongoClient(os.getenv('ME_CONFIG_MONGODB_URL'))
db = client["file_storage"]
collection = db["files"]
collection.create_index("expire_at", expireAfterSeconds=30 * 24 * 60 * 60)

def get_mongo_file(file_id: str, commons):
    file_data = collection.find_one({"_id": ObjectId(file_id)})
    if not file_data:
        return JSONResponse(
            status_code=404,
            content={"message": "File not found"},
        )
    if file_data["filename"].endswith(".xlsx") or file_data["filename"].endswith(".xls"):
        df = pd.read_excel(file_data["content"])
    elif file_data["filename"].endswith(".csv"):
        df = pd.read_csv(file_data["content"])
    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Only allow file type with .xls/.xlsx/.csv"},
        )
    if commons:
        df = df.iloc[commons.skip:commons.limit+commons.skip]
    json_data = df.to_json(orient="records")
    return json.loads(json_data)

@router.post("/uploadfile", responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "filename": "string",
                    "file_id": "string"
                }
            }
        }
    }
})
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        # raise HTTPException(status_code=400, message="No upload file sent")
        return JSONResponse(
            status_code=400,
            content={"message": "No upload file sent"},
        )
        # return {"message": "No upload file sent"}
    else:
        contents = await file.read()
        file_data = {
            "filename": file.filename,
            "content": contents,
            "expire_at": datetime.utcnow() + timedelta(days=30)
        }
        result = collection.insert_one(file_data)

        return {"filename": file.filename, "file_id": str(result.inserted_id)}

@router.get("/{file_id}", responses={
    200: {
        "content": {
            "application/json": {
                "example": [{
                    "column1": "string",
                    "column2": "string",
                    "column3": "string"
                }]
            }
        }
    },
    404: {"description": "File not found"}
})
async def get_file(file_id: str, commons: QueryParams = Depends(QueryParams)):
    return get_mongo_file(file_id, commons)