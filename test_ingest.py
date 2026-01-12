import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from ingest import download_multiple_csvs


class TestDownloadMultipleCsvs:
    """Test cases for download_multiple_csvs function."""
    
    @patch('ingest.requests.get')
    def test_download_multiple_csvs_success(self, mock_get):
        """Test downloading multiple CSV files successfully."""
        mock_response = MagicMock()
        mock_response.content = b"col1,col2\nval1,val2"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        urls = [
            "https://example.com/data1.csv",
            "https://example.com/data2.csv",
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            downloaded = download_multiple_csvs(urls, output_dir=tmpdir)
            
            assert len(downloaded) == 2
            assert mock_get.call_count == 2
            assert all(os.path.exists(f) for f in downloaded)
    
    @patch('ingest.requests.get')
    def test_download_multiple_csvs_partial_failure(self, mock_get):
        """Test downloading multiple CSV files with some failures."""
        mock_response = MagicMock()
        mock_response.content = b"col1,col2\nval1,val2"
        mock_response.raise_for_status = MagicMock()
        
        def side_effect(*args, **kwargs):
            if mock_get.call_count == 0 or mock_get.call_count == 2:
                return mock_response
            else:
                raise Exception("Network error")
        
        mock_get.side_effect = side_effect
        
        urls = [
            "https://example.com/data1.csv",
            "https://example.com/data2.csv",
            "https://example.com/data3.csv",
            "https://example.com/data4.csv",
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            downloaded = download_multiple_csvs(urls, output_dir=tmpdir)
            
            assert len(downloaded) == 2
            assert mock_get.call_count == 4
    
    @patch('ingest.requests.get')
    def test_download_multiple_csvs_generates_filename(self, mock_get):
        """Test that non-CSV URLs get generated filenames."""
        mock_response = MagicMock()
        mock_response.content = b"col1,col2\nval1,val2"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        urls = [
            "https://example.com/data1",
            "https://example.com/data2.json",
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            downloaded = download_multiple_csvs(urls, output_dir=tmpdir)
            
            assert len(downloaded) == 2
            assert "data_1.csv" in downloaded[0]
            assert "data_2.csv" in downloaded[1]

