# lamak8pen
Automated Kubernetes pentest agent using local model

## Kubernetes Pentest Agent

The `lamak8_agent.py` module implements an automated Kubernetes penetration-testing agent that assists security testers in identifying misconfigurations, vulnerabilities, and potential attack paths inside a Kubernetes cluster.

The agent is designed to interact with a Kubernetes environment using command outputs (such as `kubectl` responses) and analyze them using a language model. Its goal is to simulate the reasoning process of a security analyst by identifying risky configurations, privilege escalation paths, and opportunities for data exfiltration.

### How It Works

The agent follows a simple analysis workflow:

1. **Collect Kubernetes Information**
   - Receives Kubernetes data such as pod listings, RBAC policies, secrets, namespaces, and other cluster resources.
   - The information is typically obtained through `kubectl` commands or other cluster inspection methods.

2. **Security Analysis**
   - The agent evaluates the provided Kubernetes data to detect potential security weaknesses.
   - It looks for common misconfigurations including:
     - Excessive RBAC privileges
     - Privileged containers
     - Host filesystem mounts
     - Exposed secrets
     - Dangerous service account permissions

3. **Attack Path Identification**
   - Based on the discovered issues, the agent proposes possible attack paths an attacker could use to escalate privileges or access sensitive data.

4. **Remediation Guidance**
   - For each issue identified, the agent suggests mitigation steps and configuration fixes to reduce the attack surface and improve cluster security.

### Purpose

The agent is intended to support Kubernetes security assessments by:

- Automating the initial analysis of cluster configurations
- Highlighting potential vulnerabilities quickly
- Assisting penetration testers during manual reviews
- Providing remediation recommendations for discovered issues

This approach allows security teams to combine automated reasoning with manual validation when performing Kubernetes penetration tests.
