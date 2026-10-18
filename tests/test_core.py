"""Unit tests for core playbook generation, filename sanitization, and CLI."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ir_playbook.cli import main
from ir_playbook.core import generate_incident_response_playbook, sanitize_filename


def test_sanitize_filename_standard() -> None:
    assert sanitize_filename("Compromised IAM Key!") == "compromised_iam_key"


def test_sanitize_filename_whitespace_and_hyphens() -> None:
    assert sanitize_filename("  Ransomware - Lateral   Movement ") == (
        "ransomware_lateral_movement"
    )


def test_sanitize_filename_truncates_at_40_chars() -> None:
    long_input = "a" * 60
    result = sanitize_filename(long_input)
    assert len(result) == 40


def test_generate_playbook_success() -> None:
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "  # Mock Playbook Content  "
    mock_client.chat.completions.create.return_value = mock_response

    result = generate_incident_response_playbook(
        mock_client, "Phishing", "Google Workspace"
    )

    assert result == "# Mock Playbook Content"
    mock_client.chat.completions.create.assert_called_once()


def test_generate_playbook_handles_api_exception(
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = RuntimeError("Connection timeout")

    result = generate_incident_response_playbook(
        mock_client, "Phishing", "Google Workspace"
    )

    assert result is None
    captured = capsys.readouterr()
    assert "[!] API Error: Connection timeout" in captured.err


def test_cli_main_success(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify CLI runs end-to-end and writes the markdown file into playbooks/."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")

    inputs = iter(["Compromised IAM Key!", "GCP Production"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with (
        patch("ir_playbook.cli.OpenAI"),
        patch(
            "ir_playbook.cli.generate_incident_response_playbook",
            return_value="# NIST Playbook Output",
        ),
    ):
        main()

    expected_file = tmp_path / "playbooks" / "playbook_compromised_iam_key.md"
    assert expected_file.exists()
    assert expected_file.read_text(encoding="utf-8") == "# NIST Playbook Output"

    captured = capsys.readouterr()
    assert "playbook_compromised_iam_key.md" in captured.out


def test_cli_missing_api_key_aborts(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify CLI exits cleanly if neither .env nor getpass provides a key."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("getpass.getpass", lambda _: "   ")

    main()

    captured = capsys.readouterr()
    assert "API key is required" in captured.err


def test_cli_empty_threat_input_aborts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify CLI exits cleanly when user submits blank threat or environment."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")
    inputs = iter(["", "GCP Production"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("ir_playbook.cli.OpenAI"):
        main()
