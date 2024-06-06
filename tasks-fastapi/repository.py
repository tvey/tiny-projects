from sqlalchemy import select

from db import new_session, TaskModel
from schemas import TaskSchema, TaskCreateSchema


class TaskRepo:
    @classmethod
    async def add_one(cls, data: TaskCreateSchema) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            new_task = TaskModel(**task_dict)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id

    @classmethod
    async def get_all(cls) -> list[TaskSchema]:
        async with new_session() as session:
            query = select(TaskModel)
            result = await session.execute(query)
            tasks = result.scalars().all()
            task_schemas = [TaskSchema.model_validate(task) for task in tasks]
            return task_schemas
