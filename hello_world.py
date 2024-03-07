from langchain_community.llms import Ollama
import subprocess
llm = Ollama(model="codellama", temperature=0.6)

def get_response(prompt):
    return llm.invoke(prompt)

def clean_commit_message(response):
    cleanedCommitMessage = []
    listOfLines =  response.splitlines()
    for line in listOfLines:
        if("COMMIT MESSAGE" not in line.upper()):
            cleanedCommitMessage.append(f"{line}\n")
    return ''.join(str(x) for x in cleanedCommitMessage).strip()

def get_staged_changeset():
    return subprocess.run(["git", "diff", "--cached"], capture_output=True).stdout.splitlines()

def is_staged_changes(currentDiff):
    if(len(currentDiff) == 0):
        print("No staged changes")
        return False
    return True

def main():
    currentDiff = get_staged_changeset()
    if(not is_staged_changes(currentDiff)):
        return
    response = get_response(f"You are an expert programmer that writes simple, concise code and explanations. Write a commit message for the following diff (I am using this in a program so give me JUST the message): {currentDiff}")
    cleanedCommitMessage = clean_commit_message(response)
    if(cleanedCommitMessage == "" or cleanedCommitMessage == "\n"):
        print("No commit message available after cleanup - returning original response from AI")
        print(f"Original response: {response}")
        return response
    print(f"Commit message: {cleanedCommitMessage}")
    return cleanedCommitMessage

if __name__ == "__main__":
    main()

