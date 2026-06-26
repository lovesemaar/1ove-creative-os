from __future__ import annotations

from pathlib import Path

from app.agent_runner import run_agents
from app.evaluator import evaluate_output
from app.memory_store import init_memory, log_content_history, log_run_memory
from app.output_writer import write_outputs
from app.privacy_gate import apply_privacy_gate
from app.retriever import retrieve_memory
from app.review_runner import run_reviews
from app.types import CreativeBrief, WorkflowResult


def run_workflow(
    idea: str,
    platform: str,
    duration: str,
    privacy_mode: str = "public_safe",
    use_memory: bool = False,
    output_path: Path | None = None,
    model_backend: str | None = None,
) -> Path:
    init_memory()

    # Privacy gate always runs before retrieval and model call.
    safe_idea, sensitive_hits = apply_privacy_gate(idea, privacy_mode)

    memory_context = retrieve_memory(safe_idea, privacy_mode=privacy_mode) if use_memory else []

    brief = CreativeBrief(
        idea=safe_idea,
        platform=platform,
        duration=duration,
        privacy_mode=privacy_mode,
        use_memory=use_memory,
        memory_context=memory_context,
    )

    agent_outputs = run_agents(brief, model_backend=model_backend)
    final_content = agent_outputs[-1].content

    if sensitive_hits:
        final_content.setdefault("review_notes", []).append(
            f"Privacy gate transformed or flagged sensitive terms: {sensitive_hits}"
        )

    review_outputs = run_reviews(final_content)
    evaluation = evaluate_output(final_content, review_outputs)

    result = WorkflowResult(
        brief=brief,
        privacy_hits=sensitive_hits,
        memory_context=memory_context,
        agent_outputs=agent_outputs,
        review_outputs=review_outputs,
        evaluation=evaluation,
        final_content=final_content,
    )

    output_file = write_outputs(result, output_path)

    log_run_memory(
        title=f"Run: {final_content.get('title', 'Untitled')}",
        text=f"Idea: {safe_idea}\nDecision: {evaluation.decision}\nOutput: {output_file.name}",
        tags=["run", "stage13", evaluation.decision.lower()],
    )
    log_content_history(
        title=final_content.get("title", "Untitled content"),
        text=f"Hook: {final_content.get('hook')}\nEnding: {final_content.get('ending_line')}",
        tags=["content", "video", "stage13"],
    )

    return output_file
