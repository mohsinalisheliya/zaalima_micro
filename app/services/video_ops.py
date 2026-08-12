import subprocess
from app.core.config import settings

def compress_video(input_path: str, output_path: str) -> bool:
    """Compresses a video to 720p using FFmpeg. Uses a command list to safely handle paths across terminal environments."""
    try:
        command = [
            "ffmpeg",
            "-y",  # Overwrite output automatically
            "-i", input_path,
            "-vf", f"scale={settings.VIDEO_MAX_RESOLUTION}",
            "-c:v", settings.VIDEO_CODEC,
            "-crf", "28", # Compression quality (lower is higher quality)
            output_path
        ]
        # Execute the FFmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Error: FFmpeg is not installed globally or not in the system PATH.")
        return False
