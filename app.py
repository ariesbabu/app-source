import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
GIT_SHA     = os.getenv("GIT_SHA", "unknown")
BUILD_TIME  = os.getenv("BUILD_TIME", "unknown")
ENV_NAME    = os.getenv("ENV_NAME", "unknown")

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>App Update Visualiser - Updated</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0;
           display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
    .card {{ background: #1e293b; border-radius: 12px; padding: 2rem; min-width: 360px;
             box-shadow: 0 8px 32px rgba(0,0,0,0.4); transition: background 0.5s; }}
    .card.flash {{ background: #166534; }}
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 999px;
              font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }}
    .badge-dev {{ background: #166534; color: #bbf7d0; }}
    .badge-staging {{ background: #92400e; color: #fde68a; }}
    .badge-unknown {{ background: #374151; color: #9ca3af; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    td {{ padding: 6px 0; }}
    td:first-child {{ color: #94a3b8; width: 110px; }}
    .ts {{ margin-top: 1rem; font-size: 0.75rem; color: #64748b; }}
  </style>
</head>
<body>
  <div class="card" id="card">
    <span class="badge badge-{ENV_NAME}" id="env-badge">{ENV_NAME}</span>
    <table>
      <tr><td>Version</td><td id="version">{APP_VERSION}</td></tr>
      <tr><td>Git SHA</td><td id="sha">{GIT_SHA}</td></tr>
      <tr><td>Built</td><td id="built">{BUILD_TIME}</td></tr>
    </table>
    <div class="ts">Last checked: <span id="ts">—</span></div>
  </div>
  <script>
    let lastSha = "{GIT_SHA}";
    async function poll() {{
      try {{
        const r = await fetch('/api/version');
        const d = await r.json();
        document.getElementById('version').textContent = d.version;
        document.getElementById('sha').textContent = d.git_sha;
        document.getElementById('built').textContent = d.build_time;
        document.getElementById('ts').textContent = new Date().toLocaleTimeString();
        const badge = document.getElementById('env-badge');
        badge.textContent = d.environment;
        badge.className = 'badge badge-' + d.environment;
        if (d.git_sha !== lastSha) {{
          lastSha = d.git_sha;
          const card = document.getElementById('card');
          card.classList.add('flash');
          setTimeout(() => card.classList.remove('flash'), 1500);
        }}
      }} catch(e) {{}}
    }}
    poll();
    setInterval(poll, 3000);
  </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML

@app.get("/api/version")
def version():
    return {"version": APP_VERSION, "git_sha": GIT_SHA,
            "build_time": BUILD_TIME, "environment": ENV_NAME}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)# build trigger Thu Apr 16 00:14:27 UTC 2026
# trigger Thu Apr 16 00:32:50 UTC 2026
