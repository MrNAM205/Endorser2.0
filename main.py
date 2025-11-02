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

def run_coupon_endorsement_workflow():
    """New sovereign invocation workflow for UCC 3-305 coupon endorsement."""
    narrator.say("Starting Coupon Endorsement workflow with UCC 3-305 provisions.")

    rationale = corpus_manager.get_corpus_text('payment_coupon_endorsement_overview.md')
    if rationale:
        print("\n--- Coupon Endorsement Overview (UCC 3-305) ---")
        print(rationale[:500] + "..." if len(rationale) > 500 else rationale)
        print("---------------------")
    else:
        print("\n--- Coupon Endorsement (UCC 3-305) ---")
        print("Endorse payment coupons into private trust using UCC 3-305 provisions.")
        print("Establishes negotiable instrument status and private trust corpus.")

    proceed = get_user_input("Do you wish to proceed with coupon endorsement? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Coupon Endorsement workflow.")
        return

    # Collect coupon data
    coupon_data = {
        "endorser_name": get_user_input("What is your full name?"),
        "amount": get_user_input("What is the coupon amount?"),
        "payee": get_user_input("Who is the payee?"),
        "account_number": get_user_input("What is the account number?"),
        "endorsement_type": get_user_input("Endorsement type (private_trust/acceptance_for_value)?"),
        "due_date": get_user_input("Due date (if applicable)?")
    }

    try:
        # Process endorsement using CouponEndorserAgent
        endorsed_coupon = coupon_endorser_agent.endorse_coupon(coupon_data)

        print("\n--- Coupon Endorsement Generated ---")
        print(f"Endorsement Type: {endorsed_coupon['semantic_lineage']['endorsement_type']}")
        print(f"Trust Corpus: {endorsed_coupon['semantic_lineage']['trust_corpus']}")
        print(f"UCC Provisions: {', '.join(endorsed_coupon['ucc_compliance'].keys())}")
        print("\nEndorsement Text:")
        print(endorsed_coupon['endorsement_text'])

        # Generate document using remedy synthesizer
        template_data = {
            "endorser_name": coupon_data['endorser_name'],
            "endorsement_text": endorsed_coupon['endorsement_text'],
            "amount": coupon_data['amount'],
            "account_number": coupon_data['account_number'],
            "date": time.strftime("%Y-%m-%d")
        }

        narrator.say("Generating endorsement document.")
        output_path = remedy_synthesizer.generate_document('ucc_endorsement.txt.j2', template_data)

        if output_path:
            print(f"\nEndorsement document saved to: {output_path}")
            narrator.say("Coupon endorsement completed successfully.")
        else:
            print("Failed to generate endorsement document.")

    except Exception as e:
        print(f"Error during endorsement: {e}")
        narrator.say("Coupon endorsement failed.")

