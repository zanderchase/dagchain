# Import things that are needed generically
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import sys


def setup(module):
    global query
    query = __import__(module)
    llm = OpenAI(temperature=0)
    tools = [query.get_tool()]
    return initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )


if __name__ == "__main__":
    setup(sys.argv[1])
