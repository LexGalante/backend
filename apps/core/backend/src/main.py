from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from .api.v1 import api as api_v1

# load configurations
load_dotenv()
# prepare application
app = FastAPI()
# inject custom error
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
app.add_middleware(HTTPSRedirectMiddleware)
# prepare versioning api
app.mount("/v1", api_v1.subapp)
