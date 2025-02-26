from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from app.api.routers import api_router

app = FastAPI(
	title = "Shoppin POC",
	description = "Shoppin POC",
	version = "1.0.0"
)

app.include_router(api_router)

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"*"
	],
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)

if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="debug", reload=True)