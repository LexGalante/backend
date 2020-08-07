from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from .resources.configuration import get_configuration
from .resources.database import close_database, connect_database
from .resources.http_handler import http_error_handler
from .v1 import api as api_v1

# load configurations
load_dotenv()
config = get_configuration()
# prepare application
app = FastAPI(title=config.PROJECT_NAME)
# inject custom error
if config.ENABLE_CUSTOM_ERROR:
    app.add_middleware(ServerErrorMiddleware)
# inject cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# inject https-redirect
if config.ENABLE_HTTPS_REDIRECT:
    app.add_middleware(HTTPSRedirectMiddleware)
# inject mongo context
app.add_event_handler("startup", connect_database)
app.add_event_handler("shutdown", close_database)
# inject error handler
app.add_exception_handler(HTTPException, http_error_handler)
# prepare versioning api
app.mount("/v1", api_v1.subapp)
