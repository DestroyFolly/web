import pytest
from unittest.mock import MagicMock
from Trainer.service import TrainerService



@pytest.fixture
def trainer_service():
    repo = MagicMock()
    service = TrainerService(repo)
    return service, repo