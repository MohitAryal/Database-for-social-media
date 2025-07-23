import redis.asyncio as redis
from typing import Any, Optional
import json
from datetime import datetime


# Create a Redis client instance
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


#  -------------------Posts Cache Operations-----------------------------------

async def cache_post(post_data: dict):
    """Store a post and update recent list"""
    post_id = post_data["id"]
    key = f"post:{post_id}"
    
    # Store the post itself
    await redis_client.set(key, json.dumps(post_data))
    
    # Push to recent list
    await redis_client.lpush(RECENT_POSTS_LIST, str(post_id))
    await redis_client.ltrim(RECENT_POSTS_LIST, 0, RECENT_LIMIT - 1)

async def get_cached_post(post_id: int) -> Optional[dict]:
    """Get a single post by ID from cache"""
    key = f"post:{post_id}"
    raw = await redis_client.get(key)
    return json.loads(raw) if raw else None

async def delete_cached_post(post_id: int):
    """Delete a post from cache and remove from recent list"""
    key = f"post:{post_id}"
    await redis_client.delete(key)
    await redis_client.lrem(RECENT_POSTS_LIST, 0, str(post_id))

async def get_recent_cached_posts() -> list[dict]:
    """Fetch all cached recent posts (up to limit)"""
    ids = await redis_client.lrange(RECENT_POSTS_LIST, 0, -1)
    posts = []
    for post_id in ids:
        post = await get_cached_post(int(post_id))
        if post:
            posts.append(post)
    return posts

# ------------ USER INTERACTION TRACKING ------------ #

INTERACTION_LIMIT = 20

async def track_user_interaction(user_id: int, interaction_type: str, post_id: int):
    """Track latest interactions of a user"""
    key = f"user:{user_id}:interactions"
    interaction = {
        "type": interaction_type,
        "post_id": post_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    await redis_client.lpush(key, json.dumps(interaction))
    await redis_client.ltrim(key, 0, INTERACTION_LIMIT - 1)

async def get_user_interactions(user_id: int) -> list[dict]:
    key = f"user:{user_id}:interactions"
    raw_list = await redis_client.lrange(key, 0, -1)
    return [json.loads(entry) for entry in raw_list]

async def clear_user_interactions(user_id: int):
    key = f"user:{user_id}:interactions"
    await redis_client.delete(key)
