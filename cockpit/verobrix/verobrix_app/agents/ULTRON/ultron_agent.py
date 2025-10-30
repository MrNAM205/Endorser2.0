from agents.base_agent import BaseAgent
from typing import Any, Dict, List

# A simple, temporary search function. This would be replaced by a more robust tool.
# For now, it simulates searching files in a directory.
import os
def search_corpus(directory: str, keywords: List[str]) -> List[str]:
    findings = []
    if not os.path.isdir(directory):
        return findings
    for filename in os.listdir(directory):
        if filename.endswith('.txt'): # Assuming legal texts are .txt files
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        for keyword in keywords:
                            if keyword.lower() in line.lower():
                                findings.append(f"Found '{keyword}' in {filename}, line {i}: {line.strip()}")
                                # Return first finding for simplicity
                                return findings 
            except Exception:
                pass # Ignore files that can't be read
    return findings

class UltronAgent(BaseAgent):
    """
    Autonomous, predictive, and cautionary analysis agent.
    It searches the legal corpus for relevant codes to generate strategies.
    """

    def get_capabilities(self) -> List[str]:
        return ["strategic_recommendations"]

    def analyze(self, input_data: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyzes the situation and generates strategic legal recommendations
        by searching a corpus of legal documents.
        """
        recommendations = []
        situation_type = context.get('situation', {}).get('type', 'general')
        
        # Define keywords for each situation type
        search_map = {
            'fee_demand': ['tender', 'obligation', 'discharge'],
            'court_summons': ['jurisdiction', 'summons', 'appearance', 'due process'],
            'traffic_stop': ['travel', 'right', 'license', 'commercial']
        }
        
        keywords_to_search = search_map.get(situation_type, [])
        
        if keywords_to_search:
            # In a real scenario, we would use a proper tool to get the corpus path.
            # For now, we hardcode a relative path for the simulation.
            corpus_path = os.path.join(os.path.dirname(__file__), '../../corpus/legal')
            findings = search_corpus(corpus_path, keywords_to_search)
            
            if findings:
                for finding in findings:
                    recommendations.append(self._create_recommendation_from_finding(finding))

        if not recommendations:
            recommendations.append({
                'strategy': 'General Defensive Posture',
                'legal_basis': 'Common Law',
                'guidance': 'When the specific legal context is unclear, reserve all rights, challenge jurisdiction, and demand that all claims be proven on the record.'
            })

        return {"strategic_recommendations": recommendations}

    def _create_recommendation_from_finding(self, finding: str) -> Dict[str, str]:
        """
        Creates a structured recommendation based on a raw finding from the corpus.
        This is a placeholder for more sophisticated logic.
        """
        # Example finding: "Found 'tender' in U.C.C.txt, line 123: ...tender of payment..."
        parts = finding.split(' ')
        keyword = parts[1].strip("'")
        basis = parts[3].strip(',')

        guidance_map = {
            'tender': 'This involves formally offering full payment. If the offer is lawful and is refused, it can have specific legal consequences for the one refusing, potentially discharging your obligation to pay further interest or penalties.',
            'jurisdiction': 'This involves formally questioning the authority of the court or entity over you. It requires a special appearance and a formal motion challenging their power to compel you.',
            'travel': 'This involves asserting the fundamental right to travel, distinct from the licensed privilege of driving for commercial purposes. It often forms the basis for challenging the applicability of traffic statutes to a private, non-commercial individual.'
        }

        return {
            'strategy': f"Leverage the concept of '{keyword.capitalize()}'",
            'legal_basis': f"As referenced in {basis}",
            'guidance': guidance_map.get(keyword, 'No specific guidance available. Research this legal term for its application to your situation.')
        }