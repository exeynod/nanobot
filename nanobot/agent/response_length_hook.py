"""Opt-in hook that caps final response length as a hard backstop."""

from __future__ import annotations

from nanobot.agent.hook import AgentHook, AgentHookContext

# Boundary characters preferred (in order) when choosing a truncation point.
_SENTENCE_BOUNDARY = (". ", "! ", "? ", ".\n", "!\n", "?\n", "\n")
_TRUNCATION_MARKER = " […]"


class ResponseLengthHook(AgentHook):
    """Truncate over-long final responses at a word/sentence boundary.

    ``finalize_content`` returns the content unchanged when it is at or under
    ``max_chars``.  When it is longer, it trims to the last sentence (or, failing
    that, word) boundary at or before ``max_chars`` and appends a short marker.
    The result — marker included — never exceeds ``max_chars``.  ``None``/empty
    pass through untouched; the hook never raises.
    """

    __slots__ = ("_max_chars",)

    def __init__(self, max_chars: int, reraise: bool = False) -> None:
        super().__init__(reraise=reraise)
        self._max_chars = int(max_chars)

    def finalize_content(self, context: AgentHookContext, content: str | None) -> str | None:
        try:
            if not content or self._max_chars <= 0:
                return content
            if len(content) <= self._max_chars:
                return content
            return self._truncate(content)
        except Exception:
            # A length governor must never break the turn — fail open.
            return content

    def _truncate(self, content: str) -> str:
        marker = _TRUNCATION_MARKER if len(_TRUNCATION_MARKER) < self._max_chars else ""
        budget = self._max_chars - len(marker)
        if budget <= 0:
            # Marker alone would overflow; just hard-cut to the limit.
            return content[: self._max_chars]

        window = content[:budget]

        # Prefer a sentence boundary, then a word boundary, within the window.
        cut = -1
        for boundary in _SENTENCE_BOUNDARY:
            idx = window.rfind(boundary)
            if idx != -1:
                # Keep the boundary punctuation but drop trailing whitespace.
                cut = max(cut, idx + len(boundary.rstrip()))
        if cut <= 0:
            idx = window.rfind(" ")
            if idx > 0:
                cut = idx
        if cut <= 0:
            cut = budget

        return window[:cut].rstrip() + marker
