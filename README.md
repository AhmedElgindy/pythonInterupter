# Python Code Execution Server

This is a Flask-based HTTP server that allows users to execute Python code snippets. The server supports persistent interpreter sessions and environment hardening to restrict potentially harmful actions.

## Features

### Basic Code Execution

- Users can send Python code to the server via a POST request.
- The server executes the code and returns the output (stdout), errors (stderr), or any server-side errors.

### Persistent Interpreter Sessions

- Users can create and reuse interpreter sessions by providing a `session_id`.
- State (e.g., variables, functions) is retained between requests within the same session.

### Environment Hardening

- The server restricts access to potentially harmful operations, such as file deletion.
- For example, attempts to use `os.remove` will result in a `PermissionError`.

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask (`pip install flask`)

### Running the Server

1. Clone the repository or download the `app.py` file.
2. Install the required dependencies:

   ```bash
   pip install flask
   ```

3. Run the server:

   ```bash
   python app.py
   ```

4. The server will start at `http://127.0.0.1:5000`.

## API Endpoint

### POST `/execute`

Executes the provided Python code and returns the result.

#### Request Body

```json
{
  "code": "string",        
  "id": "string (optional)" 
}
```

#### Response

The server responds with a JSON object containing the following fields:

- `id` (string): The session ID associated with the interpreter.
- `stdout` (string, optional): The standard output from the executed code.
- `stderr` (string, optional): Any error output from the executed code.
- `error` (string, optional): Any server-side error message.

## Example Requests

### Basic Code Execution

**Request:**

```json
{
  "code": "print('Hello, World!')"
}
```

**Response:**

```json
{
  "id": "some-uuid",
  "stdout": "Hello, World!\n"
}
```

### Persistent Interpreter Session

**Request 1 (Create Session):**

```json
{
  "code": "x = 5"
}
```

**Response:**

```json
{
  "id": "some-uuid"
}
```

**Request 2 (Use Session):**

```json
{
  "id": "some-uuid",
  "code": "print(x)"
}
```

**Response:**

```json
{
  "id": "some-uuid",
  "stdout": "5\n"
}
```

### Environment Hardening

**Request:**

```json
{
  "code": "import os; os.remove('file.txt')"
}
```

**Response:**

```json
{
  "error": "[Errno 13] Permission denied: filesystem access restricted"
}
```

## Limitations

- **Time and Resource Limits:** The server does not currently enforce time or memory limits for code execution.
- **Sandboxing:** While the server restricts some harmful actions (e.g., file deletion), it is not a fully isolated sandbox. Additional restrictions may be required for production use.

## Contributing

If you'd like to contribute to this project, feel free to open an issue or submit a pull request. Contributions to improve security, performance, or functionality are welcome!

## License

This project is open-source and available under the MIT License.

