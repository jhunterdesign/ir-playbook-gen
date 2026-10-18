"""Core logic for generating and formatting incident response playbooks."""

import re
import sys
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

SYSTEM_PROMPT = """You are a senior Incident Response Engineer. Generate an actionable, 
technical Incident Response (IR) playbook tailored to the user's threat scenario and environment.

Structure the playbook strictly around NIST SP 800-61 Rev. 2 phases:
1. Preparation (Required log sources, access prerequisites, tooling)
2. Detection & Analysis (Specific telemetry queries, Event IDs, Cloud Audit log methods, and MITRE ATT&CK T-codes)
3. Containment (Short-term isolation and long-term containment steps, including CLI commands where applicable)
4. Eradication (Root cause removal, credential rotation, persistence hunting)
5. Recovery (Validation checks, service restoration, monitoring tuning)
6. Post-Incident Activity (Detection engineering takeaways and control gaps)

Keep guidance concrete and technical. Avoid generic filler."""


def sanitize_filename(name: str) -> str:
    """Convert threat name into a clean, filesystem-safe filename."""
    name = re.sub(r"[^\w\s-]", "", name).strip().lower()
    return re.sub(r"[-\s]+", "_", name)[:40]


def generate_incident_response_playbook(
    client: OpenAI, threat_type: str, environment_details: str
) -> str | None:
    """Generate an incident response playbook based on threat type and environment."""
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Threat Scenario: {threat_type}\n"
                f"Target Environment: {environment_details}\n\n"
                "Generate the technical IR playbook in Markdown."
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=2048,
            temperature=0.2,  # Lowered from 0.7 for more deterministic technical output
        )
        content = response.choices[0].message.content
        return content.strip() if content else None
    except Exception as e:
        print(f"\n[!] API Error: {e}", file=sys.stderr)
        return None
