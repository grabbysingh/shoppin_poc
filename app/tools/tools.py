from langchain_core.output_parsers import JsonOutputParser

import app.llms.gemini as LLM_gemini_flash
import app.llms.deepseek as LLM_deepseek
import app.prompts.prompts as Prompts_Catalog
from app.states.states import WorkflowState, NodeType

from app.scrape.tavily import tavily_tool

from loguru import logger
# import traceback
# import ast

output_parser = JsonOutputParser()

def products_scraper(lst, task):

	final_lst = []
	for sing in lst:
		url = sing["url"]
		sing_data = tavily_tool.invoke(task + '\n' + url)
		final_lst.append(sing_data)

	return final_lst

def tasks_definer_tool(state: WorkflowState) -> WorkflowState:

	logger.info("in tasks_definer_tool")
	logger.info(state["user_input"])

	prompt = Prompts_Catalog.tasks_definer_prompt.format_messages(
		user_input = state["user_input"]
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	list_tasks = parsed_response["list_tasks"]

	return {
		"list_tasks": list_tasks,
		"current_task": list_tasks[0]
	}

def supervisor_agent_tool(state: WorkflowState) -> WorkflowState:

	logger.info("in supervisor_agent_tool")
	
	prompt = Prompts_Catalog.supervisor_prompt.format_messages(
		list_tasks = state["list_tasks"],
		done_tasks = state["done_tasks"]
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	# logger.info(str(parsed_response))
	next_task = parsed_response["next_task"]
	next_tool = parsed_response["next_tool"]

	if next_tool == "stop":
		logger.debug(" --------- Whole State --------- ")
		logger.debug(state)

	return {
		"next_task": next_task,
		"next_tool": next_tool
	}

def ecom_search_aggregator(state: WorkflowState) -> WorkflowState:

	logger.info("in ecom_search_aggregator")

	data = tavily_tool.invoke(state["next_task"])
	logger.info("data")
	logger.info(data)

	final_lst = products_scraper(data, "retrieve all important information from the provided products present in given link")
	logger.info("final_lst")
	logger.info(final_lst)
	
	prompt = Prompts_Catalog.ecom_search_aggregator_prompt.format_messages(
		data_for_prompt = final_lst
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	# logger.info(str(parsed_response))
	dct = parsed_response

	return {
		"ecom_search": dct,
		"done_tasks": [state["next_task"]],
		"data": data
	}

def ship_time_estimator(state: WorkflowState) -> WorkflowState:

	logger.info("in ship_time_estimator")

	final_lst = products_scraper(state["data"], state["next_task"])
	logger.info("final_lst")
	logger.info(final_lst)
	
	prompt = Prompts_Catalog.ship_time_estimator_prompt.format_messages(
		data_for_prompt = final_lst
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	# logger.info(str(parsed_response))
	dct = parsed_response

	return {
		"ship_time": dct,
		"done_tasks": [state["next_task"]]
	}

def discount_promo_checker(state: WorkflowState) -> WorkflowState:

	logger.info("in discount_promo_checker")

	final_lst = products_scraper(state["data"], state["next_task"])
	logger.info("final_lst")
	logger.info(final_lst)
	
	prompt = Prompts_Catalog.discount_promo_checker_prompt.format_messages(
		data_for_prompt = final_lst
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	# logger.info(str(parsed_response))
	dct = parsed_response

	return {
		"disc_promo": dct,
		"done_tasks": [state["next_task"]]
	}

def comp_price_compare(state: WorkflowState) -> WorkflowState:

	logger.info("in comp_price_compare")

	final_lst = products_scraper(state["data"], state["next_task"])
	logger.info("final_lst")
	logger.info(final_lst)
	
	prompt = Prompts_Catalog.comp_price_compare_prompt.format_messages(
		data_for_prompt = final_lst
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	# logger.info(str(parsed_response))
	dct = parsed_response

	return {
		"comp_price": dct,
		"done_tasks": [state["next_task"]]
	}

def return_policy_check(state: WorkflowState) -> WorkflowState:

	logger.info("in return_policy_check")

	final_lst = products_scraper(state["data"], state["next_task"])
	logger.info("final_lst")
	logger.info(final_lst)
	
	prompt = Prompts_Catalog.return_policy_check_prompt.format_messages(
		data_for_prompt = final_lst
	)

	# response_llm = LLM_deepseek.llm.invoke(prompt)
	response_llm = LLM_gemini_flash.llm.invoke(prompt)
	logger.info(str(response_llm.content))
	parsed_response = output_parser.parse(response_llm.content)
	# logger.info(str(parsed_response))
	dct = parsed_response

	return {
		"return_policy": dct,
		"done_tasks": [state["next_task"]]
	}