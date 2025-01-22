from flask import Flask, request, jsonify
import uuid
import resource
import sys
import os

app = Flask(__name__)

# Dictionary to store persistent interpreter sessions
sessions = {}


# Custom class to capture stdout and stderr
class OutputCapture:
    def __init__(self):
        self.output = []

    def write(self, data):
        self.output.append(data)

    def get_output(self):
        return "".join(self.output)


# Function to execute Python code with limits
def execute_code(code, session_id=None):
    if session_id and session_id in sessions:
        # Use existing session
        session = sessions[session_id]
    else:
        # Create new session
        session_id = str(uuid.uuid4())
        session = {"locals": {}, "globals": {}}
        sessions[session_id] = session

    # Create output capture objects
    stdout_capture = OutputCapture()
    stderr_capture = OutputCapture()

    # Redirect stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture

    try:
        # Sandboxing: Restrict filesystem access
        def restricted_os_remove(*args, **kwargs):
            raise PermissionError(
                "[Errno 13] Permission denied: filesystem access restricted"
            )

        # Override os.remove with a restricted version
        session["globals"]["os"] = os
        session["globals"]["os"].remove = restricted_os_remove

        # Execute the code within the session
        exec(code, session["globals"], session["locals"])

        # Prepare response
        response = {
            "id": session_id,
            "stdout": stdout_capture.get_output(),
            "stderr": stderr_capture.get_output(),
        }
    except Exception as e:
        # Handle errors
        response = {
            "id": session_id,
            "error": str(e),
        }
    finally:
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return response


@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "Invalid request, 'code' is required"}), 400

    code = data["code"]
    session_id = data.get("id")

    try:

        # Execute code
        result = execute_code(code, session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
