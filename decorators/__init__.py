from prefect import task, get_run_logger
from functools import wraps


def with_manual_approval(
    prompt_message="Proceed with this task result? [y/N]:", max_retries=None
):
    def decorator(task_func):
        @task
        @wraps(task_func)
        def wrapper(*args, **kwargs):
            logger = get_run_logger()
            attempt = 0

            while True:
                result = task_func.fn(*args, **kwargs)
                logger.info("🔍 Task result preview:\n%s", result)

                response = input(f"🔒 {prompt_message} ").strip().lower()
                if response == "y":
                    logger.info("✅ Approval granted.")
                    return result

                attempt += 1
                logger.warning(
                    f"🛑 Approval denied. Retrying task (Attempt {attempt})..."
                )

                if max_retries and attempt >= max_retries:
                    raise Exception("Maximum manual retries reached.")

        return wrapper

    return decorator
