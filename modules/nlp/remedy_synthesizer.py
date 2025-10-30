import os
from jinja2 import Environment, FileSystemLoader
from modules.logger import system_logger, log_provenance
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

class RemedySynthesizer:
    def __init__(self, template_dir='templates', output_dir='output'):
        self.template_dir = os.path.abspath(template_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        os.makedirs(self.output_dir, exist_ok=True)

    def list_templates(self):
        return self.env.list_templates()

    def generate_document(self, template_name, data):
        try:
            template = self.env.get_template(template_name)
            rendered_content = template.render(data)

            output_filename = f"{template_name.replace('.j2', '')}_{data.get('recipient_name', 'output').replace(' ', '_')}.txt"
            output_path = os.path.join(self.output_dir, output_filename)

            with open(output_path, 'w') as f:
                f.write(rendered_content)
            
            system_logger.info(f"Successfully generated document: {output_path}")
            log_provenance(
                agent_name="RemedySynthesizer",
                action="GenerateDocument",
                details=f"Template: {template_name}, Output: {output_path}"
            )
            return output_path

        except Exception as e:
            system_logger.error(f"Failed to generate document: {e}")
            return None

    def generate_endorsement_overlay_pdf(self, original_pdf_path, endorsement_text, output_filename="endorsed_document.pdf"):
        """Generates a new PDF with endorsement text overlaid on the original PDF."""
        try:
            # Create a new PDF with ReportLab for the overlay
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Position the text (adjust x, y, font size as needed)
            can.setFont('Helvetica-Bold', 12)
            can.drawString(50, 750, endorsement_text) # Example position
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfReader(packet)
            
            # Read the original PDF
            existing_pdf = PdfReader(open(original_pdf_path, "rb"))
            output = PdfWriter()

            # Merge the new PDF (overlay) with the original PDF
            for i in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[i]
                if i == 0: # Apply overlay only to the first page for simplicity
                    page.merge_page(new_pdf.pages[0])
                output.add_page(page)

            output_path = os.path.join(self.output_dir, output_filename)
            with open(output_path, "wb") as output_stream:
                output.write(output_stream)
            
            system_logger.info(f"Successfully generated endorsed PDF: {output_path}")
            log_provenance(
                agent_name="RemedySynthesizer",
                action="GenerateEndorsementOverlay",
                details=f"Original: {original_pdf_path}, Endorsement: {endorsement_text}, Output: {output_path}"
            )
            return output_path

        except Exception as e:
            system_logger.error(f"Failed to generate endorsement overlay PDF: {e}")
            return None

# Singleton instance
remedy_synthesizer = RemedySynthesizer(
    template_dir='verobrix_engine/templates',
    output_dir='verobrix_engine/output'
)