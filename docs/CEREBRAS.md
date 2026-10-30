# 🐶 How to Use Biggato in cerebras most effective 

### 1. First Startup & The "Enter" Quirk
After installation, run `biggato` in your terminal.
1.  **Name your agent:** Enter any name (e.g., `PuppyBot`).
2.  **The Blank Enter:** Once the tool starts, **hit `Enter` one time** on the blank line.
    *   *Note: The tool often fails to recognize commands like `/set` until this first blank enter is registered.*

### 2. Configuration & Model Pinning
Copy and paste these commands one by one to set up your keys, authentication, and model bindings.

```text
/set cerebras_api_key = "YOUR_API_KEY_HERE"
/set yolo_mode = true

/add_model
```
*(Pick Anthropic, add an Opus and a Haiku model, and paste your Anthropic API key from platform.claude.com)*

```text
/model Cerebras-GLM-4.6
/pin_model planning-agent <your-opus-model>
/pin_model code-reviewer <your-haiku-model>
/pin_model python-reviewer <your-haiku-model>
```
*(Use the model names `/model` lists after `/add_model`.)*
*(Note: You can pin different reviewers depending on your language needs, e.g., java-reviewer)*

### 3. Restart
**Close and restart** Biggato. This ensures all configurations and pinned models are loaded correctly.

### 4. Running the Planning Agent
To start a task, always switch to the planning agent first. It will plan, verify with you, and then drive the other agents.

```text
/agent planning-agent 
```

### 5. Prompting Strategy
Copy and paste the prompt below to ensure the agent implements features, reviews them automatically, and avoids running the backend prematurely.

```markdown
Your task is to implement "REQUIREMENTS.MD".

For that use code-puppy to implement. Use python-reviewer to verify the implementation. If there are errors give the feedback to code_puppy to fix. Repeat until the reviewer has no more "urgent" fixes, maximum 3 times.

During development never execute the backend. Only verify with compiling!
