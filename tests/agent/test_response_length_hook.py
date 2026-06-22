"""Tests for the opt-in ResponseLengthHook output-length governor."""

from __future__ import annotations

from nanobot.agent.hook import AgentHookContext
from nanobot.agent.response_length_hook import ResponseLengthHook


def _ctx() -> AgentHookContext:
    return AgentHookContext(iteration=1, messages=[])


def test_under_limit_passthrough_unchanged() -> None:
    hook = ResponseLengthHook(max_chars=100)
    content = "Short reply that fits."
    assert hook.finalize_content(_ctx(), content) is content


def test_exactly_at_limit_unchanged() -> None:
    hook = ResponseLengthHook(max_chars=10)
    content = "0123456789"
    assert hook.finalize_content(_ctx(), content) == content


def test_over_limit_truncates_within_budget_with_marker() -> None:
    hook = ResponseLengthHook(max_chars=40)
    content = "First sentence. Second sentence. Third sentence goes on and on."
    out = hook.finalize_content(_ctx(), content)
    assert out is not None
    assert len(out) <= 40
    assert out.endswith(" […]")
    # Truncated at the latest sentence boundary that still fits the budget.
    assert out == "First sentence. Second sentence. […]"


def test_over_limit_falls_back_to_word_boundary() -> None:
    hook = ResponseLengthHook(max_chars=20)
    content = "alpha beta gamma delta epsilon zeta"
    out = hook.finalize_content(_ctx(), content)
    assert out is not None
    assert len(out) <= 20
    assert out.endswith(" […]")
    # No mid-word cut: the text before the marker is whole words.
    body = out[: -len(" […]")]
    assert not content[len(body):].startswith(tuple("abcdefghijklmnopqrstuvwxyz")) or content[len(body)] == " "


def test_empty_and_none_safe() -> None:
    hook = ResponseLengthHook(max_chars=10)
    assert hook.finalize_content(_ctx(), "") == ""
    assert hook.finalize_content(_ctx(), None) is None


def test_zero_max_chars_disabled() -> None:
    hook = ResponseLengthHook(max_chars=0)
    content = "x" * 1000
    assert hook.finalize_content(_ctx(), content) is content


def test_no_boundary_hard_cut_respects_limit() -> None:
    hook = ResponseLengthHook(max_chars=12)
    content = "a" * 50  # no spaces/sentence boundaries at all
    out = hook.finalize_content(_ctx(), content)
    assert out is not None
    assert len(out) <= 12
    assert out.endswith(" […]")


def test_never_raises_on_bad_input() -> None:
    hook = ResponseLengthHook(max_chars=5)
    # Marker longer than the whole budget -> hard cut path, still no raise.
    out = hook.finalize_content(_ctx(), "abcdefghij")
    assert out is not None
    assert len(out) <= 5
