"""CLI entrypoint for the Incident Response Playbook Generator."""

import getpass
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

from ir_playbook.core import generate_incident_response_playbook, sanitize_filename

load_dotenv()


def main() -> None:
    """Run the interactive CLI workflow."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter OpenAI API Key: ").strip()
        if not api_key:
            print("[!] Error: API key is required.", file=sys.stderr)
            return

    client = OpenAI(api_key=api_key)

    threat_type = input("What threat or attack vector are we preparing for? ").strip()
    environment_details = input(
        "Describe the target environment (cloud, OS, infrastructure): "
    ).strip()

    if not threat_type or not environment_details:
        print("[!] Both threat scenario and environment are required.", file=sys.stderr)
        return

    print("\n[*] Generating playbook...")
    sys.stdout.flush()

    playbook = generate_incident_response_playbook(
        client, threat_type, environment_details
    )

    if playbook:
        output_dir = "playbooks"
        os.makedirs(output_dir, exist_ok=True)

        clean_name = sanitize_filename(threat_type)
        file_path = os.path.join(output_dir, f"playbook_{clean_name}.md")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(playbook)

        print(f"[+] Playbook written to: {file_path}")
        print("-" * 60)
        print(playbook[:400] + "\n\n... [truncated]")
        print("-" * 60)
    else:
        print("[-] Playbook generation failed.", file=sys.stderr)


if __name__ == "__main__":
    main()
