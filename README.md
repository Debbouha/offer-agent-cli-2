# Offer Agent CLI

A command-line AI agent for searching, reading, and comparing job offers using natural language.

The application combines job-offer data from the **France Travail API** with the **Gemini Interactions API**. Gemini acts as the reasoning layer and dynamically calls deterministic Python tools to inspect the available job offers before producing a final response.

## Features

* Fetch job offers from the official France Travail API.
* Cache API responses locally to avoid unnecessary requests.
* Search offers using natural-language requests.
* List available job offers.
* Search offers by keyword.
* Retrieve the complete details of a specific offer.
* Normalize France Travail data into internal Pydantic models.
* Validate tool inputs before execution.
* Execute multiple tool calls within the same agent turn.
* Return tool results to Gemini through the Interactions API.
* Continue the agent loop until Gemini produces a final response.
* Handle invalid tool inputs and expected tool execution errors.
* Protect the agent loop with a maximum iteration limit.

## Example

```bash
python main.py "Find Python developer jobs and tell me which three pay the most."
```

The agent can decide to:

```text
User request
    ↓
Gemini
    ↓
search_offers("python")
    ↓
matching offer IDs
    ↓
read_offer(id_1)
read_offer(id_2)
read_offer(id_3)
    ↓
tool results
    ↓
Gemini
    ↓
final answer
```

Tool selection is performed by Gemini, while validation, data access, and tool execution remain deterministic Python operations.

## Architecture

```text
main.py
   │
   ▼
llm_client.py
   │
   ├── Gemini Interactions API
   │
   ├── Agent loop
   │
   └── Tool execution
   │
   ▼
registry.py
   │
   ├── Tool declarations
   ├── Python functions
   ├── Input models
   └── Output models
   │
   ▼
tools.py
   │
   ├── list_offers
   ├── search_offers
   └── read_offer
   │
   ▼
offers.py
   │
   ├── France Travail API
   ├── OAuth authentication
   ├── Local cache management
   └── Job offer loading
   │
   ▼
data/francetravail.json
```

### `main.py`

CLI entry point.

It reads the user's request, ensures job-offer data is available, calls the agent, and displays the final response.

### `llm_client.py`

Contains the Gemini integration and agent orchestration loop.

Responsibilities include:

* creating Gemini interactions;
* detecting requested function calls;
* executing all function calls returned in an interaction;
* returning function results to Gemini;
* continuing the interaction chain;
* handling Gemini API failures;
* enforcing a maximum number of agent iterations.

### `registry.py`

Central registry for all tools exposed to Gemini.

Each tool contains:

```text
declaration
function
input_model
output_model
```

The declaration is exposed to Gemini as JSON Schema, while the Python function and Pydantic models remain controlled by the application.

### `tools.py`

Contains deterministic operations available to the agent.

#### `list_offers`

Returns the IDs and titles of available offers.

#### `search_offers`

Searches job titles and descriptions using a keyword and returns matching offer summaries.

#### `read_offer`

Retrieves and normalizes the complete information for one offer using its France Travail ID.

### `models.py`

Defines the application's data contracts using Pydantic.

The normalized `JobOffer` model contains fields such as:

```text
id
title
description
publication_date
company
location
salary
experience
skills
apply_url
```

This isolates the rest of the application from the original France Travail JSON structure.

### `offers.py`

Handles communication with France Travail and local data persistence.

The current implementation retrieves recent job offers using filters for:

* Paris (`75`);
* domain `M18`;
* CDI contracts;
* offers created during the previous 60 days;
* up to 150 results.

Responses are stored in:

```text
data/francetravail.json
```

The cache is refreshed when it is missing, invalid, empty, or older than 24 hours.

## Agent Loop

The application uses Gemini's Interactions API with function calling.

```text
1. Send user request + tool declarations to Gemini

2. Inspect interaction steps

3. If Gemini returns function calls:
       validate arguments
       execute tools
       collect results

4. Send all function results back to Gemini

5. Continue using previous_interaction_id

6. Repeat until Gemini returns a final text response
```

Multiple independent function calls returned during the same interaction are executed and returned together.

A maximum iteration limit prevents an agent execution from continuing indefinitely.

## Tool Validation

Gemini receives JSON Schema declarations describing the available tools.

The application independently validates tool arguments using Pydantic before executing Python functions.

```text
Gemini FunctionCall
        ↓
JSON arguments
        ↓
Pydantic input validation
        ↓
Python tool
        ↓
Pydantic output
        ↓
FunctionResult
        ↓
Gemini
```

This keeps model decisions separate from deterministic application validation.

## Error Handling

Expected tool errors are returned to Gemini as tool results instead of terminating the entire agent.

Examples include:

* invalid Pydantic input;
* unknown job-offer IDs;
* expected business-level validation errors.

Unexpected programming errors are not silently swallowed and can still surface normally during development.

Gemini API failures are handled separately from tool execution failures.

## Requirements

* Python 3.10+
* France Travail API credentials
* Gemini API key

Python dependencies:

```bash
pip install google-genai pydantic requests
```

## Configuration

### Gemini

Set a Gemini API key:

```bash
export GEMINI_API_KEY="your_api_key"
```

The Gemini model is configured in:

```python
# config.py

GEMINI_MODEL = "gemini-3.5-flash-lite"
```

### France Travail

Set the France Travail OAuth credentials:

```bash
export FRANCE_TRAVAIL_CLIENT_ID="your_client_id"
export FRANCE_TRAVAIL_CLIENT_SECRET="your_client_secret"
```

Credentials are read from environment variables and should never be committed to the repository.

## Running the Application

Clone the repository:

```bash
git clone https://github.com/Debbouha/offer-agent-cli.git
cd offer-agent-cli
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install google-genai pydantic requests
```

Configure the required environment variables, then run:

```bash
python main.py "Show me Python job offers."
```

Example requests:

```bash
python main.py "List the available job offers."

python main.py "Find offers mentioning Python."

python main.py "Find Python developer jobs and compare the best paid ones."

python main.py "What experience and skills are required for the most relevant backend offers?"
```

## Project Structure

```text
offer-agent-cli/
├── data/
│   └── francetravail.json
├── config.py
├── llm_client.py
├── main.py
├── models.py
├── offers.py
├── registry.py
├── tools.py
└── README.md
```

## Design

The application deliberately separates LLM reasoning from deterministic execution.

Gemini is responsible for deciding **what information it needs**.

Python remains responsible for:

* validating inputs;
* selecting registered functions;
* executing tools;
* accessing external data;
* normalizing results;
* enforcing execution limits.

This architecture allows new tools or additional job-offer providers to be introduced without coupling their internal data formats directly to the agent.
