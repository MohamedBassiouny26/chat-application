import asyncio
import os

from app.jobs.tasks import update_chats_count_column
from app.jobs.tasks import update_messages_count_column
from app.providers.db import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = AsyncIOScheduler()


task_schedule = {
    "run_update_messages_every_30_minutes": [update_messages_count_column, 5],
    "run_update_chats_every_30_minutes": [update_chats_count_column, 5],
}


def add_tasks_to_scheduler():
    for key, value in task_schedule.items():
        print(f"add new task to scheduler {key}")
        scheduler.add_job(value[0], IntervalTrigger(minutes=value[1]))


if __name__ == "__main__":
    add_tasks_to_scheduler()
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        asyncio.get_event_loop().run_until_complete(db.connect())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Shutting down scheduler...")
        scheduler.shutdown()
