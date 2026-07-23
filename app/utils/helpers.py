import uuid

def generate_unique_filename(original_name: str) -> str:
    extension = original_name.split('.')[-1]
    unique_id = uuid.uuid4().hex
    return f"{unique_id}.{extension}"
