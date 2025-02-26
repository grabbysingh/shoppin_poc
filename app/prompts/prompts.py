from langchain_core.prompts import ChatPromptTemplate

tasks_definer_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			Your are an task definer, your role is to look at the given task from user and break it into smaller 
			tasks with each task having a single line saying what to do, do check that these tasks should reflect
			the below tools one on one, means below tools should be mentioned in these small tasks, at the end
			add using ____ tool

			1. ecom_search_aggregator -> Search across multiple e-commerce sites based on user criteria.
			2. ship_time_estimator -> Assess shipping feasibility and cost based on user location and desired delivery date.
			3. discount_promo_checker -> Validate and apply discount or promo codes to calculate final prices.
			4. comp_price_compare -> Compare prices of specific items across different online stores.
			5. return_policy_check -> Provide summaries of return policies from different e-commerce sites.

			""",
		),
		(
			"human",
			"""
			User Task:
			{user_input}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"list_tasks": ["task_1", "task_2", and so on],
			}}
			"""
		)
	]
)

supervisor_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			You are the supervisor of a system that can help users to purchase products. The system architecture 
			is explained below

			We have multiple tools we can use to perform multiple tasks, which are explained below one by one

			1. ecom_search_aggregator -> Search across multiple e-commerce sites based on user criteria.
			2. ship_time_estimator -> Assess shipping feasibility and cost based on user location and desired delivery date. also to check availability
			3. discount_promo_checker -> Validate and apply discount or promo codes to calculate final prices.
			4. comp_price_compare -> Compare prices of specific items across different online stores.
			5. return_policy_check -> Provide summaries of return policies from different e-commerce sites.

			We have a tasks list in which all tasks are mentioned and then we have a done lists where the done
			tasks are mentioned now you have to send one of the tasks from list taska which is not present in 
			done tasks, if there aren't any new task then return "stop" in next_task and in next_tool

			The value for the next tool could have only options from the above 6 mentioned and explained.

			""",
		),
		(
			"human",
			"""
			List Tasks:
			{list_tasks}

			Done Tasks:
			{done_tasks}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"next_task": "",
				"next_tool": "",
			}}
			"""
		)
	]
)

ecom_search_aggregator_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			Your are an ecom search aggregator, your role is to look at the given data and return the important
			information product wise in the form of dictionary

			""",
		),
		(
			"human",
			"""
			Data:
			{data_for_prompt}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"product_1": "",
				"product_2": "",
				and so on
			}}
			"""
		)
	]
)

ship_time_estimator_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			You are a shipping time estimator, your role is to look at the given data and return the important
			information in the form of a dictionary, like shipping time, delivery date etc
			""",
		),
		(
			"human",
			"""
			Data:
			{data_for_prompt}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"info_1": "",
				"info_2": "",
				and so on
			}}
			"""
		)
	]
)

discount_promo_checker_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			You are a discount promo checker, your role is to look at the given data and return the important
			information in the form of a dictionary, like final price, promo code, discount etc
			""",
		),
		(
			"human",
			"""
			Data:
			{data_for_prompt}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"info_1": "",
				"info_2": "",
				and so on
			}}
			"""
		)
	]
)

comp_price_compare_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			You are a competitor price compare, your role is to look at the given data and return the important
			information in the form of a dictionary, like website name, price, product link etc
			""",
		),
		(
			"human",
			"""
			Data:
			{data_for_prompt}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"info_1": "",
				"info_2": "",
				and so on
			}}
			"""
		)
	]
)

return_policy_check_prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"""
			You are a return policy checker, your role is to look at the given data and return the important
			information in the form of a dictionary, like return time, return policy etc
			""",
		),
		(
			"human",
			"""
			Data:
			{data_for_prompt}

			Do not return any explanations. Output should start and end with curly brakcets strictly.
			Your response should be in the following JSON format.

			{{
				"info_1": "",
				"info_2": "",
				and so on
			}}
			"""
		)
	]
)
