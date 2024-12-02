# Getting Started with MultiverseNote

Welcome to MultiverseNote! This guide will walk you through the updated steps for setting up and running the project, along with configuration details for customization. The setup process has been streamlined to use `uv` for management, simplifying the workflow.



## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Python 3.8+**: Required for running the backend and management scripts.



## Installation Steps

### Step 1: Install `uv`

The project is managed with `uv`, which handles all configurations and dependencies. To install `uv`, run:

```bash
pip install uv
```

### Step 2: Synchronize Project Files

After installing `uv`, use it to set up the project. Navigate to the project directory and run:

```bash
uv sync
```

This command will download and configure all necessary dependencies and files.

### Step 3: Activate the Virtual Environment and Start the Project

Once synchronization is complete, activate the virtual environment that `uv sync` creates. Depending on your system type, use the following command:

- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```
- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```

For more information, refer to the [Python venv Documentation](https://docs.python.org/3/library/venv.html).

After activating the virtual environment, start the project by running:

```bash
python main.py
```

This will launch the backend and initialize the application.



## Configuration

MultiverseNote allows customization through configuration files and modular components. Follow these steps to update configurations and extend functionality:

### 1. Update Configuration Files

Configurations are stored in the `storage/config` directory. To update or customize settings:

1. Navigate to `storage/config`.
2. Open the desired configuration file (e.g., `main_config.yaml` by default) for editing.
3. Modify the configuration as needed.

#### Example Configuration File with Comments

```yaml
control:  
  bot:  
    api_key:  # Enter the API key for your bot service.
    name: OpenAI  # Name of the bot (e.g., OpenAI).
  tools:  
    - searchOnlineTool  # List of tool names available for the bot to use.

dao:  
  db:  
    activate: false  # Set to true if using a database; false otherwise.
    db_name: storage/db/db.sqlite  # Path to the database file.
    db_type: sqlite  # Type of database (e.g., sqlite, postgres, etc.).
    db_url: null  # Database URL (if applicable).
    password: null  # Database password (if applicable).
    user: null  # Database username (if applicable).
  file:  
    activate: false  # Set to true if using file-based storage.
    file_path: storage/file  # Path to the file storage location.

runtime:  
  agent_path: storage/agent  # Directory where agent configurations are stored.
  current_session_id:  # Leave empty for runtime-generated session IDs.
  history_path: storage/history  # Path to store conversation history.

view:  
  flask:  
    activate: true  # Enable Flask server.
    debug: true  # Enable debugging mode for development.
    host: localhost  # Host address for the Flask server.
    port: 5000  # Port for the Flask server.
  taipy:  
    activate: false  # Enable Taipy-based frontend (set to true if using).
```



### 2. Add Your Agent

To add a custom agent, follow these steps:

1. **Place Your Agent's File in the `storage/agent` Directory**:
   - Add the agent's configuration file to the `storage/agent` directory. This file defines the behavior and responses of the agent.

2. **Follow the Same Structure and Naming Conventions as Existing Agent Files**:
   - Consistency is key. Use the same naming conventions and file structure as the existing agents in the directory. This helps maintain uniformity and ensures that the application can properly identify and load agents.

3. **Restart the Application to Load the New Agent**:
   - After adding your agent, restart the application so that the new agent is recognized and available for use.

#### Example Agent File with Comments

```yaml
name: base  # The name of the agent.
args:  
  - query  # Arguments required by the agent (e.g., the input 'query' for conversation).
prompt: >  
  ## Participant Profile  
  **Name:** KK  
  **Role:** A helpful assistant.  

  ## Dialogue with USER  
  While the person asking the question is busy with work, keep the reply concise. KK engages USER in conversation. USER begins by saying: "{query}"
```

**Explanation**:

- **`name`**: This is the unique identifier for the agent (e.g., "base"). It helps differentiate between different agents.
- **`args`**: Lists the arguments that the agent expects. Here, it includes "query", which represents the user's input.
- **`prompt`**: Defines the structure of the agent's response.
  - `{}` (curly braces) are used to insert dynamic content. For instance, `{query}` will be replaced with the actual user query.
  - This prompt helps set the tone and behavior of the agent during a conversation, guiding how it should respond based on the user's input.



### 3. Add Your Own Tools

To integrate new tools into the application, you need to create a new tool file and follow specific guidelines. Each tool must include a function definition, input arguments, a mapping dictionary, and adhere to the OpenAI function calling definition.

1. **Navigate to the `app/tools` directory**: This is where all tool files are stored.
2. **Add Your Tool File**: Create a new Python file for your tool in this directory.
3. **Define the Tool Function**: Each tool must be implemented as a function. For example:

   ```python
   def fetch_web_page(url):
       """Fetches and returns the content of a web page."""
       try:
           response = requests.get(url)
           response.raise_for_status()
           return response.text
       except requests.RequestException as e:
           return "Failed to access: " + str(e)
   ```

4. **Specify Input Arguments**: Define the function input arguments clearly, as they will be used by the OpenAI function calling system.

5. **Map the Function to a Dictionary**: Use a mapping dictionary to connect the function name to its implementation. For example:

   ```python
   FUNCTION_MAPPING = {
       "fetch_web_page": fetch_web_page,  # Map function name to its implementation.
   }
   ```

6. **Define the Tool in `TOOLS_DEFINE`**: Use the OpenAI function calling format to define the tool. This includes specifying the function's name, description, and input parameters. For example:

   ```python
   TOOLS_DEFINE = [
       {
           "type": "function",
           "function": {
               "name": "fetch_web_page",
               "description": "Fetches and returns the content of a web page.",
               "parameters": {
                   "type": "object",
                   "properties": {
                       "url": {
                           "type": "string",
                           "description": "The URL of the web page to fetch."
                       }
                   },
                   "required": ["url"]
               }
           }
       }
   ]
   ```

7. **Follow Existing Patterns**: Refer to other files in the `app/tools` directory for guidance and ensure consistency.

For more details on OpenAI function calling definitions, see the [OpenAI Documentation](https://platform.openai.com/docs/api-reference/completions/create).

#### Example Tool Definition with Comments

```python
import requests

def fetch_web_page(url):
    """Fetches and returns the content of a web page."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 responses.
        return response.text
    except requests.RequestException as e:
        return "Failed to access: " + str(e)

def search_duckduckgo(query):
    """Use the DuckDuckGo Instant Answer API to search for a query and return a structured JSON response."""
    url = "https://api.duckduckgo.com/"
    params = {
        'q': query,      # The search query text.
        'format': 'json', # Response format in JSON.
        'no_html': 1,     # Remove HTML from responses.
        'skip_disambig': 1  # Skip disambiguation pages.
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data  # Return raw JSON data from DuckDuckGo API.
    except requests.RequestException as e:
        return {"error": str(e)}

FUNCTION_MAPPING = {
    "fetch_web_page": fetch_web_page,  # Map function name to its implementation.
    "search_duckduckgo": search_duckduckgo,  # Another mapped function.
}

TOOLS_DEFINE = [
    {
        "type": "function",
        "function": {
            "name": "fetch_web_page",
            "description": "Fetches and returns the content of a web page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the web page to fetch."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_duckduckgo",
            "description": "Simulates a simple DuckDuck Go search and returns the first result URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on DuckDuckGo."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
```



## Next Steps

Once your configurations and customizations are complete, you can:

- **Explore Features**: Test the tools and agents you've added.
- **Contribute**: Check the GitHub repository for open issues and tasks.
- **Collaborate**: Join community discussions to share ideas and receive feedback.



## Troubleshooting

If you encounter any issues:

1. Verify Python 3.8+ is installed and working correctly.
2. Ensure `uv sync` was run successfully without errors.
3. Double-check the file structure and naming conventions in the configuration, agent, and tools directories.
4. Consult terminal logs for detailed error messages.
5. Raise an issue on the GitHub repository or contact project maintainers for support.



## Conclusion

Thank you for contributing to MultiverseNote! Your contributions help expand and improve this project. For further assistance, contact us or refer to the documentation.

Happy coding! 🚀

