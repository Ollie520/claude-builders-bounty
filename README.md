# 🤖 Claude PR Review Agent

This project provides a command-line interface (CLI) tool and a GitHub Action to automate Pull Request (PR) reviews using Anthropic's Claude AI. It fetches a PR diff, sends it to Claude for analysis, and returns a structured Markdown review comment.

## ✨ Features

*   **CLI Tool:** Review any public or private GitHub PR from your terminal.
*   **Structured Output:** Generates a review with a summary, identified risks, improvement suggestions, and a confidence score.
*   **GitHub Action Ready:** Easily integrate into your CI/CD pipeline to automatically post reviews.

## 🚀 Setup

### 1. Prerequisites

*   Python 3.8+
*   A GitHub Personal Access Token (PAT) with `repo` scope (for private repos) or `public_repo` / `pull_requests:read` (for public repos).
*   An Anthropic API Key.

### 2. Installation

1.  **Clone the repository:**
    