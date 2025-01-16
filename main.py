from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

import schemas
from deps import get_token
from utils import (
    generate_video_with_prompt,
    generate_video_with_taskid,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root():
    return schemas.Response()

@app.post("/generate")
async def generate_with_video_description(
    data: schemas.DescriptionModeGenerateParam, token: str = Depends(get_token)
):
    try:
        resp = await generate_video_with_prompt(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/task")
async def generate_with_video_task(
    data: schemas.TaskParam, token: str = Depends(get_token)
):
    try:
        resp = await generate_video_with_taskid(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )