import os
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json

# Load environment variables
load_dotenv()

# Configure API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

# Configure Autogen
config_list = config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4"]
    }
)

class ResearchCopilot:
    def __init__(self):
        self.retriever = AssistantAgent(
            name="retriever",
            system_message="""You are a research paper retriever. Your task is to find relevant papers using the Semantic Scholar API.
            Focus on recent papers (last 2 years) and ensure they are directly related to the research query.""",
            llm_config={"config_list": config_list}
        )
        
        self.summarizer = AssistantAgent(
            name="summarizer",
            system_message="""You are a research paper summarizer. Your task is to extract key insights from papers.
            Focus on the problem statement, methodology, results, and novel contributions.""",
            llm_config={"config_list": config_list}
        )
        
        self.synthesizer = AssistantAgent(
            name="synthesizer",
            system_message="""You are a research synthesis expert. Your task is to compare findings across papers
            and create a comprehensive synthesis highlighting common techniques, innovations, and challenges.""",
            llm_config={"config_list": config_list}
        )
        
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "research_workspace"},
            llm_config={"config_list": config_list}
        )

    def search_papers(self, query: str) -> List[Dict]:
        """Search for papers using Semantic Scholar API"""
        base_url = "https://api.semanticscholar.org/graph/v1"
        headers = {"x-api-key": SEMANTIC_SCHOLAR_API_KEY} if SEMANTIC_SCHOLAR_API_KEY else {}
        
        params = {
            "query": query,
            "limit": 5,
            "fields": "title,abstract,year,authors,url"
        }
        
        response = requests.get(f"{base_url}/paper/search", headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []

    def generate_report(self, query: str) -> str:
        """Generate a research report using the agent swarm"""
        # Create group chat
        groupchat = GroupChat(
            agents=[self.user_proxy, self.retriever, self.summarizer, self.synthesizer],
            messages=[],
            max_round=50
        )
        
        manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
        
        # Start the research process
        self.user_proxy.initiate_chat(
            manager,
            message=f"""Let's research: {query}
            
            Retriever: Please find relevant papers using the Semantic Scholar API.
            Summarizer: For each paper, extract key insights.
            Synthesizer: Create a final synthesis comparing the findings.
            
            Format the output as a markdown report with sections for each paper and a final synthesis.
            """
        )
        
        return manager.last_message()["content"]

def main():
    # Example research query
    query = "What are the latest methods in Retrieval-Augmented Generation (RAG)?"
    
    # Initialize and run the research copilot
    copilot = ResearchCopilot()
    report = copilot.generate_report(query)
    
    # Save the report
    with open("research_report.md", "w") as f:
        f.write(report)
    
    print("Research report has been generated and saved to research_report.md")

if __name__ == "__main__":
    main() 