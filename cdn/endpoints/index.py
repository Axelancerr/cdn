# Future
from __future__ import annotations

# Standard Library
from typing import Any

# Packages
import aiohttp.web
import aiohttp_jinja2
import aiohttp_session

# My stuff
from core.app import CDN


@aiohttp_jinja2.template("index.html")  # type: ignore
async def index(request: aiohttp.web.Request) -> dict[str, Any] | None:

    session = await aiohttp_session.get_session(request)
    app: CDN = request.app  # type: ignore

    user = await app.get_user(session)
    related_guilds = await app.get_related_guilds(session, user_id=getattr(user, "id", None))
    stats = await app.ipc.request("stats")

    return {
        **app.links,
        "user": user.to_dict() if user else None,
        **related_guilds,
        **stats
    }


def setup(app: aiohttp.web.Application) -> None:
    app.add_routes([aiohttp.web.get(r"/", index)])  # type: ignore
