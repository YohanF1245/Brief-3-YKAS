import os
import requests

# ID du jeu de données sur data.gouv.fr
DATASET_ID = "operations-coordonnees-par-les-cross"
API_URL = f"https://www.data.gouv.fr/api/1/datasets/{DATASET_ID}/"

# Dossiers de destination
RAW_DIR = "data/raw"
REF_DIR = "references"

# Liste des fichiers cibles
TARGET_FILES = {
    "operations.csv": RAW_DIR,
    "flotteurs.csv": RAW_DIR,
    "resultats_humain.csv": RAW_DIR,
    "Script SQL création tables": REF_DIR
}

def download_file(url, folder, filename):
    """Télécharge un fichier depuis une URL vers un dossier local."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(folder, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"[OK] Telecharge : {filename} -> {folder}")
    else:
        print(f"[ERREUR] Echec telechargement : {filename} (Status {response.status_code})")

def main():
    # Création des dossiers
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(REF_DIR, exist_ok=True)

    print(f"Recuperation des metadonnees pour : {DATASET_ID}...")
    
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("[ERREUR] Impossible d'acceder a l'API data.gouv.fr")
        return

    data = response.json()
    resources = data.get('resources', [])

    found_count = 0
    for resource in resources:
        title = resource.get('title')
        
        target_folder = None
        target_name = None

        if title in TARGET_FILES:
            target_folder = TARGET_FILES[title]
            target_name = title
        elif "Script SQL" in title:
            target_folder = REF_DIR
            target_name = "schema_officiel.sql"

        if target_folder:
            print(f"Telechargement de '{title}'...")
            download_file(resource.get('url'), target_folder, target_name)
            found_count += 1

    print(f"\nTermine. {found_count} fichiers recuperes.")

if __name__ == "__main__":
    main()