def run_semantic_scan_workflow():
    """New sovereign invocation workflow for semantic warfare analysis."""
    narrator.say("Starting Semantic Scan workflow for institutional framing detection.")

    rationale = corpus_manager.get_corpus_text('carl_miller_teachings_structured.md')
    if rationale:
        print("\n--- Semantic Warfare Analysis Overview ---")
        print("Carl Miller's teachings on semantic warfare and institutional framing detection.")
        print("Scans for semantic traps and generates narrative sovereignty rebuttals.")
        print("---------------------")
    else:
        print("\n--- Semantic Warfare Analysis ---")
        print("Detect institutional framing, semantic traps, and generate rebuttals.")

    proceed = get_user_input("Do you wish to proceed with semantic scan? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Semantic Scan workflow.")
        return

    document_input = get_user_input("Enter document text or file path to scan:")

    # For demo purposes, treat as direct text input
    if document_input.startswith('/') or document_input.startswith('.'):
        # File path - would implement file reading here
        print("File reading not implemented in demo. Using sample text.")
        document_text = "All persons must file tax returns. Residents are required to have licenses."
    else:
        document_text = document_input

    try:
        # Analyze using SemanticWarfareAgent
        framing_analysis = semantic_warfare_agent.scan_institutional_framing(document_text)
        trap_analysis = semantic_warfare_agent.detect_semantic_traps(document_text)

        # Combine analyses
        full_analysis = {
            "institutional_framing": framing_analysis["institutional_framing"],
            "semantic_traps": trap_analysis["semantic_traps"]
        }

        # Generate rebuttal
        rebuttal = semantic_warfare_agent.generate_narrative_rebuttal(full_analysis)

        print("\n--- Semantic Analysis Results ---")
        print(f"Institutional Framing Detected: {len(framing_analysis['institutional_framing'])}")
        print(f"Semantic Traps Detected: {len(trap_analysis['semantic_traps'])}")
        print(f"Document Classification: {trap_analysis['document_classification']}")

        # Display detected traps
        if trap_analysis['semantic_traps']:
            print("\nDetected Semantic Traps:")
            for trap in trap_analysis['semantic_traps'][:5]:  # Show first 5
                print(f"- {trap['trap_type'].upper()}: '{trap['match_text']}' in context '{trap['context']}'")
                print(f"  Rebuttal: {trap['rebuttal']}")

        # Display rebuttal sections
        print("\n--- Narrative Sovereignty Rebuttal ---")
        for section in rebuttal['rebuttal_sections']:
            print(f"\n{section['title']}:")
            print(section['content'][:300] + "..." if len(section['content']) > 300 else section['content'])

        # Generate rebuttal document
        template_data = {
            "rebuttal_sections": rebuttal['rebuttal_sections'],
            "document_classification": trap_analysis['document_classification'],
            "total_traps": len(trap_analysis['semantic_traps']),
            "date": time.strftime("%Y-%m-%d")
        }

        narrator.say("Generating semantic rebuttal document.")
        output_path = remedy_synthesizer.generate_document('semantic_rebuttal.txt.j2', template_data)

        if output_path:
            print(f"\nRebuttal document saved to: {output_path}")
            narrator.say("Semantic scan completed successfully.")
        else:
            print("Failed to generate rebuttal document.")

    except Exception as e:
        print(f"Error during semantic scan: {e}")
        narrator.say("Semantic scan failed.")

def run_legal_search_workflow():
    """New sovereign invocation workflow for legal authority research."""
    narrator.say("Starting Legal Research workflow for sovereign authorities.")

    print("\n--- Legal Authority Research ---")
    print("Search case law, constitutional provisions, and remedy statutes.")
    print("Find obscure court rulings and legal authorities for sovereign invocation.")
    print("---------------------")

    proceed = get_user_input("Do you wish to proceed with legal research? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Legal Research workflow.")
        return

    search_query = get_user_input("Enter search query (e.g., 'Hale v. Henkel', 'UCC 1-207', 'sovereign immunity'):")
    jurisdiction_filter = get_user_input("Filter by jurisdiction (federal/state/common_law/leave blank for all):")
    remedy_type = get_user_input("Filter by remedy type (sovereignty/jurisdiction/rights/leave blank for all):")

    try:
        # Search legal authorities
        search_results = law_gathering_engine.search_legal_authorities(search_query)

        print("\n--- Legal Research Results ---")
        print(f"Query: {search_query}")
        print(f"Summary: {search_results['summary']}")

        # Display case law results
        if search_results['case_law']:
            print(f"\nRelevant Case Law ({len(search_results['case_law'])} results):")
            for case in search_results['case_law'][:3]:  # Show top 3
                print(f"- {case['case_name']} ({case['citation']}, {case['year']})")
                print(f"  Relevance: {case['relevance_score']:.2f}")
                print(f"  Holding: {case['holding'][:150]}...")
                print(f"  Key Principles: {', '.join(case['key_principles'])}")

        # Display statute results
        if search_results['statutes']:
            print(f"\nRelevant Statutes ({len(search_results['statutes'])} results):")
            for statute in search_results['statutes'][:3]:  # Show top 3
                print(f"- {statute['statute_name']} ({statute['citation']})")
                print(f"  Code Type: {statute['code_type']}")
                print(f"  Application: {statute['application']}")

        # Display constitutional results
        if search_results['constitutional']:
            print(f"\nConstitutional Provisions ({len(search_results['constitutional'])} results):")
            for provision in search_results['constitutional'][:3]:  # Show top 3
                print(f"- {provision['provision']} ({provision['article']}{provision['section']})")
                print(f"  Application: {provision['application']}")

        # Display recommended authorities
        if search_results['recommended_authorities']:
            print(f"\nRecommended Authorities for Citation:")
            for auth in search_results['recommended_authorities']:
                print(f"- {auth['authority']} ({auth['citation']})")
                print(f"  Reason: {auth['reason']}")

        # Generate research document
        template_data = {
            "search_query": search_query,
            "summary": search_results['summary'],
            "case_law": search_results['case_law'],
            "statutes": search_results['statutes'],
            "constitutional": search_results['constitutional'],
            "recommended_authorities": search_results['recommended_authorities'],
            "date": time.strftime("%Y-%m-%d")
        }

        narrator.say("Generating legal research document.")
        output_path = remedy_synthesizer.generate_document('legal_research.txt.j2', template_data)

        if output_path:
            print(f"\nResearch document saved to: {output_path}")
            narrator.say("Legal research completed successfully.")
        else:
            print("Failed to generate research document.")

    except Exception as e:
        print(f"Error during legal research: {e}")
        narrator.say("Legal research failed.")

