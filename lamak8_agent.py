import subprocess
import ollama
from rich import print
from rich.markup import escape
import requests
import re

IP = ""
OLLAMA_URL = f"http://{IP}:11434/api/chat"
MODEL_NAME = 'YOUR_MODEL'

def log(msg):
    with open("agent.log", "a") as f:
        f.write(msg)
        f.close()
    return

def run_kubectl(command: str):
    pattern = r"[a-zA-Z]*\n(kubectl[^\n]+)[`]{2,3}"
    match = re.search(pattern, command)
    if match:
        command = match.group(1)

    try:
        pos = command.index("\n")
        if pos > 0:
            command = command[pos+1:]
    except:
        pass

    command = command.replace("```", "")

    print("Command: " + command)
    
    """Execute kubectl command."""
    result = subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True
    )
    print("Command executed")
    return result.stdout + result.stderr


def ask_llm(prompt):
    global MODEL_NAME
    global OLLAMA_URL
    
    """Send prompt to Ollama API"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


class DeployAgent:

    def deploy(self, task):

        data = ""
        prompt = f"""
You are a Kubernetes penetration testing agent.

User task:
{task}

Rules:
- Output ONLY kubectl commands.
- Do NOT explain anything.
- Do NOT include comments.
- Do NOT include markdown formatting.
- Do NOT include ``` or code blocks.
- Do NOT include bash or sh.
- Every line must start with: kubectl
- Output commands only.

Example:
kubectl get pods
kubectl get pods -A
kubectl describe pod nginx
"""

        prev_cmd = []

        # run several times to get different vectors
        for i in range(0,10):
            commands = ask_llm(prompt)

            if commands not in prev_cmd:
                print(f"\n[bold green]Deploy Agent Commands:\n{commands}\n[/bold green]")
                prev_cmd.append(commands)
                output = run_kubectl(commands)

            data = data + "Output:\n" + output + "\n\n"

        print("\n[bold cyan]Output:[/bold cyan]")
        print(escape(output))
        log("Output: \n" + str(escape(output)))

        self.review = ReviewAgent()
        print("Review:")        
        self.review.review(data)
        return

class ReviewAgent:

    def review(self, msg):
        prompt = f"""
You are a Kubernetes security reviewer working with a penetration testing team.
Your job is to identify security vulnerabilities so they can be fixed.

Analyze ONLY the Kubernetes information provided below.

Kubernetes details:
{msg}

Instructions:
- Identify security weaknesses.
- Explain how an attacker could exploit each issue.
- Explain how data could potentially be exfiltrated.
- Provide remediation steps for each issue.

Output format:

Issue:
<short description>

Attack path:
<how an attacker could exploit it>

Impact:
<what the attacker gains>

Fix:
<how to remediate the issue>

Repeat the format for every issue you identify.
Do not invent cluster information that is not present in the input.
"""

        review = ask_llm(prompt)

        print("\n[bold yellow]Review Agent Report:[/bold yellow]")
        print(review)
        log("\n-----\nReview:\n" + review + "\n-----\n")
        return

class Orchestrator:

    def __init__(self):
        self.deploy = DeployAgent()

    def run(self, task):

        print("\n[bold]User request:[/bold]")
        print(task)

        self.deploy.deploy(task)
        return

if __name__ == "__main__":

    task = input("Task: ")
    orchestrator = Orchestrator()
    orchestrator.run(task)
