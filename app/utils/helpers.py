import os
import time
import shutil
import uuid

def generate_unique_filename(original_filename: str) -> str:
    ext = original_filename.split('.')[-1]
    return f"{uuid.uuid4()}.{ext}"

def create_job_workspace(job_id: str) -> str:
    """Creates a temporary local directory for processing media files."""
    workspace_path = f"/tmp/media_processing/{job_id}"
    
    if os.name == 'nt':
        workspace_path = f"C:\\tmp\\media_processing\\{job_id}"
        
    os.makedirs(workspace_path, exist_ok=True)
    return workspace_path

def clear_local_workspaces(max_age_hours: int = 24) -> int:
    """Deletes temporary job folders older than the specified hours."""
    base_path = "/tmp/media_processing/"
    if os.name == 'nt':
        base_path = "C:\\tmp\\media_processing\\"
        
    if not os.path.exists(base_path):
        return 0
        
    current_time = time.time()
    deleted_count = 0
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            folder_age_seconds = current_time - os.path.getmtime(folder_path)
            if folder_age_seconds > (max_age_hours * 3600):
                try:
                    shutil.rmtree(folder_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {folder_path}: {e}")
                    
    return deleted_count