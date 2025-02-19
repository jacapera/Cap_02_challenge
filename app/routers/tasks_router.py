from fastapi import APIRouter, HTTPException
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()


@tasks_router.post(
    "/",
    response_model=Task,
    summary="Crear una nueva tarea",
    description="Crea una nueva tarea en la base de datos.",
)
async def create_task(task: Task):
    """
    Crea una nueva tarea.

    Args:
        task (Task): Los datos de la tarea a crear.

    Returns:
        Task: La tarea creada.

    Raises:
        HTTPException 500: Si ocurre un error al crear la tarea.
    """
    try:
        return db.add_task(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tarea: {str(e)}")


@tasks_router.get(
    "/{task_id}",
    response_model=Task,
    summary="Obtener una tarea por ID",
    description="Obtiene una tarea específica por su ID.",
)
async def get_task(task_id: int):
    """
    Obtiene una tarea por su ID.

    Args:
        task_id (int): El ID de la tarea a obtener.

    Returns:
        Task: La tarea encontrada.

    Raises:
        HTTPException 404: Si la tarea no se encuentra.
    """
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get(
    "/",
    response_model=TaskList,
    summary="Obtener todas las tareas",
    description="Obtiene una lista de todas las tareas.",
)
async def get_tasks():
    """
    Obtiene todas las tareas.

    Returns:
        TaskList: Una lista de todas las tareas.

    Raises:
        Ninguna.
    """
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)


@tasks_router.put(
    "/{task_id}",
    response_model=Task,
    summary="Actualizar una tarea",
    description="Actualiza una tarea existente por su ID.",
)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    """
    Actualiza una tarea existente.

    Args:
        task_id (int): El ID de la tarea a actualizar.
        task_update (UpdateTaskModel): Los datos a actualizar de la tarea.

    Returns:
        Task: La tarea actualizada.

    Raises:
        HTTPException 404: Si la tarea no se encuentra.
    """
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@tasks_router.delete(
    "/{task_id}",
    summary="Eliminar una tarea",
    description="Elimina una tarea por su ID.",
)
async def delete_task(task_id: int):
    """
    Elimina una tarea.

    Args:
        task_id (int): El ID de la tarea a eliminar.

    Returns:
        dict: Un mensaje de éxito.

    Raises:
        Ninguna.
    """
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}


@tasks_router.delete(
    "/",
    summary="Eliminar todas las tareas",
    description="Elimina todas las tareas de la base de datos.",
)
async def delete_all_tasks():
    """
    Elimina todas las tareas.

    Returns:
        dict: Un mensaje de éxito.

    Raises:
        Ninguna.
    """
    db.delete_all_tasks()
    return {"message": "All tasks deleted successfully"}
