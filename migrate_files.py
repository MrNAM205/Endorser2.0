import shutil
import os

# Define file migrations as (source, destination) pairs
migrations = [
    # NLP modules
    ("remedy_synthesizer.py", "modules/nlp/remedy_synthesizer.py"),
    ("nlp_processor.py", "modules/nlp/nlp_processor.py"),
    ("document_parser.py", "modules/nlp/document_parser.py"),
    ("corpus_manager.py", "modules/nlp/corpus_manager.py"),

    # Config and utilities
    ("config_manager.py", "modules/config/config_manager.py"),
    ("config.yaml", "modules/config/config.yaml"),
    ("logger.py", "modules/utils/logger.py"),
    ("file_watcher.py", "modules/utils/file_watcher.py"),
    ("system_monitor.py", "modules/utils/system_monitor.py"),

    # Agent logic
    ("voice_narrator.py", "modules/agent/voice_narrator.py"),

    # Cockpit projects
    ("verobrix", "cockpit/verobrix/verobrix"),
    ("verobrix_app", "cockpit/verobrix/verobrix_app"),
    ("verobrix_engine", "cockpit/verobrix/verobrix_engine"),
    ("VeroBrix-Agent", "cockpit/verobrix/VeroBrix-Agent"),
    ("Endorser", "cockpit/endorser/Endorser"),
    ("AutoTender_Sovereign", "cockpit/autotender/AutoTender_Sovereign"),
    ("sovereign--financial-cockpit", "cockpit/sovereign--financial-cockpit"),

    # Legacy projects
    ("sovereign-financial-cockpit-old", "legacy/sovereign-financial-cockpit-old"),
    ("old_agent_scripts", "legacy/old_agent_scripts"),
    ("old_scripts", "legacy/old_scripts"),

    # Documentation
    ("README.md", "docs/README.md"),
    ("DEVELOPMENT_DOCS.md", "docs/DEVELOPMENT_DOCS.md"),
    ("TECHNICAL_ROADMAP.md", "docs/TECHNICAL_ROADMAP.md"),
    ("SOVEREIGN_FINANCE_COCKPIT.md", "docs/SOVEREIGN_FINANCE_COCKPIT.md"),
    ("PROJECT_OVERVIEW.md", "docs/PROJECT_OVERVIEW.md"),
    ("PEOPLE_OF_INTEREST.md", "docs/PEOPLE_OF_INTEREST.md"),
]

# Perform migrations
for src, dst in migrations:
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"Moved: {src} → {dst}")
    else:
        print(f"Skipped (not found): {src}")
