from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import time
from werkzeug.utils import secure_filename
import re

# Import existing modules
from modules.voice_narrator import narrator
from modules.config_manager import config_manager
from modules.logger import system_logger, log_provenance
from modules.remedy_synthesizer import remedy_synthesizer
from modules.corpus_manager import corpus_manager
from modules.nlp_processor import nlp_processor
from modules.document_parser import document_parser

# Dynamically import agents based on config
jarvis_agent = None
if config_manager.get('agents.jarvis.enabled', False):
    from agents.jarvis_agent import jarvis_agent

friday_agent = None
if config_manager.get('agents.friday.enabled', False):
    from agents.friday_agent import friday_agent

dialogos_agent = None
if config_manager.get('agents.dialogos.enabled', False):
    from agents.dialogos_agent import dialogos_agent

echo_agent = None
if config_manager.get('agents.echo.enabled', False):
    from agents.echo_agent import echo_agent

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(__file__), config_manager.get('engine.watch_directory', 'intake')))
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Ensure output directory exists
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
os.makedirs(output_dir, exist_ok=True)

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        system_logger.info(f"File uploaded: {filepath}")
        narrator.say(f"New document uploaded: {file.filename}")
        
        processed_text = ""
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            narrator.say("Image file detected. Performing OCR.")
            processed_text = document_parser.ocr_image(filepath)
            if processed_text:
                system_logger.info(f"OCR successful for {filename}. Text length: {len(processed_text)}")
                # Enhanced parsing for general entities
                extracted_entities = document_parser.parse_document_for_entities(processed_text)
                system_logger.info(f"Extracted entities: {extracted_entities}")

                if document_parser.identify_remittance_slip(processed_text):
                    narrator.say("This appears to be a remittance slip. Attempting to extract details for endorsement.")
                    # Extract details for endorsement (existing logic)
                    extracted_data = extract_remittance_details(processed_text)
                    # Pass original file path for endorsement overlay
                    extracted_data['original_file_path'] = filepath
                    return redirect(url_for('generate_endorsement', **extracted_data))
                else:
                    narrator.say("OCR processed. Does not appear to be a remittance slip. Analyzing general entities.")
                    # Process general entities with agents
                    process_text_with_agents(filepath, processed_text)
                    return f"File {file.filename} uploaded and OCR processed. General entities analyzed."
            else:
                narrator.say("OCR failed for the uploaded image.")
                return f"Error processing image {file.filename}."
        elif filename.lower().endswith('.pdf'):
            narrator.say("PDF file detected. Extracting text.")
            processed_text = document_parser.extract_text_from_pdf(filepath)
            if processed_text:
                system_logger.info(f"PDF text extraction successful for {filename}. Text length: {len(processed_text)}")
                # Enhanced parsing for general entities
                extracted_entities = document_parser.parse_document_for_entities(processed_text)
                system_logger.info(f"Extracted entities: {extracted_entities}")

                if document_parser.identify_remittance_slip(processed_text):
                    narrator.say("This appears to be a remittance slip. Attempting to extract details for endorsement.")
                    extracted_data = extract_remittance_details(processed_text)
                    extracted_data['original_file_path'] = filepath
                    return redirect(url_for('generate_endorsement', **extracted_data))
                else:
                    narrator.say("PDF processed. Does not appear to be a remittance slip. Analyzing general entities.")
                    process_text_with_agents(filepath, processed_text)
                    return f"File {file.filename} uploaded and PDF processed. General entities analyzed."
            else:
                narrator.say("PDF text extraction failed for the uploaded PDF.")
                return f"Error processing PDF {file.filename}."
        else: # Assume text file
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    processed_text = f.read()
                system_logger.info(f"Text file loaded: {filename}. Text length: {len(processed_text)}")
                # Enhanced parsing for general entities
                extracted_entities = document_parser.parse_document_for_entities(processed_text)
                system_logger.info(f"Extracted entities: {extracted_entities}")
                process_text_with_agents(filepath, processed_text)
                return f"File {file.filename} uploaded and processed. General entities analyzed."
            except Exception as e:
                system_logger.error(f"Error reading text file {filename}: {e}")
                return f"Error reading text file {file.filename}."

