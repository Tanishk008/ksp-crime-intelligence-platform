import pytest
import sys
import os

# Add to path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.pipeline.nodes.hypothesis import generate_hypotheses

def test_hypothesis_generation():
    state = {"evidence": ["some evidence"]}
    new_state = generate_hypotheses(state)
    
    assert "hypotheses" in new_state
    # Ensure it generates MULTIPLE hypotheses to avoid premature collapse
    assert len(new_state["hypotheses"]) > 1
