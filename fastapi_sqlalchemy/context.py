import gc
import warnings
from contextlib import AsyncExitStack, ExitStack, asynccontextmanager, contextmanager
from typing import List

from .extensions import SQLAlchemy

REGISTERED_DBS: List[SQLAlchemy] = []


def refresh_dbs():
    global REGISTERED_DBS
    REGISTERED_DBS = []
    with warnings.catch_warnings():
        for obj in gc.get_objects():
            if isinstance(obj, SQLAlchemy):
                if obj.initiated:
                    REGISTERED_DBS.append(obj)


@contextmanager
def enter_contexts():
    global REGISTERED_DBS
    with ExitStack() as stack:
        for db in REGISTERED_DBS:
            stack.enter_context(db())
        yield


@asynccontextmanager
async def async_enter_contexts():
    global REGISTERED_DBS
    async with AsyncExitStack() as stack:
        for db in REGISTERED_DBS:
            await stack.enter_async_context(db())
        yield


refresh_dbs()
