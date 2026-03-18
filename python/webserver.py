from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

SHM_FOLDER = "/dev/shm"

# Serve files from shm folder
@app.route("%s/<path:filename>"%SHM_FOLDER)
def serve_file(filename):
    file_path = os.path.join(SHM_FOLDER, filename)

    # Prevent directory traversal
    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(SHM_FOLDER, filename)

# Index page listing all files
@app.route("/")
@app.route("/index.htm")
def index():
    files = [
        f for f in os.listdir(SHM_FOLDER)
        if os.path.isfile(os.path.join(SHM_FOLDER, f))
    ]

    html = """
    <html>
    <head>
        <title>File List</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>DigiCast</h1>
        <ul>
    """

    for f in files:
        html += f'<li><a href="%s/{f}">{f}</a></li>'%SHM_FOLDER

    html += """
        </ul>
        <p>Page auto-refreshes every 5 seconds.</p>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
