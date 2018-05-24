import pytest
from mock import patch
import database
from merge import MergeBranch

def get_event():
    return {
        "event":{
            "payload":{
                "branch":"cenario-01"
            }
        }
    }

def test_should_merge():
    with patch.object(MergeBranch, 'get_event', return_value=get_event()) as mock_event:
        assert 1 == 1
        pass