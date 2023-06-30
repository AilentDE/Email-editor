from fastapi import Header, HTTPException, BackgroundTasks


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "inuitoko":
        raise HTTPException(status_code=400, detail="No inuitoko token provided")

async def csrf_check(csrfToken: str = Header()):
    if csrfToken != "inuitoko":
        raise HTTPException(status_code=400, detail="Must be my wife Inui")
    
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

class QueryParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit