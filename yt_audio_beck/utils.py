import os
import yt_dlp
import uuid

def download_audio_from_youtube(youtube_url: str, output_dir="downloads") -> str:
    os.makedirs(output_dir, exist_ok=True)
    
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(output_dir, unique_id)
    final_path = os.path.join(output_dir, f"{unique_id}.mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,  # no .mp3 extension here
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    if not os.path.exists(final_path):
        raise FileNotFoundError(f"Audio not found at {final_path}")

    return final_path  # ✅ This was the fix
