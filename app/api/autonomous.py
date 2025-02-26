from fastapi import APIRouter, HTTPException, status
from loguru import logger
import traceback

from app.graphs.graphs import *

router = APIRouter()

logger.add("app/logs/func_execute.log", rotation="10 MB", level="DEBUG", backtrace=True, diagnose=True)

@router.post("/query")
async def func_query(user_query: str):
	try:
		grapher = Grapher("unique")
		state = grapher.state
		state["user_input"] = user_query

		for chunk in grapher.graph.stream(state, grapher.config, stream_mode="updates"):
			logger.debug("done")
		

	except Exception as e:
		tb = traceback.format_exc()
		logger.warning(tb)
		logger.error("An error occurred: %s", str(e))
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
