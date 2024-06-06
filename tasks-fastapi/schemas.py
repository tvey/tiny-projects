from pydantic import BaseModel, ConfigDict


class TaskCreateSchema(BaseModel):
    name: str
    description: str | None = None


class TaskSchema(TaskCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskIdSchema(BaseModel):
    ok: bool
    task_id: int