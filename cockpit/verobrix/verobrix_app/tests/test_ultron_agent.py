import pytest
from agents.ULTRON.ultron_agent import UltronAgent

def test_ultron_strategy_for_fee_demand(monkeypatch):
    """
    Tests that the Ultron agent generates a specific strategy for a 'fee_demand' situation
    when its search function finds a relevant keyword.
    """
    # 1. Create a mock search function that returns a predictable result
    def mock_search_corpus(directory, keywords):
        if 'tender' in keywords:
            return ["Found 'tender' in U.C.C.txt, line 123: ...tender of payment..."]
        return []

    # 2. Replace the real search_corpus function with our mock version for this test
    monkeypatch.setattr('agents.ULTRON.ultron_agent.search_corpus', mock_search_corpus)

    # 3. Initialize the agent and run the analysis
    agent = UltronAgent()
    context = {'situation': {'type': 'fee_demand'}}
    result = agent.analyze("some input text", context=context)

    # 4. Assert that the correct recommendation was generated
    recommendations = result['strategic_recommendations']
    assert len(recommendations) == 1
    rec = recommendations[0]
    assert rec['strategy'] == "Leverage the concept of 'Tender'"
    assert rec['legal_basis'] == "As referenced in U.C.C.txt"
    assert "This involves formally offering full payment" in rec['guidance']

def test_ultron_general_strategy_when_no_finding(monkeypatch):
    """
    Tests that the Ultron agent returns a general strategy when no specific keywords are found.
    """
    # 1. Mock the search function to return no results
    def mock_search_corpus(directory, keywords):
        return []

    # 2. Apply the mock function
    monkeypatch.setattr('agents.ULTRON.ultron_agent.search_corpus', mock_search_corpus)

    # 3. Initialize and run analysis for a known situation
    agent = UltronAgent()
    context = {'situation': {'type': 'fee_demand'}}
    result = agent.analyze("some input text", context=context)

    # 4. Assert that the general recommendation was returned
    recommendations = result['strategic_recommendations']
    assert len(recommendations) == 1
    rec = recommendations[0]
    assert rec['strategy'] == "General Defensive Posture"
    assert rec['legal_basis'] == "Common Law"
