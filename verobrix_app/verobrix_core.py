import os
import json
from datetime import datetime

from modules.config_manager import config
from modules.agent_manager import AgentManager
from modules.remedy_synthesizer import RemedySynthesizer
from modules.situation_interpreter import SituationInterpreter
from modules.provenance_logger import get_provenance_logger, log_provenance
from modules.sovereignty_scorer import get_sovereignty_scorer

class VeroBrixSystem:
    """
    Enhanced VeroBrix Sovereign Modular Intelligence System.
    """
    
    def __init__(self):
        """Initializes the VeroBrixSystem with its core components."""
        self.agent_manager = AgentManager()
        self.remedy_synthesizer = RemedySynthesizer()
        self.situation_interpreter = SituationInterpreter()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.provenance_logger = get_provenance_logger()
        self.sovereignty_scorer = get_sovereignty_scorer()
        os.makedirs(config.get_logs_path(), exist_ok=True)
        os.makedirs(config.get_output_path(), exist_ok=True)
        log_provenance("VeroBrix System", f"Initialized new session: {self.session_id}")
    
    def analyze_situation(self, input_text: str, situation_context: dict = None) -> dict:
        """Performs a comprehensive analysis of a legal situation."""
        log_provenance("VeroBrix System", "Starting comprehensive situation analysis")
        
        situation = self.situation_interpreter.interpret_situation(input_text, situation_context)
        
        jarvis = self.agent_manager.get_agent('jarvis')
        friday = self.agent_manager.get_agent('friday')
        ultron = self.agent_manager.get_agent('ultron')
        dialogos = self.agent_manager.get_agent('dialogos')

        jarvis_analysis = jarvis.analyze(input_text)
        friday_analysis = friday.analyze(input_text, context=jarvis_analysis)
        ultron_analysis = ultron.analyze(input_text, context={'situation': situation})
        dialogos_analysis = dialogos.analyze(input_text)

        sovereignty_metrics = self.sovereignty_scorer.score_text(input_text, context="legal_document")
        
        remedy_input = {
            'type': situation['type'],
            'risk_level': friday_analysis['legal_summary']['risk_level'],
            'contradictions': jarvis_analysis['contradictions'],
            'tone_analysis': friday_analysis['tone_analysis'],
            'urgency': situation['urgency'],
            'jurisdiction': situation['jurisdiction'],
            'legal_framework': situation['legal_framework']
        }
        remedy = self.remedy_synthesizer.synthesize_remedy(remedy_input)
        remedy_sovereignty = self.sovereignty_scorer.score_decision({})

        results = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'system_version': 'VeroBrix v2.3 - Status Correction',
            'input': {'raw_text': input_text, 'context': situation_context},
            'situation_analysis': situation,
            'legal_analysis': {**jarvis_analysis, **friday_analysis},
            'strategic_recommendations': ultron_analysis,
            'authorship_prompts': dialogos_analysis,
            'sovereignty_analysis': {
                'input_sovereignty': sovereignty_metrics.__dict__,
                'remedy_sovereignty': remedy_sovereignty.__dict__
            },
            'remedy': remedy,
            'recommendations': self._generate_recommendations(situation, friday_analysis['legal_summary'], remedy, sovereignty_metrics)
        }
        
        # Generate the new report and add it to the results
        results['status_correction_report'] = self._generate_status_correction_report(results)
        
        log_provenance("VeroBrix System", "Comprehensive analysis completed")
        return results

    def _generate_status_correction_report(self, results: dict) -> list:
        """Synthesizes all agent outputs into a single, actionable checklist."""
        report = []
        sovereignty = results.get('sovereignty_analysis', {}).get('input_sovereignty', {})
        recommendations = results.get('recommendations', {})
        ultron_recs = results.get('strategic_recommendations', {}).get('strategic_recommendations', [])
        dialogos_prompts = results.get('authorship_prompts', {}).get('authorship_prompts', [])

        report.append("**STATUS CORRECTION CHECKLIST:** This report synthesizes all agent findings into actionable steps to improve your sovereign standing.")

        # 1. Sovereignty Score
        if sovereignty.get('sovereignty_level') == 'Servile':
            report.append(f"**Priority 1: Address Servile Language.** Your document scores as 'Servile' ({sovereignty.get('overall_score', 0):.2f}/1.00). Review the improvement suggestions immediately.")
            for suggestion in sovereignty.get('improvement_suggestions', []):
                report.append(f"  - Suggestion: {suggestion}")
        else:
            report.append(f"**Posture Analysis:** Your document scores as '{sovereignty.get('sovereignty_level')}' ({sovereignty.get('overall_score', 0):.2f}/1.00). Maintain this frame.")

        # 2. Immediate Actions
        immediate_actions = recommendations.get('immediate_actions', [])
        if immediate_actions:
            report.append("**Priority 2: Take Immediate Actions.** The system has identified urgent risks.")
            for action in immediate_actions:
                report.append(f"  - Action: {action}")

        # 3. Strategic Legal Actions (from Ultron)
        if ultron_recs:
            report.append("**Priority 3: Review Strategic Legal Options.** Ultron has identified the following strategies based on the legal corpus.")
            for rec in ultron_recs:
                report.append(f"  - Strategy: {rec.get('strategy')}. Basis: {rec.get('legal_basis')}. Guidance: {rec.get('guidance')}")

        # 4. Authorship and Framing (from Dialogos)
        if dialogos_prompts:
            report.append("**Priority 4: Refine Your Authorship.** Dialogos offers these prompts to strengthen your standing.")
            for prompt in dialogos_prompts:
                report.append(f"  - Concept: {prompt.get('concept')}. Question: {prompt.get('guiding_question')}")

        return report

    def _generate_recommendations(self, situation: dict, legal_summary: dict, remedy: dict, sovereignty_metrics=None) -> dict:
        """Generates prioritized recommendations based on the analysis."""
        # ... (This method remains the same)
        recommendations = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'warnings': [],
            'opportunities': [],
            'sovereignty_improvements': []
        }
        
        if sovereignty_metrics:
            if sovereignty_metrics.sovereignty_level == "Servile":
                recommendations['warnings'].append('SOVEREIGNTY WARNING: Language contains servile patterns')
                recommendations['sovereignty_improvements'].extend(sovereignty_metrics.improvement_suggestions)
            elif sovereignty_metrics.sovereignty_level == "Transitional":
                recommendations['opportunities'].append('SOVEREIGNTY OPPORTUNITY: Language shows transitional sovereignty - can be improved')
                recommendations['sovereignty_improvements'].extend(sovereignty_metrics.improvement_suggestions[:3])
        
        if situation['urgency']['level'] == 'high':
            recommendations['immediate_actions'].extend([
                'URGENT: Time-sensitive situation detected',
                'Review all deadlines and timelines immediately',
                'Consider emergency legal consultation'
            ])
        
        if legal_summary['risk_level'] == 'HIGH':
            recommendations['immediate_actions'].append('HIGH RISK: Seek immediate legal counsel')
            recommendations['warnings'].append('Situation contains high-risk legal elements')

        return recommendations

    def _save_analysis_results(self, results: dict):
        """Saves the analysis results to a JSON file."""
        output_dir = config.get_output_path()
        filename = os.path.join(output_dir, f"verobrix_analysis_{self.session_id}.json")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            log_provenance("VeroBrix System", f"Analysis results saved to {filename}")
        except Exception as e:
            log_provenance("VeroBrix System", f"Error saving results: {e}")

    def generate_document(self, template_name: str, variables: dict) -> str:
        """Generates a legal document."""
        log_provenance("VeroBrix System", f"Generating document: {template_name}")
        return self.remedy_synthesizer.generate_document(template_name, variables)

    def get_available_templates(self) -> list:
        """Gets a list of available document templates."""
        return self.remedy_synthesizer.get_available_templates()

    def print_analysis_summary(self, results: dict):
        """Prints a formatted summary of the analysis results."""
        print("\n" + "="*60)
        print("VEROBRIX SOVEREIGN INTELLIGENCE ANALYSIS")
        print("="*60)
        
        print(f"Session ID: {results.get('session_id', 'N/A')}")
        print(f"System Version: {results.get('system_version', 'N/A')}")
        print(f"Analysis Time: {results.get('timestamp', 'N/A')}")
        
        # ... (other sections remain the same)

        # Status Correction Report
        report = results.get('status_correction_report', [])
        if report:
            print("\n" + "-"*20 + " STATUS CORRECTION REPORT " + "-"*21)
            for item in report:
                print(f"- {item}")
        
        print("\n" + "="*60)
