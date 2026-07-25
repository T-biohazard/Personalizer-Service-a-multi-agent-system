import httpx

from app.voice_io import record_audio, transcribe


def main() -> None:
    record_audio(5, "input.wav")
    query = transcribe("input.wav")
    print("You said:", query)
    resp = httpx.post("http://localhost:8000/ask", params={"user_id": "u1", "query": query}, timeout=30.0)
    print(resp.json())


if __name__ == "__main__":
    main()
