from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from schematic_to_boardview_pipeline import process_schematic

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and processing."""
    if "file" not in request.files:
        return redirect(request.url)
    
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    
    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Process the file and generate the boardview
        output_file = os.path.join(app.config["OUTPUT_FOLDER"], "output.brd")
        process_schematic(file_path, output_file)

        # Provide the download link for the boardview
        return redirect(url_for("download_file", filename="output.brd"))


@app.route("/download/<filename>")
def download_file(filename):
    """Serve the generated boardview file for download."""
    file_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
