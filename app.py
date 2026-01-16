import os 
from datetime import datetime 
from flask import Flask, jsonify, request, render_template 


app = Flask(__name__)


@app.get("/")
def homepage():
    try:
        # inserts data into a rendered template and serves it to the client
        return render_template(
            "index.html",
            server_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            message="Hello from Render!"
        )
    except Exception as e:
        return {'error': e}, 404


@app.get("/api/hello")
def api_hello():
    name = request.args.get("name", "world")
    return jsonify(message=f"Hello, {name}!", ok=True)

@app.post("/api/echo")
def api_echo():
    data = request.get_json(silent=True)

    if not data:
        return jsonify(ok=False, error="Missing JSON body"), 400

    # Accept a "text" field from the JSON
    text = data.get("text", "")
    if not isinstance(text, str):
        return jsonify(ok=False, error="'text' must be a string"), 400

    return jsonify(
        ok=True,
        received=text,
        length=len(text),
    )


@app.post("/api/secret-status")
def api_secret_status():
    print("Entered API")
    api_key = os.environ.get("DEMO_API_KEY")

    if not api_key:
        return jsonify(
            ok=False,
            configured=False,
            hint="DEMO_API_KEY was not found, please set it in Render environment variable."
        )
    
    return jsonify({})


# For local development
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)