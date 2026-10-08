import asyncio
import logging
import os

from aiohttp import web

from .config import Config
from .plugins.authentication import handle_oauth_callback
from .utubebot import UtubeBot

log = logging.getLogger(__name__)


async def oauth_health(request: web.Request) -> web.Response:
    return web.Response(text="Utubeitbot OAuth endpoint is running.")


async def oauth_callback(request: web.Request) -> web.Response:
    error = request.query.get("error")
    if error:
        return web.Response(
            text=f"Authorization was cancelled or denied: {error}",
            status=400,
        )

    code = request.query.get("code")
    state = request.query.get("state")

    if not code or not state:
        return web.Response(
            text="Missing OAuth code/state. Please run /login again.",
            status=400,
        )

    try:
        await handle_oauth_callback(
            request.app["bot"],
            code,
            state,
        )
    except Exception:
        log.error("OAuth callback failed", exc_info=True)
        return web.Response(
            text="YouTube authorization failed. Please run /login again.",
            status=400,
        )

    return web.Response(
        text=(
            "<html><body>"
            "<h2>YouTube authorization successful.</h2>"
            "<p>You can close this page and return to Telegram.</p>"
            "</body></html>"
        ),
        content_type="text/html",
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG if Config.DEBUG else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.getLogger("pyrogram").setLevel(
        logging.DEBUG if Config.DEBUG else logging.WARNING
    )

    bot = UtubeBot()

    web_app = web.Application()
    web_app["bot"] = bot
    web_app.router.add_get("/", oauth_health)
    web_app.router.add_get("/oauth2callback", oauth_callback)

    runner = web.AppRunner(web_app)
    await runner.setup()

    port = int(os.environ.get("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    log.info("OAuth web server listening on port %s", port)

    try:
        await bot.start()
        await asyncio.Event().wait()
    finally:
        await bot.stop()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
