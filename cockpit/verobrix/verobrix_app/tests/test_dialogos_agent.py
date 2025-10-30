import pytest
from agents.DIALOGOS.dialogos_agent import DialogosAgent

def test_dialogos_prompt_for_consent():
    """
    Tests that the Dialogos agent generates a specific prompt when the word 'consent' is found.
    """
    agent = DialogosAgent()
    input_text = "We do not consent to this agreement."
    result = agent.analyze(input_text)

    prompts = result['authorship_prompts']
    assert len(prompts) > 0
    
    consent_prompt_found = False
    for prompt in prompts:
        if prompt['concept'] == 'Consent':
            consent_prompt_found = True
            assert "True consent must be knowing, willing, and voluntary" in prompt['guiding_question']
            break
    
    assert consent_prompt_found, "Prompt for 'Consent' was not generated."

def test_dialogos_default_prompt():
    """
    Tests that the Dialogos agent returns a default authorship prompt when no keywords are found.
    """
    agent = DialogosAgent()
    input_text = "This is a simple statement."
    result = agent.analyze(input_text)

    prompts = result['authorship_prompts']
    assert len(prompts) == 1
    prompt = prompts[0]
    assert prompt['concept'] == 'Authorship'
    assert "Every word you write creates your standing" in prompt['guiding_question']
