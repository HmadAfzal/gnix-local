import pytest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock



@pytest.fixture
def temp_config(tmp_path, monkeypatch):
    config_dir  = str(tmp_path / ".gnix")
    config_file = str(tmp_path / ".gnix" / "config.json")

    monkeypatch.setattr("gnix.config.CONFIG_DIR",  config_dir)
    monkeypatch.setattr("gnix.config.CONFIG_FILE", config_file)

    return config_file


class TestLoadSaveConfig:

    def test_load_returns_empty_when_no_file(self, temp_config):
        from gnix.config import load_config
        result = load_config()
        assert result == {}

    def test_save_and_load_model(self, temp_config):
        from gnix.config import save_config, load_config
        save_config({"model": "qwen2.5:0.5b"})
        result = load_config()
        assert result["model"] == "qwen2.5:0.5b"

    def test_save_creates_directory(self, temp_config):
        from gnix.config import save_config, CONFIG_DIR
        save_config({"model": "qwen2.5:0.5b"})
        assert os.path.isdir(CONFIG_DIR)

    def test_save_creates_file(self, temp_config):
        from gnix.config import save_config
        save_config({"model": "qwen2.5:0.5b"})
        assert os.path.exists(temp_config)

    def test_save_overwrites_existing(self, temp_config):
        from gnix.config import save_config, load_config
        save_config({"model": "qwen2.5:0.5b"})
        save_config({"model": "phi3.5:latest"})
        result = load_config()
        assert result["model"] == "phi3.5:latest"

    def test_load_handles_corrupted_file(self, temp_config):
        from gnix.config import load_config, CONFIG_DIR
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(temp_config, "w") as f:
            f.write("this is not valid json {{{{")
        result = load_config()
        assert result == {}

    def test_save_valid_json(self, temp_config):
        from gnix.config import save_config
        save_config({"model": "qwen2.5:0.5b"})
        with open(temp_config, "r") as f:
            data = json.load(f)
        assert data["model"] == "qwen2.5:0.5b"


class TestIsFirstRun:

    def test_first_run_when_no_config(self, temp_config):
        from gnix.config import is_first_run
        assert is_first_run() == True

    def test_not_first_run_when_config_exists(self, temp_config):
        from gnix.config import is_first_run, save_config
        save_config({"model": "qwen2.5:0.5b"})
        assert is_first_run() == False


class TestGetModel:

    def test_returns_empty_when_no_config(self, temp_config):
        from gnix.config import get_model
        assert get_model() == ""

    def test_returns_model_from_config(self, temp_config):
        from gnix.config import get_model, save_config
        save_config({"model": "qwen2.5:0.5b"})
        assert get_model() == "qwen2.5:0.5b"

    def test_returns_updated_model(self, temp_config):
        from gnix.config import get_model, save_config
        save_config({"model": "qwen2.5:0.5b"})
        save_config({"model": "phi3.5:latest"})
        assert get_model() == "phi3.5:latest"



class TestOllamaChecks:

    def test_ollama_installed_true(self):
        from gnix.config import check_ollama_installed
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch("subprocess.run", return_value=mock_result):
            assert check_ollama_installed() == True

    def test_ollama_installed_false(self):
        from gnix.config import check_ollama_installed
        with patch("subprocess.run", side_effect=FileNotFoundError):
            assert check_ollama_installed() == False

    def test_ollama_running_true(self):
        from gnix.config import check_ollama_running
        mock_response = MagicMock()
        with patch("requests.get", return_value=mock_response):
            assert check_ollama_running() == True

    def test_ollama_running_false(self):
        from gnix.config import check_ollama_running
        import requests
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            assert check_ollama_running() == False


class TestGetAvailableModels:

    def test_returns_model_list(self):
        from gnix.config import get_available_models
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "models": [
                {"name": "qwen2.5:0.5b"},
                {"name": "phi3.5:latest"},
            ]
        }
        with patch("requests.get", return_value=mock_response):
            models = get_available_models()
        assert "qwen2.5:0.5b" in models
        assert "phi3.5:latest" in models

    def test_returns_empty_on_connection_error(self):
        from gnix.config import get_available_models
        import requests
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            models = get_available_models()
        assert models == []

    def test_returns_empty_when_no_models(self):
        from gnix.config import get_available_models
        mock_response = MagicMock()
        mock_response.json.return_value = {"models": []}
        with patch("requests.get", return_value=mock_response):
            models = get_available_models()
        assert models == []



class TestValidateModel:
	
    def test_valid_model_found(self):
        from gnix.config import validate_model
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "models": [{"name": "qwen2.5:0.5b"}]
        }
        with patch("requests.get", return_value=mock_response):
            assert validate_model("qwen2.5:0.5b") == True

    def test_invalid_model_not_found(self):
        from gnix.config import validate_model
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "models": [{"name": "qwen2.5:0.5b"}]
        }
        with patch("requests.get", return_value=mock_response):
            assert validate_model("nonexistent-model") == False

    def test_invalid_random_string(self):
        from gnix.config import validate_model
        mock_response = MagicMock()
        mock_response.json.return_value = {"models": []}
        with patch("requests.get", return_value=mock_response):
            assert validate_model("abcxyz123") == False