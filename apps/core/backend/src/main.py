import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from resources.config import config
from api.v1 import api as api_v1

# load configurations
load_dotenv()
# prepare application
app = FastAPI()
# inject custom error
app.add_middleware(ServerErrorMiddleware)
# inject cors
if config.API_ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
# enable https redirect
if config.API_ENABLE_HTTPS_REDIRECT:
    app.add_middleware(HTTPSRedirectMiddleware)
# inject routers
app.include_router(api_v1.router, prefix=api_v1.prefix)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
