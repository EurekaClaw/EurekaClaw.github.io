"""
Reverse proxy: serves English docs (port 8002) and Chinese docs (port 8001)
on a single port 8000.

  http://127.0.0.1:8000/      -> English (sphinx-autobuild on :8002)
  http://127.0.0.1:8000/zh/   -> Chinese (sphinx-autobuild on :8001)

Supports both HTTP and WebSocket (live-reload).
"""

import asyncio
import httpx
import websockets
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket

EN_ORIGIN = "http://127.0.0.1:8002"
ZH_ORIGIN = "http://127.0.0.1:8001"


def _backend(path: str) -> tuple[str, str]:
    """Return (origin, rewritten_path) for the given request path."""
    if path.startswith("/zh"):
        stripped = path[3:] or "/"
        return ZH_ORIGIN, stripped
    return EN_ORIGIN, path


async def proxy_http(request: Request) -> Response:
    path = request.url.path
    if request.url.query:
        path = f"{path}?{request.url.query}"
    origin, rewritten = _backend(path)

    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient(base_url=origin, follow_redirects=True) as client:
        backend_url = rewritten
        resp = await client.request(
            method=request.method,
            url=backend_url,
            headers=headers,
            content=await request.body(),
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        media_type=resp.headers.get("content-type"),
    )


async def proxy_ws(websocket: WebSocket) -> None:
    path = websocket.url.path
    if websocket.url.query:
        path = f"{path}?{websocket.url.query}"
    origin, rewritten = _backend(path)
    backend_ws_url = origin.replace("http://", "ws://") + rewritten

    await websocket.accept()
    try:
        async with websockets.connect(backend_ws_url) as backend:
            async def client_to_backend():
                async for msg in websocket.iter_text():
                    await backend.send(msg)

            async def backend_to_client():
                async for msg in backend:
                    await websocket.send_text(msg)

            await asyncio.gather(client_to_backend(), backend_to_client())
    except Exception:
        pass
    finally:
        await websocket.close()


app = Starlette(
    routes=[
        WebSocketRoute("/{path:path}", proxy_ws),
        Route("/{path:path}", proxy_http, methods=["GET", "POST", "HEAD", "OPTIONS"]),
        Route("/", proxy_http, methods=["GET", "POST", "HEAD", "OPTIONS"]),
    ]
)

if __name__ == "__main__":
    import uvicorn
    print("Proxy running on http://127.0.0.1:8000")
    print("  English -> http://127.0.0.1:8000/")
    print("  Chinese -> http://127.0.0.1:8000/zh/")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
