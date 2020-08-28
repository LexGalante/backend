import uvicorn
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from api.v1 import api as api_v1
from middlewares.error_middleware import http_error_handler
from resources.config import API_ENABLE_CORS, API_ENABLE_HTTPS_REDIRECT
from resources.database import database_connect, database_disconnect

# configure logging
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# load configurations
load_dotenv()
# prepare application
app = FastAPI(title="Fastapi ASYNC")
# configure cors
if API_ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"]
    )
# enable https redirect
if API_ENABLE_HTTPS_REDIRECT:
    app.add_middleware(HTTPSRedirectMiddleware)
# inject routers
app.include_router(api_v1.router, prefix=api_v1.prefix)
# custom handlers
app.add_exception_handler(HTTPException, http_error_handler)


# starlette events
@app.on_event("startup")
async def startup():
    await database_connect()


@app.on_event("shutdown")
async def shutdown():
    await database_disconnect()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
