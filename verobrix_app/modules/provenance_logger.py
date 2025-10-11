# verobrix_app/modules/provenance_logger.py
"""
Logs every action with semantic lineage and agent attribution.
Enables full traceability and authorship.
"""
import datetime
import json

class ProvenanceLogger:
    def __init__(self, log_file="provenance.log"):
        self.log_file = log_file

    def log_action(self, agent_name, action, context, input_data, output_data):
        """
        Logs an action performed by an agent.
        """
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "agent": agent_name,
            "action": action,
            "context": context,
            "input": input_data,
            "output": output_data
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(f"Logged action '{action}' by agent '{agent_name}'.")

if __name__ == '__main__':
    logger = ProvenanceLogger()
    logger.log_action(
        agent_name="JARVIS",
        action="Contradiction Detection",
        context="Analyzing a sample contract.",
        input_data={"text_snippet": "Clause 5 contradicts Clause 12."},
        output_data={"contradiction_found": True, "type": "structural"}
    )