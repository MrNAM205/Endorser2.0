import os

# Define modular directory structure
directories = [
    "modules/config",
    "modules/nlp",
    "modules/utils",
    "modules/agent",
    "modules/ui",
    "cockpit/verobrix",
    "cockpit/endorser",
    "cockpit/autotender",
    "shared/templates",
    "shared/assets",
    "shared/logs",
    "shared/output",
    "legacy/old_agent_scripts",
    "legacy/old_scripts",
    "legacy/sovereign-financial-cockpit-old",
    "docs"
]

# Create each directory if it doesn't exist
for path in directories:
    os.makedirs(path, exist_ok=True)
