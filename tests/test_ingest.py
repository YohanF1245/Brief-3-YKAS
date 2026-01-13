import pytest
import tempfile
import requests
from unittest.mock import patch, MagicMock
from pathlib import Path

# On importe la bonne fonction depuis le fichier src/ingest.py
from src.ingest import download_file

class TestIngest:
    """Test cases for the ingest module."""

    @patch('src.ingest.requests.get')
    def test_download_file_success(self, mock_get):
        """Teste le téléchargement réussi d'un fichier unique."""
        # 1. Préparer la fausse réponse (Mock)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content = MagicMock(return_value=[b"data1", b"data2"])
        mock_get.return_value = mock_response

        # 2. Utiliser un dossier temporaire
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            filename = "test.csv"
            
            # Appel de la fonction à tester
            result = download_file("http://fake.url", tmp_path, filename)

            # 3. Vérifications
            assert result == tmp_path / filename
            assert result.exists()
            assert result.read_bytes() == b"data1data2"
            assert mock_get.call_count == 1

    @patch('src.ingest.requests.get')
    def test_download_file_failure(self, mock_get):
        """Teste la gestion d'une erreur (ex: 404)."""
        # On simule une erreur HTTP
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Appel de la fonction
            result = download_file("http://fake.url/missing", tmp_path, "missing.csv")

            # La fonction doit retourner None et ne pas planter
            assert result is None
            assert len(list(tmp_path.iterdir())) == 0  # Dossier vide