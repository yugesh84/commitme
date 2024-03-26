import json
from langchain_community.llms import Ollama
import subprocess

def get_response_from_local_ai(prompt, properties):
    localRunningModelName = properties.get("localModel",{}).get("name","codellama")
    llm = Ollama(model=localRunningModelName, temperature=0.6)
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

def commit(finalCommitMessage, shouldAmend):
    subprocess.run(["git", "commit", "-m", finalCommitMessage])
    if(shouldAmend):
        subprocess.run(["git", "commit", "--amend"])

def is_staged_changes(currentDiff):
    if(len(currentDiff) == 0):
        print("No staged changes")
        return False
    return True

def calculate_final_commit_message(response):
    cleanedCommitMessage = clean_commit_message(response)
    if(cleanedCommitMessage == "" or cleanedCommitMessage == "\n"):
        print("No commit message available after cleanup - returning original response from AI")
        return response
    return cleanedCommitMessage

def get_response_from_ai(currentDiff, properties):
    if(properties.get("use") == "openAI"):
        response = get_response_from_open_ai(currentDiff, properties)
    else:
        response = get_response_from_local_ai(f"You are an expert programmer that writes simple, concise code and explanations. Write a commit message for the following diff (I am using this in a program so give me JUST the message): {currentDiff}", properties)
    return calculate_final_commit_message(response)

def commit_when_happy(currentDiff, properties):
    while True:
        finalCommitMessage = get_response_from_ai(currentDiff, properties)
        print(f"Final commit message: {finalCommitMessage}")
        userInput = input("Are you happy with this commit message? [(y)es/(n)o/(a)mend/(q)uit] ").lower()
        match userInput:
            case "y":
                commit(finalCommitMessage, False)
                break
            case "a":
                commit(finalCommitMessage, True)
                break
            case "q":
                return
            case _:
                continue

def get_response_from_open_ai(currentDiff, properties):
    from openai import OpenAI

    client = OpenAI(
        organization=properties.get("openAI",{}).get("organizationId",""),
        api_key=properties.get("openAI",{}).get("apiKey","")
    )
    from openai import OpenAI

    collectedData = ""
    stream = client.chat.completions.create(
        model=properties.get("openAI",{}).get("model",properties.get("openAI",{}).get("model","gpt-4")),
        messages=[{"role": "user", "content": f"Can you write a git commit message for this diff? {currentDiff}"}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            collectedData += chunk.choices[0].delta.content
    return collectedData

def load_properties():
    from pathlib import Path
    with open(Path.home()/"commitme.properties.json") as f:
        properties = json.load(f)
    return properties

def main():
    properties = load_properties()
    currentDiff = get_staged_changeset()
    if(not is_staged_changes(currentDiff)):
        return
    commit_when_happy(currentDiff, properties)


if __name__ == "__main__":
    main()

