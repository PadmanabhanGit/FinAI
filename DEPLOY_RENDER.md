Render Docker deployment (recommended)

1. Create a Render Web Service (https://dashboard.render.com/new)
   - Environment: Docker
   - Dockerfile: repository root (Dockerfile created)
   - Branch: main

2. Add Environment Variables (Settings → Environment):
   - GEMINI_API_KEY = your_key_here

3. Deploy and wait ~1-3 minutes.

Notes:
- This image uses Python 3.11 and installs system libs required by packages like Pillow and lxml.
- You can also deploy locally with Docker:

```bash
# build
docker build -t finai:latest .
# run
docker run -p 8501:8501 -e GEMINI_API_KEY="your_key" finai:latest
```
