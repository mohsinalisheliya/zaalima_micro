import os
# Add this below your generate_unique_filename function
def create_job_workspace(job_id: str) -> str:
    """Creates a temporary local directory for processing media files."""
    workspace_path = f"/tmp/media_processing/{job_id}"
    # For Windows compatibility, change /tmp/ to a local folder if needed
    if os.name == 'nt':
        workspace_path = f"C:\\tmp\\media_processing\\{job_id}"
    os.makedirs(workspace_path, exist_ok=True)
    return workspace_path

