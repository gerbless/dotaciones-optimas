from app.scheduling.main import scheduling, search_diary
from app.input.main import get_result_task_id, processing_errors
from app.helpers.util import monthyear


def create_app(action: str):
    if action == 'scheduling':
        scheduling(monthyear=monthyear)
    elif action == 'generate':
        search_diary(monthyear=monthyear)
    elif action == 'endowments':
        get_result_task_id()
    elif action == 'runerror':
        processing_errors()