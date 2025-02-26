import operator
from enum import Enum
from typing import Annotated, Dict, List, Sequence, Tuple, TypedDict

from langchain_core.messages import BaseMessage

class WorkflowState(TypedDict):
	messages: Annotated[Sequence[BaseMessage], operator.add]
	list_tasks: List | None
	done_tasks: Annotated[Sequence[BaseMessage], operator.add]
	current_task: str | None
	next_task: str | None
	next_tool: str | None
	user_input: str | None
	data: List | None
	ecom_search: Dict | None
	ship_time: Dict | None
	disc_promo: Dict | None
	comp_price: Dict | None
	return_policy: Dict | None

class NodeType(str, Enum):
	SUPERVISOR_AGENT_TOOL = "supervisor_agent_tool"
	ECOM_SEARCH_AGGREGATOR = "ecom_search_aggregator"
	SHIP_TIME_ESTIMATOR = "ship_time_estimator"
	DISCOUNT_PROMO_CHECKER = "discount_promo_checker"
	COMP_PRICE_COMPARE = "comp_price_compare"
	RETURN_POLICY_CHECK = "return_policy_check"
	HUMAN_AGENT_TOOL = "human_agent_tool"