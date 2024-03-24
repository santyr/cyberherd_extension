import asyncio
from typing import List

from fastapi import APIRouter

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_cyberherd")  #TODO: change to cyberherd

scheduled_tasks: List[asyncio.Task] = []

cyberherd_static_files = [
    {
        "path": "/cyberherd/static", #TODO:  change paths
        "name": "cyberherd_static",  #TODO: change to cyberherd
    }
]
cyberherd_ext: APIRouter = APIRouter(
    prefix="/cyberherd", tags=["cyberherd"]  #TODO: change to cyberherd
)


def cyberherd_renderer():
    return template_renderer(["cyberherd/templates"]) #TODO: change to cyberherd


from .tasks import wait_for_paid_invoices
from .views import *  # noqa: F401,F403
from .views_api import *  # noqa: F401,F403


def cyberherd_start():
    loop = asyncio.get_event_loop()
    task = loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
    scheduled_tasks.append(task)
