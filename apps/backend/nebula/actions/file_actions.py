#file actions
import os
import shutil
import subprocess
import urllib.parse
from pathlib import Path

from nebula.logger import get_logger

logger = get_logger("FileActions")

# ================================
# STANDARD USER FOLDERS
# ================================

USER_HOME = Path.home()

KNOWN_FOLDERS = {
    "desktop": USER_HOME / "Desktop",
    "downloads": USER_HOME / "Downloads",
    "documents": USER_HOME / "Documents",
    "docs": USER_HOME / "Documents",
    "pictures": USER_HOME / "Pictures",
    "photos": USER_HOME / "Pictures",
    "videos": USER_HOME / "Videos",
    "music": USER_HOME / "Music"
}

# ================================
# OPEN FOLDER
# ================================

def open_folder(name: str):
    name = name.lower().strip()
    logger.info(f"Open folder request: {name}")

    if name in KNOWN_FOLDERS:
        path = KNOWN_FOLDERS[name]
        if path.exists():
            os.startfile(path)
            return True, str(path)

    for base in KNOWN_FOLDERS.values():
        for root, dirs, _ in os.walk(base):
            for d in dirs:
                if name in d.lower():
                    full_path = Path(root) / d
                    os.startfile(full_path)
                    return True, str(full_path)

    logger.warning("Folder not found")
    return False, None


# ================================
# WINDOWS EXPLORER SEARCH (FAST)
# ================================

def explorer_search(query: str):
    """
    Uses Windows indexed search via search-ms protocol.
    Opens File Explorer search directly.
    """
    query = query.strip()
    logger.info(f"Explorer search: {query}")

    try:
        encoded_query = urllib.parse.quote(query)
        search_path = f"explorer \"search-ms:query={encoded_query}&crumb=location:C:\\\""
        subprocess.Popen(search_path, shell=True)
        return True
    except Exception as e:
        logger.error(f"Explorer search failed: {e}")
        return False


# ================================
# OPEN FILE (INDEXED SEARCH + STARTFILE)
# ================================

def open_file(name: str):
    """
    Attempts fast Windows search first.
    If direct open fails, triggers Explorer search.
    """
    name = name.strip()
    logger.info(f"Open file request: {name}")

    # Try normal search in user folders
    for base in KNOWN_FOLDERS.values():
        for root, _, files in os.walk(base):
            for file in files:
                if name.lower() in file.lower():
                    full_path = Path(root) / file
                    os.startfile(full_path)
                    return True, str(full_path)

    # If not found → trigger explorer search
    explorer_search(name)
    return False, None


# ================================
# DELETE FILE (SAFE MOVE TO TRASH)
# ================================

def delete_file(name: str):
    logger.info(f"Delete file request: {name}")

    for base in KNOWN_FOLDERS.values():
        for root, _, files in os.walk(base):
            for file in files:
                if name.lower() in file.lower():
                    full_path = Path(root) / file
                    trash = USER_HOME / "Desktop" / "Nebula_Trash"
                    trash.mkdir(exist_ok=True)
                    shutil.move(full_path, trash / file)
                    return True, str(full_path)

    return False, None


# ================================
# DELETE FOLDER (SAFE MOVE TO TRASH)
# ================================

def delete_folder(name: str):
    logger.info(f"Delete folder request: {name}")

    for base in KNOWN_FOLDERS.values():
        for root, dirs, _ in os.walk(base):
            for d in dirs:
                if name.lower() in d.lower():
                    full_path = Path(root) / d
                    trash = USER_HOME / "Desktop" / "Nebula_Trash"
                    trash.mkdir(exist_ok=True)
                    shutil.move(full_path, trash / d)
                    return True, str(full_path)

    return False, None
