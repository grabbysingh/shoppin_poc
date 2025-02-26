Comparative Conceptual Map - Included in the Flow folder in repo.

Short Written Analysis - Have used FastAPI for backend design, langgraph for agentic implementation, a single API call with user input triggers the flow.

Design Decisions - Agent architecture and Tool Selection  - total 7 agents
                                                          - task definer tool (which breaks the user query into small tasks tagging them with given tools)
                                                          - one supervisor agent (calls the below mentioned 5 agents / tools)
                                                          - 5 agents / tools
                                                              - ecom search aggregator
                                                              - ship time estimator
                                                              - discount promo checker
                                                              - comp price compare
                                                              - return policy check

Challenges and improvements - The system required multiple state definitions to go along with the respective tools called by the supervisor which was quite challenging to implement.

Steps to run the application:

1. git clone https://github.com/grabbysingh/shoppin_poc.git
2. cd path_to_folder
3. pip install -r requirements.txt
4. python main.py
5. go to http://127.0.0.1:8001/docs
