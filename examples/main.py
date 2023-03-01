import sys
import agent


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit("Too few arguments calling script")
    qa = agent.setup(sys.argv[1])
    print("Chat Langchain Demo")
    print("Ask a question to begin:")
    while True:
        query = input("")
        answer = qa.run(query)
        print(answer)
        print("\nWhat else can I help you with:")
