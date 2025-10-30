import pytest
from types import SimpleNamespace
from verobrix_core import VeroBrixSystem

@pytest.fixture
def system():
    """Provides a VeroBrixSystem instance for testing."""
    return VeroBrixSystem()

def test_generate_recommendations_high_urgency(system):
    """
    Tests that high urgency situations generate immediate action recommendations.
    """
    situation = {'urgency': {'level': 'high'}, 'type': 'general', 'jurisdiction': {'primary': 'unknown'}}
    legal_summary = {'risk_level': 'LOW', 'tone_summary': 'neutral'}
    remedy = {}
    
    recommendations = system._generate_recommendations(situation, legal_summary, remedy)
    
    assert 'URGENT: Time-sensitive situation detected' in recommendations['immediate_actions']

def test_generate_recommendations_high_risk(system):
    """
    Tests that high risk situations generate immediate action recommendations.
    """
    situation = {'urgency': {'level': 'low'}, 'type': 'general', 'jurisdiction': {'primary': 'unknown'}}
    legal_summary = {'risk_level': 'HIGH', 'tone_summary': 'neutral'}
    remedy = {}

    recommendations = system._generate_recommendations(situation, legal_summary, remedy)

    assert 'HIGH RISK: Seek immediate legal counsel' in recommendations['immediate_actions']
    assert 'Situation contains high-risk legal elements' in recommendations['warnings']

def test_generate_recommendations_servile_sovereignty(system):
    """
    Tests that 'Servile' sovereignty metrics generate warnings and improvement suggestions.
    """
    situation = {'urgency': {'level': 'low'}, 'type': 'general', 'jurisdiction': {'primary': 'unknown'}}
    legal_summary = {'risk_level': 'LOW', 'tone_summary': 'neutral'}
    remedy = {}
    # Mock sovereignty metrics object
    sovereignty_metrics = SimpleNamespace(
        sovereignty_level="Servile",
        overall_score=0.2,
        improvement_suggestions=["Use more assertive language.", "State rights clearly."]
    )

    recommendations = system._generate_recommendations(situation, legal_summary, remedy, sovereignty_metrics)

    assert 'SOVEREIGNTY WARNING: Language contains servile patterns' in recommendations['warnings']
    assert 'CRITICAL: Review language for servile patterns and replace with sovereign alternatives' in recommendations['immediate_actions']
    assert "Use more assertive language." in recommendations['sovereignty_improvements']
