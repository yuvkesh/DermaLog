import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
import base64
import imghdr
from anthropic import Anthropic

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("No ANTHROPIC_API_KEY set for Flask application")

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_with_claude(image_path):
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    try:
        response = anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this skin image as a dermatologist. Provide potential conditions with percentages of likelihood. Include an overall accuracy percentage for the analysis. Indicate if findings are safe (green), need monitoring (orange), or potentially dangerous (red). Provide different suggestions based on the severity."
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error in analysis: {str(e)}"

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            analysis = analyze_with_claude(filepath)
            
            severity_class = 'green'
            severity_level = 'Safe'
            if 'red' in analysis.lower():
                severity_class = 'red'
                severity_level = 'Potentially Dangerous'
            elif 'orange' in analysis.lower():
                severity_class = 'orange'
                severity_level = 'Needs Monitoring'
            
            with open(filepath, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            return render_template('result.html', image=encoded_image, analysis=analysis, severity_class=severity_class, severity_level=severity_level)
    return render_template('index.html')
