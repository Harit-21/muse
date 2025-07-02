from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from utils import download_audio_from_youtube
import os
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class YouTubeRequest(BaseModel):
    url: str
    title: str
    artist: str
    cover_url: str

@app.post("/upload_youtube_audio")
def upload_youtube_audio(data: YouTubeRequest):
    try:
        audio_path = download_audio_from_youtube(data.url)

        file_name = os.path.basename(audio_path)

        # Upload to Supabase Storage
        with open(audio_path, 'rb') as f:
            supabase.storage.from_("music").upload(f"tracks/{file_name}", f, {"content-type": "audio/mpeg"})

        audio_url = f"{SUPABASE_URL}/storage/v1/object/public/music/tracks/{file_name}"

        # Add metadata to tracks table
        supabase.table("tracks").insert({
            "title": data.title,
            "artist": data.artist,
            "coverUrl": data.cover_url,
            "audioUrl": audio_url
        }).execute()

        os.remove(audio_path)

        return {"success": True, "url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
