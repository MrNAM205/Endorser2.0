from agents.base_agent import BaseAgent
from typing import Any, Dict, List

class DialogosAgent(BaseAgent):
    """
    Philosophical overlays and authorship prompts agent.
    """

    def get_capabilities(self) -> List[str]:
        return ["authorship_prompts"]

    def analyze(self, input_data: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyzes the input text for foundational concepts and generates
        philosophical prompts to guide the user's authorship.
        """
        prompts = []
        text_lower = input_data.lower()

        # Define foundational concepts and associated guiding questions
        concept_map = {
            'consent': {
                'question': 'This document mentions consent. Are you consenting to their jurisdiction, or are you stating your own terms? True consent must be knowing, willing, and voluntary.',
                'foundational_principle': 'Consent of the governed'
            },
            'right': {
                'question': 'The word "right" appears. Are you claiming a right or asking for a privilege? A right is inherent and cannot be granted or denied, only violated.',
                'foundational_principle': 'Inherent and unalienable rights'
            },
            'must': {
                'question': 'The document uses the word "must," implying a mandatory obligation. Is this obligation established by a contract you have knowingly entered into, or is it a presumption? Consider challenging the source of the alleged obligation.',
                'foundational_principle': 'Contract and voluntary obligation'
            },
            'jurisdiction': {
                'question': 'Jurisdiction is mentioned. Is their jurisdiction presumed or proven? All jurisdiction must be proven on the record. Consider how you can challenge this presumption.',
                'foundational_principle': 'Lawful and proven jurisdiction'
            }
        }

        for keyword, data in concept_map.items():
            if keyword in text_lower:
                prompts.append({
                    'concept': keyword.capitalize(),
                    'guiding_question': data['question'],
                    'foundational_principle': data['foundational_principle']
                })

        if not prompts:
            prompts.append({
                'concept': 'Authorship',
                'guiding_question': 'Does this document speak as the author and creator of the record, or as a subject responding to a higher authority? Every word you write creates your standing.',
                'foundational_principle': 'Sovereignty through authorship'
            })

        return {"authorship_prompts": prompts}