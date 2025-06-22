# AI-AGENT

## This is a toy ai-agent that uses Google's gemini based on the "ai-agent" project from boot.dev

## To Run

- Clone the code:

```
git clone git@github.com:voylento/ai-agent.git
```

- Create and run the virtual environment, and install the requirements:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- create a .env file that contains your gemini api key:

```
  GEMINI_API_KEY="(your gemini api key)"
```

- try running a simple command:

```
python3 main.py "what files are in the root?"
```

You should see output similar to the following:

```
Calling function: get_files_info
('Okay, I see the following files in the root directory: `hello.py`, '
'`main.txt`, `README.md`, `lorem.txt`, `tests.py`, `main.py`, and `tests.go`. '
"There's also a directory named `pkg`.\n")
```

Try a few more:

```
python3 main.py "read the contents of main.py"
python3 main.py "write 'hello world' to main.txt"
python3 main.py "run main.py"
python3 main.py "list the contents of the pkg directory"
```

Try something a bit more complex:

- Change the file in calculator/pkg/calculator.py to set the precedence of the '+' operator to 3
- Verify that typing `python3 calculator/main.py "3 + 7 * 2"` produces the incorrect value of 20
- Get the ai-agent to fix the bug in pkg/calculator.py:

```
python3 main.py "fix the bug in pkg/calculator.py -- when running python3 main.py and passing in '3 + 7 * 2' it returns 20 and it should return 17"
```

The ai-agent is constrained to working in the calculator directory.

> [!WARNING]
> This is a toy app and does not contain sufficient security guardrails.
