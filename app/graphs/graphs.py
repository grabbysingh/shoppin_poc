from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from fastapi import status, HTTPException

import app.tools.tools as Agents_Tools_Catalog
from app.states.states import WorkflowState

from loguru import logger
import traceback

class Grapher:

	def __init__(self, thread_id):
		memory = MemorySaver()
		workflow = StateGraph(WorkflowState)
		self.state = self.initial_state()
		self.graph = self.create_shoppin_graph(memory, workflow)
		self.config = {
			"recursion_limit": 50,
			"configurable": {
				"thread_id": thread_id
			}
		}
	
	def initial_state(self):
		initial_state = WorkflowState(
			messages = ["begin the process"],
			list_tasks = [],
			done_tasks = [],
			current_task = "",
			next_task = "",
			user_input = "",
			data = [],
			ecom_search = {},
			ship_time = {},
			disc_promo = {},
			comp_price = {},
			return_policy = {},
		)
		
		return initial_state
	
	def create_shoppin_graph(self, memory, workflow):

		workflow.add_node("task_definer_tool", Agents_Tools_Catalog.tasks_definer_tool)
		workflow.add_node("supervisor_agent_tool", Agents_Tools_Catalog.supervisor_agent_tool)
		workflow.add_node("ecom_search_aggregator", Agents_Tools_Catalog.ecom_search_aggregator)
		workflow.add_node("ship_time_estimator", Agents_Tools_Catalog.ship_time_estimator)
		workflow.add_node("discount_promo_checker", Agents_Tools_Catalog.discount_promo_checker)
		workflow.add_node("comp_price_compare", Agents_Tools_Catalog.comp_price_compare)
		workflow.add_node("return_policy_check", Agents_Tools_Catalog.return_policy_check)
		# workflow.add_node("human_agent_tool", Agents_Tools_Catalog.human_agent_tool)

		def route_from_supervisor(state: WorkflowState) -> str:
			try:
				next_tool = state.get("next_tool")
				return next_tool
			except Exception as e:
				tb = traceback.format_exc()
				logger.warning(tb)
				logger.error("An error occurred: %s", str(e))
				raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
		
		# def route_from_human(state: WorkflowState) -> str:
		# 	try:
		# 		if state.get("next_node") == "stop":
		# 			return END
		# 		return state["next_node"]
		# 	except Exception as e:
		# 		tb = traceback.format_exc()
		# 		logger.warning(tb)
		# 		logger.error("An error occurred: %s", str(e))
		# 		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
			
		workflow.add_edge(START, "task_definer_tool")
		workflow.add_edge("task_definer_tool", "supervisor_agent_tool")
		# workflow.add_conditional_edges(
		# 	"human_agent_tool",
		# 	route_from_human,
		# 	{
		# 		"supervisor_agent_tool": "supervisor_agent_tool",
		# 		END: END
		# 	}
		# )
		workflow.add_conditional_edges(
			"supervisor_agent_tool",
			route_from_supervisor,
			{
				"ecom_search_aggregator": "ecom_search_aggregator",
				"ship_time_estimator": "ship_time_estimator",
				"discount_promo_checker": "discount_promo_checker",
				"comp_price_compare": "comp_price_compare",
				"return_policy_check": "return_policy_check",
				"stop": END
			}
		)
		workflow.add_edge("ecom_search_aggregator", "supervisor_agent_tool")
		workflow.add_edge("ship_time_estimator", "supervisor_agent_tool")
		workflow.add_edge("discount_promo_checker", "supervisor_agent_tool")
		workflow.add_edge("comp_price_compare", "supervisor_agent_tool")
		workflow.add_edge("return_policy_check", "supervisor_agent_tool")

		return workflow.compile(checkpointer=memory)
	
'''
from IPython.display import Image, display
grapher = Grapher(thread_id="thread_id")

image_data = grapher.graph.get_graph().draw_mermaid_png()

with open("/flow/graph.png", "wb") as f:
    f.write(image_data)
display(Image(image_data))

'''