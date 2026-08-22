# AWS AI Moment Validation Framework (BDD Architecture Prototype)
## SDET for AI - Manuel Steele

This repository serves as a lightweight technical demonstration for an automated data validation framework targeting real-time, asynchronous AI/ML streaming data pipelines.

## System Overview
Instead of utilizing heavy, synchronous HTTP request cycles typical of traditional REST architectures (such as API Gateway & Swagger specs), this testing paradigm utilizes **Pydantic Data Contracts** within a **Behavior-Driven Development (BDD)** test harness to validate complex multi-modal AI payloads instantly at the data engine level.

## Prerequisites & Installation
Ensure you have Python 3.10+ installed locally.

```bash
# Clone the repository
git clone https://github.com
cd ai-moment-validator-bdd

# Install project test dependencies
pip install -r requirements.txt
```

## Running the Automated Test Suite
Execute the entire behavioral testing suite through your command-line interface:

```bash
behave
```
