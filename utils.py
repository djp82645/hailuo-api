import json
import os
import aiohttp
from loguru import logger
from cache import cache
import asyncio

BASE_URL = "https://api.acedata.cloud/hailuo"
TOKEN = os.getenv("TOKEN")
CALLBACK_URL = os.getenv("CALLBACK_URL")

COMMON_HEADERS = {
    "content-type": "application/json",
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}


async def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if data is not None:
        data = json.dumps(data)
    if data['callback']:# 
        data['callback_url']=CALLBACK_URL
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=method, url=url, data=data, headers=headers
            ) as resp:
                return await resp.json()
        except Exception as e:
            raise Exception(resp.text)


async def get_feed(task_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/tasks"
    payload = {"action": "retrieve", "id": task_id}
    logger.info(f"Fetching feed for task id: {task_id}")
    response = await fetch(api_url, headers, payload)
    logger.info(f"Feed fetched: {response}")
    return response


async def get_feed_by_clip_id(clip_id, token):
    task_id = cache.get(clip_id)
    if task_id:
        feed = await get_feed(task_id, token)
        if feed and feed.get("response") and feed.get("response").get("data"):
            for clip in feed.get("response").get("data"):
                if clip.get("id"):
                    return [clip]




async def generate_video_with_prompt(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/videos"
    payload = {
        "action": "generate",
        "model": data["md"],
        "prompt": data["prompt"],
        "callback":False # false:it cost 1-2 minutes to generate a video;true:it reutun task_id
    }
    response = await fetch(api_url, headers, payload)
    # res = await get_clip_id(response, token)
    if response:
        return response
    return {"detail": "timeout"}

async def generate_video_with_taskid(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/tasks"
    payload = {
        "id": data["task_id"],
    }
    response = await fetch(api_url, headers, payload)
    res = await get_clip_id(response, token)
    if res:
        return res
    return {"detail": "timeout"}



async def get_clip_id(response, token):
    if response.get("task_id"):
        for _ in range(60):
            feed = await get_feed(response.get("task_id"), token)
            if feed.get("response") and feed.get("response").get("data"):
                clips = []
                for clip in feed.get("response").get("data"):
                    if clip.get("id"):
                        clips.append({"id": clip.get("id")})
                        cache.set(clip.get("id"), response.get("task_id"), 600)
                if clips:
                    return {"id": response.get("task_id"), "clips": clips}
            await asyncio.sleep(1)
