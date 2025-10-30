import spacy
from modules.config_manager import config_manager
from modules.logger import system_logger

class NlpProcessor:
    def __init__(self):
        model = config_manager.get('nlp.model')
        try:
            self.nlp = spacy.load(model)
            system_logger.info(f"spaCy model '{model}' loaded successfully.")
        except Exception as e:
            system_logger.error(f"Failed to load spaCy model '{model}': {e}")
            self.nlp = None

    def process_text(self, text):
        if not self.nlp:
            return {"classification": "unknown", "entities": {}}

        doc = self.nlp(text)

        # --- Entity Extraction ---
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        # --- Simple Classification (can be improved later) ---
        classification = "general"
        keywords = {
            "legal": ["legal", "court", "affidavit", "law", "judge"],
            "technical": ["technical", "python", "code", "software", "bug"]
        }
        for cat, keys in keywords.items():
            if any(key in text.lower() for key in keys):
                classification = cat
                break
        
        return {
            "classification": classification,
            "entities": entities,
            "text_content": text
        }

# Singleton instance
nlp_processor = NlpProcessor()