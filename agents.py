import os

from langchain.agents import create_agent
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv


load_dotenv()
# model setup 
# HuggingFaceEndpoint defaults sometimes mismatch for chat models.
# Use task="text-generation" (no chat) and rely on ChatHuggingFace for message formatting.
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    # Ensure we don't try to call a non-supported chat endpoint.
    # LangChain will still format messages for ChatHuggingFace; this parameter prevents HF from using /v1/chat/completions.
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)


model = llm


# 1st agents
def build_search_agent():
    # Use a plain text-generation model to avoid HF chat-completions routing issues.
    # ChatHuggingFace can be incompatible depending on the HF endpoint.
    return create_agent(
        model=model,
        tools=[web_search],
    )

# 2nd agents
def build_reader_agent():
    return create_agent(
        model=model,
        tools=[scrape_url],
    )


# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""
    )
])

writer_chaim = writer_prompt | model | StrOutputParser()

# critic chain

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Be honest and specific."
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    )
])

critic_chain = critic_prompt | model | StrOutputParser()