from typing import Annotated

from fastapi import APIRouter, Depends

from repository import TaskRepo
from schemas import TaskSchema, TaskCreateSchema, TaskIdSchema

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks'],
)


@router.get('/tasks')
async def get_tasks() -> list[TaskSchema]:
    tasks = await TaskRepo.get_all()
    return tasks


@router.post('/tasks')
async def add_task(
    task_data: Annotated[TaskCreateSchema, Depends()]
) -> TaskIdSchema:
    new_task_id = await TaskRepo.add_one(task_data)
    return {'ok': True, 'task_id': new_task_id}
