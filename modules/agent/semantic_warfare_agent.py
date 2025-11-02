from modules.logger import log_provenance, system_logger
from modules.corpus_manager import corpus_manager
from modules.nlp.remedy_synthesizer import remedy_synthesizer
import re
import json
from datetime import datetime

class SemanticWarfareAgent:
    """
    Implements Carl Miller's semantic warfare detection and rebuttal strategies.
    Detects institutional framing, adhesion contracts, and semantic traps.
    """

    def __init__(self):
        self.carl_miller_teachings = corpus_manager.get_corpus_text('carl_miller_teachings_structured.md')
        if not self.carl_miller_teachings:
            system_logger.warning("Carl Miller teachings not loaded. Semantic Warfare agent will have limited analysis.")

        # Define semantic trap patterns based on Carl Miller's teachings
        self.semantic_trap_patterns = {
            "person": {
                "pattern": r'\b(person|persons|people)\b',
                "description": "Institutional construct reducing sovereign to legal fiction",
                "rebuttal": "I am a living man/woman, not a legal 'person' or corporate fiction"
            },
            "resident": {
                "pattern": r'\b(resident|resides|residence)\b',
                "description": "Presumption of domicile in corporate jurisdiction",
                "rebuttal": "I am a state national, not a 'resident' of any corporate municipality"
            },
            "liable": {
                "pattern": r'\b(liable|liability|responsible for|obligated)\b',
                "description": "Imposition of statutory obligation without consent",
                "rebuttal": "I am not 'liable' for obligations I did not voluntarily consent to"
            },
            "citizen": {
                "pattern": r'\b(citizen|citizenship|u\.s\. citizen)\b',
                "description": "Presumption of federal citizenship and subject status",
                "rebuttal": "I am an American State National, not a U.S. citizen subject"
            },
            "must": {
                "pattern": r'\b(must|shall|required to|compelled to)\b',
                "description": "Command language removing choice and consent",
                "rebuttal": "Nothing is required without my informed and voluntary consent"
            },
            "taxpayer": {
                "pattern": r'\b(taxpayer|taxes|taxed)\b',
                "description": "Presumption of tax liability and voluntary compliance",
                "rebuttal": "I am not a 'taxpayer' as defined by Internal Revenue Code"
            },
            "driver": {
                "pattern": r'\b(driver|driving|license to drive)\b',
                "description": "Regulation of travel as privilege requiring license",
                "rebuttal": "I exercise my right to travel, not 'drive' as commercial activity"
            },
            "employee": {
                "pattern": r'\b(employee|employment|work for)\b',
                "description": "Presumption of employer-employee relationship",
                "rebuttal": "I am an independent contractor, not an 'employee' subject to employer control"
            },
            "consumer": {
                "pattern": r'\b(consumer|consumption|customer)\b',
                "description": "Classification as passive consumer rather than sovereign producer",
                "rebuttal": "I am a producer and sovereign, not a 'consumer' subject to regulation"
            },
            "subject": {
                "pattern": r'\b(subject to|subject of|subjected to)\b',
                "description": "Declaration of subjection to external authority",
                "rebuttal": "I am subject only to laws I have consented to through contract"
            }
        }

        # Institutional framing patterns
        self.institutional_framing_patterns = {
            "government_authority": {
                "pattern": r'\b(government has authority|official capacity|acting under color of law)\b',
                "description": "Presumption of government authority over sovereign individuals",
                "rebuttal": "Government officials are public servants, not authorities over sovereigns"
            },
            "statutory_jurisdiction": {
                "pattern": r'\b(statute|regulation|code|ordinance)\b',
                "description": "Application of statutory law to sovereign individuals",
                "rebuttal": "Statutes apply only to corporate entities, not sovereign individuals"
            },
            "contractual_adhesion": {
                "pattern": r'\b(by using|you agree|terms of service|acceptance of|consent to)\b',
                "description": "Implied consent through adhesion contracts",
                "rebuttal": "Silence and inaction do not constitute consent to any contract"
            },
            "presumption_consent": {
                "pattern": r'\b(it is presumed|we assume|unless you object)\b',
                "description": "Presumption creates burden to rebut",
                "rebuttal": "All presumptions are rebutted. No consent exists unless expressly given"
            }
        }

    def scan_institutional_framing(self, document_text):
        """
        Scans document for institutional framing patterns.

        Args:
            document_text (str): Text to analyze

        Returns:
            dict: Detected framing patterns with positions and rebuttals
        """
        log_provenance("SemanticWarfare", "ScanInstitutionalFraming", "Starting institutional framing analysis")

        detected_framing = []

        for framing_type, pattern_info in self.institutional_framing_patterns.items():
            pattern = pattern_info["pattern"]
            description = pattern_info["description"]
            rebuttal = pattern_info["rebuttal"]

            matches = re.finditer(pattern, document_text, re.IGNORECASE)

            for match in matches:
                # Extract context around the match
                start_pos = max(0, match.start() - 50)
                end_pos = min(len(document_text), match.end() + 50)
                context = document_text[start_pos:end_pos].strip()

                detected_framing.append({
                    "type": framing_type,
                    "pattern": pattern,
                    "match_text": match.group(),
                    "position": match.start(),
                    "context": context,
                    "description": description,
                    "rebuttal": rebuttal,
                    "severity": "high" if framing_type in ["government_authority", "statutory_jurisdiction"] else "medium"
                })

        analysis_result = {
            "document_length": len(document_text),
            "total_framing_detected": len(detected_framing),
            "institutional_framing": detected_framing,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "framing_categories": {
                "government_authority": [f for f in detected_framing if f["type"] == "government_authority"],
                "statutory_jurisdiction": [f for f in detected_framing if f["type"] == "statutory_jurisdiction"],
                "contractual_adhesion": [f for f in detected_framing if f["type"] == "contractual_adhesion"],
                "presumption_consent": [f for f in detected_framing if f["type"] == "presumption_consent"]
            }
        }

        log_provenance("SemanticWarfare", "FramingAnalysisComplete", f"Detected {len(detected_framing)} framing patterns")
        return analysis_result

    def detect_semantic_traps(self, document_text):
        """
        Detects semantic traps in document text.

        Args:
            document_text (str): Text to analyze

        Returns:
            dict: Detected semantic traps with analysis
        """
        log_provenance("SemanticWarfare", "DetectSemanticTraps", "Starting semantic trap detection")

        detected_traps = []

        for trap_type, pattern_info in self.semantic_trap_patterns.items():
            pattern = pattern_info["pattern"]
            description = pattern_info["description"]
            rebuttal = pattern_info["rebuttal"]

            matches = re.finditer(pattern, document_text, re.IGNORECASE)

            for match in matches:
                # Extract surrounding context
                start_pos = max(0, match.start() - 30)
                end_pos = min(len(document_text), match.end() + 30)
                context = document_text[start_pos:end_pos].strip()

                detected_traps.append({
                    "trap_type": trap_type,
                    "pattern": pattern,
                    "match_text": match.group(),
                    "position": match.start(),
                    "context": context,
                    "description": description,
                    "rebuttal": rebuttal,
                    "trap_category": self._categorize_trap(trap_type),
                    "severity": self._assess_trap_severity(trap_type, context)
                })

        # Analyze trap density and patterns
        trap_analysis = self._analyze_trap_patterns(detected_traps, document_text)

        result = {
            "total_traps_detected": len(detected_traps),
            "semantic_traps": detected_traps,
            "trap_analysis": trap_analysis,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "document_classification": self._classify_document_semantics(detected_traps)
        }

        log_provenance("SemanticWarfare", "TrapDetectionComplete", f"Detected {len(detected_traps)} semantic traps")
        return result

    def generate_narrative_rebuttal(self, semantic_analysis):
        """
        Generates narrative sovereignty rebuttal based on semantic analysis.

        Args:
            semantic_analysis (dict): Results from semantic trap detection

        Returns:
            dict: Rebuttal document with narrative sovereignty declarations
        """
        log_provenance("SemanticWarfare", "GenerateNarrativeRebuttal", "Generating narrative sovereignty rebuttal")

        semantic_traps = semantic_analysis.get("semantic_traps", [])
        institutional_framing = semantic_analysis.get("institutional_framing", [])

        # Generate rebuttal sections
        rebuttal_sections = []

        # 1. Sovereign Declaration
        sovereign_declaration = self._generate_sovereign_declaration()
        rebuttal_sections.append({
            "title": "SOVEREIGN STATUS DECLARATION",
            "content": sovereign_declaration
        })

        # 2. Semantic Trap Rebuttals
        if semantic_traps:
            trap_rebuttals = self._generate_trap_rebuttals(semantic_traps)
            rebuttal_sections.append({
                "title": "SEMANTIC TRAP REBUTTALS",
                "content": trap_rebuttals
            })

        # 3. Institutional Framing Rebuttals
        if institutional_framing:
            framing_rebuttals = self._generate_framing_rebuttals(institutional_framing)
            rebuttal_sections.append({
                "title": "INSTITUTIONAL FRAMING REBUTTALS",
                "content": framing_rebuttals
            })

        # 4. Narrative Sovereignty Declaration
        narrative_declaration = self._generate_narrative_sovereignty_declaration()
        rebuttal_sections.append({
            "title": "NARRATIVE SOVEREIGNTY DECLARATION",
            "content": narrative_declaration
        })

        # Create complete rebuttal document
        rebuttal_document = {
            "title": "NARRATIVE SOVEREIGNTY REBUTTAL",
            "created_at": datetime.utcnow().isoformat(),
            "jurisdiction": "Common Law",
            "authority": "Sovereign Individual",
            "rebuttal_sections": rebuttal_sections,
            "semantic_lineage": {
                "author": "Sovereign Individual",
                "basis": "Carl Miller semantic warfare analysis",
                "authority": "Common Law and Natural Rights",
                "original_analysis": semantic_analysis
            },
            "ucl_preservation": "WITHOUT PREJUDICE UCC 1-207"
        }

        log_provenance("SemanticWarfare", "RebuttalGenerated", "Successfully generated narrative sovereignty rebuttal")
        return rebuttal_document

    def _categorize_trap(self, trap_type):
        """Categorizes semantic trap type."""
        categories = {
            "person": "identity_framing",
            "resident": "jurisdiction_presumption",
            "liable": "obligation_imposition",
            "citizen": "status_presumption",
            "must": "coercive_language",
            "taxpayer": "financial_obligation",
            "driver": "rights_regulation",
            "employee": "labor_classification",
            "consumer": "economic_classification",
            "subject": "authority_subjection"
        }
        return categories.get(trap_type, "other")

    def _assess_trap_severity(self, trap_type, context):
        """Assesses severity of semantic trap based on type and context."""
        high_severity_traps = ["person", "citizen", "liable", "subject"]
        if trap_type in high_severity_traps:
            return "high"

        # Check context for severity indicators
        if any(word in context.lower() for word in ["required", "mandatory", "must", "compelled"]):
            return "high"
        elif any(word in context.lower() for word in ["should", "encouraged", "recommended"]):
            return "medium"
        else:
            return "low"

    def _analyze_trap_patterns(self, detected_traps, document_text):
        """Analyzes patterns in detected semantic traps."""
        trap_types = [trap["trap_type"] for trap in detected_traps]
        trap_categories = [trap["trap_category"] for trap in detected_traps]
        severity_counts = {"high": 0, "medium": 0, "low": 0}

        for trap in detected_traps:
            severity_counts[trap["severity"]] += 1

        # Calculate trap density (traps per 1000 characters)
        trap_density = (len(detected_traps) / len(document_text)) * 1000 if document_text else 0

        return {
            "most_common_traps": self._get_most_common_items(trap_types),
            "most_common_categories": self._get_most_common_items(trap_categories),
            "severity_distribution": severity_counts,
            "trap_density": round(trap_density, 2),
            "total_trap_types": len(set(trap_types))
        }

    def _classify_document_semantics(self, semantic_traps):
        """Classifies document based on semantic content."""
        if not semantic_traps:
            return "clean"

        trap_count = len(semantic_traps)
        high_severity_count = len([t for t in semantic_traps if t["severity"] == "high"])

        if high_severity_count >= 3:
            return "high_risk_adhesion"
        elif trap_count >= 5:
            return "moderate_semantic_warfare"
        elif trap_count >= 2:
            return "low_level_framing"
        else:
            return "minimal_semantic_issues"

    def _generate_sovereign_declaration(self):
        """Generates sovereign status declaration."""
        return """
I, a living man/woman, hereby declare and affirm:

1. I am a sovereign individual created by my Creator with inalienable rights
2. I am an American State National, not a U.S. citizen or corporate fiction
3. I am subject only to Common Law and laws I have expressly consented to
4. I reserve all rights under UCC 1-207 without prejudice
5. I am the principal author of my legal and commercial affairs

All presumptions to the contrary are hereby rebutted and dismissed.
"""

    def _generate_trap_rebuttals(self, semantic_traps):
        """Generates specific rebuttals for detected semantic traps."""
        rebuttal_text = "REBUTTAL OF SEMANTIC TRAPS:\n\n"

        for trap in semantic_traps:
            rebuttal_text += f"{trap['trap_type'].upper()} TRAP DETECTED:\n"
            rebuttal_text += f"Context: '{trap['context']}'\n"
            rebuttal_text += f"Rebuttal: {trap['rebuttal']}\n\n"

        return rebuttal_text

    def _generate_framing_rebuttals(self, institutional_framing):
        """Generates rebuttals for institutional framing."""
        rebuttal_text = "REBUTTAL OF INSTITUTIONAL FRAMING:\n\n"

        for framing in institutional_framing:
            rebuttal_text += f"{framing['type'].upper()} FRAMING DETECTED:\n"
            rebuttal_text += f"Context: '{framing['context']}'\n"
            rebuttal_text += f"Rebuttal: {framing['rebuttal']}\n\n"

        return rebuttal_text

    def _generate_narrative_sovereignty_declaration(self):
        """Generates narrative sovereignty declaration."""
        return """
NARRATIVE SOVEREIGNTY DECLARATION:

I hereby reclaim narrative control over my legal and commercial affairs.

I am not defined by institutional language or semantic constructs.
I am not subject to presumptions or implied contracts.
I am the author of my own legal narrative.

Any document, notice, or communication that attempts to define me through
institutional language is hereby rebutted and returned without prejudice.

I operate under narrative sovereignty, where my words and declarations
have primacy over any institutional framing or semantic warfare.

This declaration serves as notice to all parties that I operate under
my own narrative authority and do not consent to institutional definitions
or semantic traps.

WITHOUT PREJUDICE UCC 1-207
All Rights Reserved
"""

    def _get_most_common_items(self, items):
        """Returns most common items from a list."""
        if not items:
            return []

        item_counts = {}
        for item in items:
            item_counts[item] = item_counts.get(item, 0) + 1

        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"item": item, "count": count} for item, count in sorted_items[:5]]

# Singleton instance
semantic_warfare_agent = SemanticWarfareAgent()