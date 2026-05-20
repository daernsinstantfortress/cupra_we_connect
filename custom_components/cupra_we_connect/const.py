"""Constants for the Cupra We Connect integration."""

DOMAIN = "cupra_we_connect"


def apply_app_market_header(we_connect) -> None:
    """Cupra API headers required since VW backend change (2026-05-20).

    weconnect_cupra's addToken() builds headers from scratch (Authorization only),
    so session.headers are ignored unless we merge them in addToken.
    """
    session = getattr(we_connect, "session", None)
    if session is None:
        return

    base_headers = getattr(session, "headers", None)
    if base_headers is not None:
        base_headers["app-market"] = "android"
        base_headers["app-brand"] = "cupra"
        base_headers["app-version"] = "2.15.0"
        base_headers["origin"] = "app"

    if getattr(session, "_cupra_headers_patched", False):
        return

    original_add_token = session.addToken

    def add_token_with_session_headers(uri, body=None, headers=None, **kwargs):
        merged = dict(base_headers) if base_headers is not None else {}
        if headers:
            merged.update(headers)
        return original_add_token(uri, body=body, headers=merged, **kwargs)

    session.addToken = add_token_with_session_headers
    session._cupra_headers_patched = True
