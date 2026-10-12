import os
import re
import argparse
from github import Github
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-opus-20240229" # Or claude-3-sonnet-20240229 for faster/cheaper

# --- GitHub Interaction ---
def get_pr_diff(pr_url: str) -> str:
    """Fetches the diff of a given GitHub Pull Request."""
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN environment variable not set.")

    match = re.match(r"https://github.com/([^/]+)/([^/]+)/pull/(\d+)", pr_url)
    if not match:
        raise ValueError(f"Invalid GitHub PR URL format: {pr_url}")

    owner, repo_name, pr_number = match.groups()
    pr_number = int(pr_number)

    g = Github(GITHUB_TOKEN)
    repo = g.get_user(owner).get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    print(f"Fetching diff for {owner}/{repo_name} PR #{pr_number}...")
    # Get the diff in a raw format
    diff = pr.get_patch()
    if not diff:
        raise ValueError(f"Could not retrieve diff for PR {pr_url}. It might be too large or empty.")
    return diff

# --- Claude Interaction ---
def generate_review_prompt(diff: str) -> str:
    """Generates the prompt for Claude to review the PR diff."""
    return f"""You are an expert software engineer and a meticulous code reviewer. Your task is to analyze the provided GitHub Pull Request diff and generate a structured review comment.

Focus on:
- Summarizing the changes concisely.
- Identifying potential risks (bugs, performance issues, security vulnerabilities, maintainability concerns, breaking changes).
- Suggesting concrete improvements (code style, best practices, alternative approaches, missing tests, documentation).
- Providing a confidence score for the quality and correctness of the changes.

The output MUST be in the following Markdown format. Do not include any other text or conversational elements outside of this structure.