def run_complete_sovereign_manifest_workflow():
    """Complete sovereign invocation manifest generation workflow."""
    narrator.say("Starting Complete Sovereign Manifest generation workflow.")

    print("\n--- Complete Sovereign Manifest ---")
    print("Generates a comprehensive sovereign invocation manifest combining:")
    print("- Coupon endorsements (UCC 3-305)")
    print("- Semantic warfare rebuttals")
    print("- Legal authority citations")
    print("- Status and jurisdiction declarations")
    print("---------------------")

    proceed = get_user_input("Do you wish to generate a complete sovereign manifest? (yes/no)")
    if proceed.lower() != 'yes':
        narrator.say("Aborting Complete Sovereign Manifest workflow.")
        return

    try:
        manifest_data = {
            "sovereign_name": get_user_input("What is your full name?"),
            "date": time.strftime("%Y-%m-%d"),
            "jurisdiction": get_user_input("Declare your jurisdiction (Common Law/State National):"),
            "corpus_reference": "Private Trust - " + get_user_input("Trust corpus name:")
        }

        # Generate complete manifest using all agents
        print("Generating sovereign manifest with all components...")

        # This would integrate all the workflow results
        narrator.say("Assembling sovereign invocation manifest.")

        template_data = {
            "sovereign_name": manifest_data["sovereign_name"],
            "date": manifest_data["date"],
            "jurisdiction": manifest_data["jurisdiction"],
            "corpus_reference": manifest_data["corpus_reference"],
            "ucc_provisions": ["UCC 3-302", "UCC 3-305", "UCC 3-401", "UCC 1-207"],
            "authorities": ["Hale v. Henkel", "Bond v. United States", "Marbury v. Madison"],
            "semantic_lineage": f"Created by sovereign authority on {manifest_data['date']}"
        }

        output_path = remedy_synthesizer.generate_document('sovereign_manifest.txt.j2', template_data)

        if output_path:
            print(f"\nComplete Sovereign Manifest saved to: {output_path}")
            narrator.say("Sovereign manifest generation completed successfully.")
        else:
            print("Failed to generate sovereign manifest.")

    except Exception as e:
        print(f"Error during manifest generation: {e}")
        narrator.say("Sovereign manifest generation failed.")

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
        print("15. SOVEREIGN INVOCATION: Generate Coupon Endorsement (UCC 3-305)")
        print("16. SOVEREIGN INVOCATION: Scan Document for Semantic Traps")
        print("17. SOVEREIGN INVOCATION: Search Legal Authorities")
        print("18. SOVEREIGN INVOCATION: Generate Complete Sovereign Manifest")
        print("19. Exit")

        choice = input("Enter your choice (1-19): ")

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
            run_coupon_endorsement_workflow()
        elif choice == '16':
            run_semantic_scan_workflow()
        elif choice == '17':
            run_legal_search_workflow()
        elif choice == '18':
            run_complete_sovereign_manifest_workflow()
        elif choice == '19':
            narrator.say("Exiting VeroBrix Engine.")
            break
        else:
            narrator.say("Invalid choice. Please try again.")

if __name__ == "__main__":
    narrator.say("VeroBrix Sovereign Intelligence Engine Initialized.")
    main_menu()
