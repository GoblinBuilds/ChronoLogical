import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import game_logic
from unittest.mock import patch

def simulate_input(mocked_inputs, function_to_test, *args, **kwargs):
    with patch('builtins.input', side_effect=mocked_inputs):
        return function_to_test(*args, **kwargs)

def test_get_user_input_chooses_index():
    combined_timeline = [{"date": 1800}]
    result = simulate_input(["0"], game_logic.get_user_input, combined_timeline)
    assert result == "0"

def test_get_user_input_lock_command():
    combined_timeline = [{"date": 1800}]
    result = simulate_input(["lock"], game_logic.get_user_input, combined_timeline)
    assert result == "lock"

def test_get_user_input_quit_command():
    combined_timeline = [{"date": 1800}]
    result = simulate_input(["quit"], game_logic.get_user_input, combined_timeline)
    assert result == "quit"
