from langchain_community.llms import Ollama
import subprocess
llm = Ollama(model="codellama", temperature=0.6)

def get_response(prompt):
    return llm.invoke(prompt)

def get_staged_changeset():
    return subprocess.run(["git", "diff", "--cached"], capture_output=True).stdout.splitlines()

def main():
    currentDiff = get_staged_changeset()
    if(len(currentDiff) == 0):
        print("No staged changes")
        return
    response = get_response(f"You are an expert programmer that writes simple, concise code and explanations. Write a commit message for the following diff (I am using this in a program so give me JUST the message): {currentDiff}")
    # response = get_response(f"Assume you are a developer and you are writing a succinct but clear commit message for the following changeset: {get_staged_changeset()}")
    print(response)

if __name__ == "__main__":
    main()

