# VeroBrix Sovereign Intelligence Engine

![VeroBrix Logo Placeholder](https://example.com/verobrix_logo.png) <!-- Placeholder for a future logo -->

## Project Overview

The VeroBrix Sovereign Intelligence Engine is a sophisticated, Python-based AI assistant designed to empower individuals by providing tools for legal analysis, document generation, and the navigation of complex legal and financial systems from a sovereign perspective. Rooted in the philosophies of key thinkers like Carl Miller, Anelia Sutton, David Straight, and Brandon Joe Williams, VeroBrix aims to demystify legal processes and enable users to assert their rights and claims.

This engine operates on the principle that understanding and applying specific interpretations of law and commerce can lead to greater individual autonomy and remedy.

## Key Features

VeroBrix offers a range of interactive workflows and analytical capabilities:

*   **Passive Monitoring:** Monitors a designated `intake` folder for new documents (text, images, PDFs), processes them, and logs agent analysis.
*   **Document Upload (Web GUI):** Upload documents directly via a web interface for processing.
*   **OCR & Document Parsing:** Extracts text from image files (PNG, JPG) and PDFs, and attempts to identify document types (e.g., remittance slips) and extract key entities.
*   **Generate Cease & Desist Letter:** Create formal letters to demand cessation of unwanted contact.
*   **Workflow: Process a Bill with 'Accepted for Value':** Guides users through the process of endorsing bills for discharge, based on the A4V doctrine.
*   **Workflow: Process a Video Transcript:** Summarizes and analyzes video transcripts using the engine's agents.
*   **Workflow: Respond with Conditional Acceptance:** Generate letters to conditionally accept demands, setting specific terms for acceptance.
*   **Workflow: Initiate Status Correction:** Guides users in generating affidavits to declare their sovereign status.
*   **Workflow: Initiate Private Administrative Process:** Assists in generating a series of documents (e.g., Notice of Fault, Affidavit of Default) for administrative remedies.
*   **Workflow: Initiate UCC Filing for Status:** Generate simplified UCC-1 Financing Statements for declaring status or claiming interests.
*   **Workflow: Initiate Claim Against Official's Bond:** Generate notices to claim against public officials' surety bonds for alleged violations.
*   **Workflow: Create Debt Discharge Instrument:** Generate sovereign Bills of Exchange or Promissory Notes for debt discharge.
*   **Workflow: File Commercial Lien:** Generate Affidavits of Commercial Lien to assert claims.
*   **Generate a General Affidavit of Fact:** Create customizable affidavits to declare specific facts.
*   **Look up a Legal Term:** Query the engine's corpus for definitions of legal terms, including sovereign interpretations.
*   **Voice Narration:** Provides audible feedback for engine actions and prompts.

## Core Components

The VeroBrix engine is built on a modular architecture, with specialized agents and modules:

*   **`Dialogos` Agent:** The philosophical core, analyzing text through the lenses of Carl Miller, Anelia Sutton, David Straight, and Brandon Joe Williams. It provides contextualized insights from their teachings.
*   **`JARVIS` Agent:** Performs logical analysis, entity extraction, and system monitoring.
*   **`FRIDAY` Agent:** Conducts sentiment analysis on document content.
*   **`EchoAgent`:** Processes and summarizes text from transcripts.
*   **`CorpusManager`:** Manages the engine's extensive knowledge base, including legal definitions, historical documents, and structured teachings of key figures.
*   **`RemedySynthesizer`:** Generates various legal documents from customizable templates, including PDF endorsement overlays.
*   **`DocumentParser`:** Handles OCR for image files, extracts text from PDFs, and performs basic entity extraction and document type identification.
*   **`ConfigManager`:** Centralized configuration management for all engine settings.
*   **`Logger`:** Provides structured system and provenance logging for traceability and auditing.

## Knowledge Base Highlights

The engine's intelligence is powered by a rich corpus of information, including:

*   **Structured Teachings:** Detailed interpretations from Carl Miller, Anelia Sutton, David Straight, and Brandon Joe Williams.
*   **Legal Concepts:** Overviews of concepts like Accepted for Value, Conditional Acceptance, Private Administrative Process, Status Correction, Common Law vs. Admiralty/Maritime Law, UCC Filings, Surety and Bond Theory, Bills of Exchange/Promissory Notes, Color of Law, Judicial Notice/Immunity, Res Judicata/Collateral Estoppel, and Payment Coupon Endorsement.
*   **Foundational Texts:** Snippets from Black's Law Dictionary, UCC, and IRM.

## Installation and Setup

### Prerequisites
*   Python 3.10+ (with `venv` module)
*   `git`
*   `Tesseract` OCR engine (for image/PDF processing) - [Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)

### Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MrNAM205/VeroBrix-Engine.git
    cd VeroBrix-Engine
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download spaCy model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

### Running the Web GUI
1.  Navigate to the `VeroBrix-Engine` directory.
2.  Activate the virtual environment (`source venv/bin/activate`).
3.  Run the Flask application:
    ```bash
    python app.py
    ```
4.  Open your web browser and go to `http://127.0.0.1:5000`.

### Using the CLI (for passive monitoring)
1.  Navigate to the `VeroBrix-Engine` directory.
2.  Activate the virtual environment (`source venv/bin/activate`).
3.  Run the main script with the appropriate option (e.g., `python main.py 1` to start passive monitoring).

## Deployment

### Docker (Recommended for Portability)

To build the Docker image:
```bash
docker build -t verobrix-engine .
```

To run the interactive menu:
```bash
docker run -it --name verobrix-cli verobrix-engine
```

To run passive monitoring with volume mapping (for persistent intake/output/logs):
```bash
docker run -d \
  --name verobrix-watcher \
  -v /path/to/your/local/intake:/app/intake \
  -v /path/to/your/local/output:/app/output \
  -v /path/to/your/local/logs:/app/logs \
  verobrix-engine python main.py 1
```

### Background Service (Linux - systemd conceptual)

For Linux systems, you can configure a `systemd` service. Create a file like `/etc/systemd/system/verobrix.service`:

```ini
[Unit]
Description=VeroBrix Sovereign Intelligence Engine
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/your/VeroBrix-Engine
ExecStart=/path/to/your/VeroBrix-Engine/venv/bin/python main.py 1
Restart=always

[Install]
WantedBy=multi-user.target
```

Then, enable and start the service using `sudo systemctl enable verobrix.service` and `sudo systemctl start verobrix.service`.

## Future Enhancements

*   **More Document Templates:** Expand the library of customizable legal documents.
*   **Advanced Document Parsing:** Implement more robust AI/ML models for extracting structured data from diverse document layouts.
*   **Multi-Document Workflow Management:** Develop a system to track and manage complex, multi-step administrative processes over time.
*   **User Profile Management:** Allow users to store and manage their personal information for auto-filling documents.
*   **Direct Communication Integration:** Explore secure methods for sending documents via certified mail APIs or encrypted email.
*   **Enhanced User Interface:** Develop a more sophisticated web GUI or a desktop application for a richer user experience.

---

*Disclaimer: The VeroBrix Sovereign Intelligence Engine is designed for educational and informational purposes, exploring specific interpretations of legal and commercial theories. It does not provide legal advice. The legal theories and practices discussed and implemented within this project are not recognized by mainstream legal and financial systems and may be considered pseudolegal. Attempting to use these methods in real-world scenarios can lead to severe legal and financial consequences, including civil penalties, criminal charges, and the failure to achieve intended outcomes. Users are strongly advised to consult with qualified legal professionals before taking any action based on the information or tools provided by this engine. The developers of this project are not responsible for any adverse outcomes resulting from the use of this software.*
