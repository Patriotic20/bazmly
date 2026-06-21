from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.exceptions import AppException


app = FastAPI(title="Bazmly")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


from app.modules.routers import router
app.include_router(router)


@app.get("/test", response_class=HTMLResponse, include_in_schema=False)
async def test_page() -> HTMLResponse:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bazmly — Auth Test</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 60px 16px; }
    .card { background: #fff; border-radius: 12px; padding: 40px; width: 100%; max-width: 540px; box-shadow: 0 2px 16px rgba(0,0,0,.08); }
    h1 { font-size: 1.5rem; margin-bottom: 8px; }
    p  { color: #666; margin-bottom: 28px; font-size: .95rem; }
    .btn-google {
      display: flex; align-items: center; gap: 12px;
      background: #fff; border: 1px solid #dadce0; border-radius: 8px;
      padding: 12px 20px; font-size: 1rem; cursor: pointer; width: 100%;
      transition: box-shadow .2s;
    }
    .btn-google:hover { box-shadow: 0 2px 8px rgba(0,0,0,.12); }
    .btn-google svg { flex-shrink: 0; }
    #token-section { margin-top: 28px; display: none; }
    #token-section h2 { font-size: 1rem; margin-bottom: 10px; color: #333; }
    #token-box {
      background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 8px;
      padding: 14px; font-family: monospace; font-size: .78rem;
      word-break: break-all; max-height: 120px; overflow-y: auto; color: #1a1a1a;
    }
    .btn-copy {
      margin-top: 10px; padding: 8px 18px; border: none; border-radius: 6px;
      background: #1a73e8; color: #fff; font-size: .9rem; cursor: pointer;
    }
    .btn-copy:hover { background: #1558b0; }
    #copy-msg { margin-left: 10px; font-size: .85rem; color: #1a73e8; opacity: 0; transition: opacity .3s; }
  </style>
</head>
<body>
<div class="card">
  <h1>Bazmly Auth Test</h1>
  <p>Test Google OAuth login and get a JWT token.</p>

  <button class="btn-google" onclick="window.location='/api/v1/auth/google'">
    <svg width="20" height="20" viewBox="0 0 48 48">
      <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
      <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
      <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
    </svg>
    Login with Google
  </button>

  <div id="token-section">
    <h2>Access Token</h2>
    <div id="token-box"></div>
    <button class="btn-copy" onclick="copyToken()">Copy</button>
    <span id="copy-msg">Copied!</span>
  </div>
</div>

<script>
  const hash = window.location.hash;
  if (hash.startsWith('#token=')) {
    const token = decodeURIComponent(hash.slice(7));
    document.getElementById('token-section').style.display = 'block';
    document.getElementById('token-box').textContent = token;
    history.replaceState(null, '', '/test');
  }

  function copyToken() {
    const token = document.getElementById('token-box').textContent;
    navigator.clipboard.writeText(token);
    const msg = document.getElementById('copy-msg');
    msg.style.opacity = '1';
    setTimeout(() => msg.style.opacity = '0', 1500);
  }
</script>
</body>
</html>"""
    return HTMLResponse(html)




