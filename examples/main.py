from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import sys

query = __import__(sys.argv[1])
llm = OpenAI(temperature=0)
tools = [query.get_tool()]

def get_agent():
    return initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit("Too few arguments calling script")
    qa = get_agent()
    print("Chat Langchain Demo")
    print("Ask a question to begin:")
    while True:
        query = input("")
        answer = qa.run(query)
        print(answer)
        print("\nWhat else can I help you with:")
