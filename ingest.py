import requests
import os
from pathlib import Path
from typing import List, Optional
import pandas as pd

def download_multiple_csvs(urls: List[str], output_dir: str = "data") -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    downloaded_files = []
    
    for i, url in enumerate(urls, 1):
        filename = url.split('/')[-1]
        if not filename.endswith('.csv'):
            filename = f"data_{i}.csv"
        
        output_path = os.path.join(output_dir, filename)
        
        if download_csv(url, output_path):
            downloaded_files.append(output_path)
    
    return downloaded_files


def main():
    csv_urls = [
        "https://www.data.gouv.fr/api/1/datasets/r/8eb7f207-1ce5-460c-b941-5f1761a79c46",
        "https://www.data.gouv.fr/api/1/datasets/r/5d3c65fb-c861-4b22-b8aa-1eab58e3d9db",
        "https://www.data.gouv.fr/api/1/datasets/r/ae0e17e4-7117-45f0-80c4-b11b38f31c5c",
        "https://www.data.gouv.fr/api/1/datasets/r/fae6bc13-fe4c-4838-b281-b16628b7babe",
    ]
    
    downloaded_files = download_multiple_csvs(csv_urls, output_dir="data")
    



if __name__ == "__main__":
    dfs = main()
    

