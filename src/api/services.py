import re
import json
import asyncio
from functools import wraps

from src import redis_manager


def cache(expire: int | None = None):
    def wrapper(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("cache decorator can only be applied to async functions")

        @wraps(func)
        async def inner(*args, **kwargs):
            key = generate_cache_key(func.__name__, args, kwargs)

            cached_data = await redis_manager.get(key)
            if cached_data:
                return json.loads(cached_data)

            data = await func(*args, **kwargs)
            if not data:
                return data

            data_schemas: list[dict] = [d.model_dump() for d in data]
            data_json = json.dumps(data_schemas)

            await redis_manager.set(key, data_json, expire)

            return data

        return inner

    return wrapper


def generate_cache_key(func_name, args, kwargs):
    pattern = re.compile(r"0x[0-9a-fA-F]+")
    mapper_dict = {}
    mapper_list = []
    if args:
        for arg in args:
            str(arg)
            has_id = re.sub(pattern, "", arg)
            if has_id:
                mapper_list.append(has_id)
            mapper_list.append(arg)
    if kwargs:
        for key, value in kwargs.items():
            value = str(value)
            has_id = re.sub(pattern, "", value)
            if has_id:
                mapper_dict[key] = has_id
            else:
                mapper_dict[key] = value
    return f"{func_name}:{mapper_dict}:{mapper_list}"
