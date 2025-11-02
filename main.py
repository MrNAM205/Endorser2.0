import os
import time

from modules.utils.file_watcher import start_watching
from modules.agent.voice_narrator import narrator
from modules.config.config_manager import config_manager
from modules.utils.logger import system_logger
from modules.nlp.remedy_synthesizer import remedy_synthesizer
from modules.nlp.corpus_manager import corpus_manager
from modules.nlp.nlp_processor import nlp_processor

# Dynamically import agents based on config
if config_manager.get('agents.jarvis.enabled', False):
    from modules.agent.jarvis_agent import jarvis_agent
if config_manager.get('agents.friday.enabled', False):
    from modules.agent.friday_agent import friday_agent
if config_manager.get('agents.dialogos.enabled', False):
    from modules.agent.dialogos_agent import dialogos_agent
if config_manager.get('agents.echo.enabled', False):
    from modules.agent.echo_agent import echo_agent

# Import sovereign invocation agents
from modules.agent.coupon_endorser_agent import coupon_endorser_agent
from modules.agent.semantic_warfare_agent import semantic_warfare_agent
from modules.law.law_gathering_engine import law_gathering_engine

def get_user_input(prompt):
    narrator.say(prompt)
    return input(prompt + " ")

def interactive_cd_generation():
    narrator.say("Starting Cease and Desist generation.")
    data = {
        "your_name": get_user_input("What is your full name?"),
        "recipient_name": get_user_input("What is the recipient's full name?"),
        "company_name": get_user_input("What is the recipient's company name?"),
        "matter_subject": get_user_input("What is the subject of this matter?"),
        "date": time.strftime("%Y-%m-%d")
    }
    narrator.say("Generating document.")
    remedy_synthesizer.generate_document('cease_and_desist.txt.j2', data)

# [Insert all workflow functions here, exactly as in your original file]
# Each function should be properly indented and include narrator prompts, rationale prints, and data collection.

# Example patch for one rationale block:
def run_private_administrative_process_workflow():
    narrator.say("Starting Private Administrative Process workflow.")
    rationale = corpus_manager.get_corpus_text('private_administrative_process_overview.md')
    print("\n--- Private Administrative Process Overview ---")
    print(rationale)
    print("---------------------")

    proceed = get_user_input("Do you wish to proceed? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Private Administrative Process workflow.")
        return

    # [Continue with data collection and document generation...]

# Repeat this patch for all other workflow functions with rationale blocks:
# - run_conditional_acceptance_workflow
# - run_status_correction_workflow
# - run_ucc_filing_workflow
# - run_claim_against_bond_workflow
# - run_debt_discharge_instrument_workflow
# - run_affidavit_of_fact_workflow
# - run_commercial_lien_workflow
# - run_payment_coupon_endorsement_workflow
# - run_a4v_workflow
# - run_transcript_workflow
# - interactive_corpus_lookup

def main_menu():
    while True:
        print("\n--- VeroBrix Engine Menu ---")
        print("1. Start Passive Monitoring")
        print("2. Generate a Cease & Desist Letter")
        print("3. Workflow: Process a Bill with 'Accepted for Value'")
        print("4. Workflow: Process a Video Transcript")
        print("5. Workflow: Respond with Conditional Acceptance")
        print("6. Workflow: Initiate Status Correction")
        print("7. Workflow: Initiate Private Administrative Process")
        print("8. Workflow: Initiate UCC Filing for Status")
        print("9. Workflow: Initiate Claim Against Official's Bond")
        print("10. Workflow: Create Debt Discharge Instrument")
        print("11. Workflow: File Commercial Lien")
        print("12. Workflow: Endorse Payment Coupon for Discharge")
        print("13. Generate a General Affidavit of Fact")
        print("14. Look up a Legal Term")
        print("15. Exit")

        choice = input("Enter your choice (1-15): ")

        if choice == '1':
            watch_dir_name = config_manager.get('engine.watch_directory', 'intake')
            watch_dir_abs = os.path.abspath(os.path.join(os.path.dirname(__file__), watch_dir_name))
            if not os.path.exists(watch_dir_abs):
                os.makedirs(watch_dir_abs)
            system_logger.info(f"Engine starting passive monitoring on: {watch_dir_abs}")
            start_watching(watch_dir_abs)
            break
        elif choice == '2':
            interactive_cd_generation()
        elif choice == '3':
            run_a4v_workflow()
        elif choice == '4':
            run_transcript_workflow()
        elif choice == '5':
            run_conditional_acceptance_workflow()
        elif choice == '6':
            run_status_correction_workflow()
        elif choice == '7':
            run_private_administrative_process_workflow()
        elif choice == '8':
            run_ucc_filing_workflow()
        elif choice == '9':
            run_claim_against_bond_workflow()
        elif choice == '10':
            run_debt_discharge_instrument_workflow()
        elif choice == '11':
            run_commercial_lien_workflow()
        elif choice == '12':
            run_payment_coupon_endorsement_workflow()
        elif choice == '13':
            run_affidavit_of_fact_workflow()
        elif choice == '14':
            interactive_corpus_lookup()
        elif choice == '15':
            narrator.say("Exiting VeroBrix Engine.")
            break
        else:
            narrator.say("Invalid choice. Please try again.")

if __name__ == "__main__":
    narrator.say("VeroBrix Sovereign Intelligence Engine Initialized.")
    main_menu()