def process_text_with_agents(filepath, processed_text):
    """Helper function to process text with NLP and agents."""
    try:
        nlp_results = nlp_processor.process_text(processed_text)
        narrator.say(f"Document classified as {nlp_results['classification']}.")

        if jarvis_agent:
            jarvis_agent.analyze(filepath, nlp_results)
        
        if friday_agent:
            friday_agent.analyze(filepath, processed_text)

        if dialogos_agent:
            dialogos_agent.analyze(processed_text)

    except Exception as e:
        system_logger.error(f"Error processing file {filepath} with agents: {e}")
        narrator.say("An error occurred during agent processing.")

def extract_remittance_details(text):
    # Basic heuristic extraction for common remittance slip fields
    # This is highly dependent on the format of the billing statement
    data = {
        "bill_from": "",
        "bill_amount": "",
        "account_number": ""
    }

    # Example: Extracting amount (simple regex for currency format)
    amount_match = re.search(r'\$([\d,\.]+)', text)
    if amount_match:
        data["bill_amount"] = amount_match.group(1)

    # Example: Extracting account number (simple regex for common patterns)
    account_match = re.search(r'Account Number:?\s*([\d-]+)', text, re.IGNORECASE)
    if account_match:
        data["account_number"] = account_match.group(1)

    # Example: Extracting bill_from (very basic, might need more context)
    # This is hard to do reliably without knowing the document structure
    # For now, we'll leave it blank or try to infer from top of document
    lines = text.split('\n')
    if len(lines) > 0:
        data["bill_from"] = lines[0].strip() # Assume first line is sender

    return data

@app.route('/generate_cd', methods=['GET', 'POST'])
def generate_cd():
    if request.method == 'POST':
        data = {
            "your_name": request.form['your_name'],
            "recipient_name": request.form['recipient_name'],
            "company_name": request.form['company_name'],
            "matter_subject": request.form['matter_subject'],
            "date": time.strftime("%Y-%m-%d")
        }
        output_path = remedy_synthesizer.generate_document('cease_and_desist.txt.j2', data)
        if output_path:
            return f"Cease & Desist letter generated: {output_path}"
        else:
            return "Failed to generate Cease & Desist letter."
    return render_template('generate_cd.html') # Create this template

@app.route('/generate_endorsement', methods=['GET', 'POST'])
def generate_endorsement():
    if request.method == 'POST':
        data = {
            "your_name": request.form['your_name'],
            "date": time.strftime("%Y-%m-%d"),
            "current_date": time.strftime("%Y-%m-%d"),
            "bill_from": request.form['bill_from'],
            "bill_amount": request.form['bill_amount'],
            "account_number": request.form['account_number'],
            "your_name_all_caps": request.form['your_name_all_caps']
        }
        # Generate PDF endorsement overlay instead of text instructions
        output_path = remedy_synthesizer.generate_endorsement_overlay_pdf(
            original_pdf_path=request.form.get('original_pdf_path'), # Pass original PDF path from form
            endorsement_text=f"Accepted for Value and Returned for Value\nExempt from Levy\nDeposit to the account of the U.S. Treasury\nBy: {data['your_name']}©, Authorized Representative\nWithout Prejudice UCC 1-308\nDate: {data['date']}",
            output_filename=f"endorsement_overlay_{data['account_number']}.pdf"
        )

        if output_path:
            return f"Endorsement instructions generated: {output_path}"
        else:
            return "Failed to generate endorsement instructions."
    else:
        # Pre-fill from GET parameters (extracted from OCR)
        your_name = request.args.get('your_name', '')
        bill_from = request.args.get('bill_from', '')
        bill_amount = request.args.get('bill_amount', '')
        account_number = request.args.get('account_number', '')
        original_pdf_path = request.args.get('original_pdf_path', '') # Pass original PDF path
        return render_template('generate_endorsement.html', 
                               your_name=your_name, 
                               bill_from=bill_from, 
                               bill_amount=bill_amount, 
                               account_number=account_number,
                               original_pdf_path=original_pdf_path)

if __name__ == '__main__':
    system_logger.info("Starting VeroBrix Web GUI.")
    narrator.say("VeroBrix Web GUI Initialized.")
    app.run(debug=True, host='0.0.0.0')