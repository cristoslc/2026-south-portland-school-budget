"""Pending state infrastructure for LLM pipeline coordination.

This module implements the pending state pattern for managing LLM-intensive
pipeline stages. The pattern decouples prompt assembly from LLM execution,
enabling parallel, runtime-agnostic work with visibility and error isolation.

Key components:
- generate_sidecars: Create .pending/ directories with sidecar templates
- get_stage: Detect stage (pending-interpret, ready-to-resolve, done, unknown)
- resolve_bundle: Apply completed sidecars to final outputs

See ADR-006 for architecture rationale.
"""

from pathlib import Path
from typing import Any


def generate_sidecars(
    bundle: Path,
    stage: str,
    personas: list[dict[str, Any]],
    template_name: str = "interpret.j2",
) -> None:
    """Generate sidecar templates for each persona.
    
    Creates .pending/PERSONA-NNN/ directories with template files containing
    persona context and task prompts. This is a fast, deterministic operation
    with no LLM calls.
    
    Args:
        bundle: Path to bundle directory
        stage: Pipeline stage (interpret, brief, fold, etc.)
        personas: List of persona dictionaries with 'id', 'name', 'body' keys
        template_name: Template filename (default: interpret.j2)
    
    Performance:
        Must complete in <5 seconds for 15 personas.
    
    Side effects:
        Creates .pending/PERSONA-NNN/ directories if they don't exist.
        Preserves existing templates (no overwrite).
    """
    pending_dir = bundle / ".pending"
    pending_dir.mkdir(exist_ok=True)
    
    for persona in personas:
        persona_id = persona["id"]
        persona_dir = pending_dir / persona_id
        
        # Skip if template already exists (preserve existing work)
        template_path = persona_dir / template_name
        if template_path.exists():
            continue
        
        # Create persona directory
        persona_dir.mkdir(exist_ok=True)
        
        # Generate template content
        template_content = _build_interpret_template(persona)
        template_path.write_text(template_content)


def _build_interpret_template(persona: dict[str, Any]) -> str:
    """Build interpret stage template for a persona.
    
    Args:
        persona: Dictionary with 'id', 'name', 'body' keys
    
    Returns:
        Template content as string
    """
    persona_id = persona["id"]
    persona_name = persona["name"]
    persona_body = persona["body"]
    
    template = f"""# Interpretation Task: {persona_name} ({persona_id})

## Persona Definition

{persona_body}

## Task

Read the meeting evidence through the eyes of {persona_name} and produce a three-layer interpretation.

## Output Format

Your output MUST follow this exact markdown format:

---
schema_version: "1.0"
interpreter_model: "<FILL_IN_MODEL_ID>"
---

# Interpretation: {persona_name} ({persona_id})

## Structured Points

Produce 5-8 structured points in this EXACT format:

#### 1. [Short descriptive title]
- **Fact:** [Concise statement]
- **Source:** [Timestamp or reference]
- **Emotional valence:** [positive/negative/neutral]
- **Threat level:** [1-5]
- **Open question:** [true/false]

## Journey Map

Produce a Mermaid journey diagram.

## Reactions

Write 2-3 paragraphs in {persona_name}'s authentic voice.
"""
    return template


def get_stage(bundle: Path, persona_id: str, template_name: str = "interpret.j2") -> str:
    """Detect stage for a persona's sidecar.
    
    Args:
        bundle: Path to bundle directory
        persona_id: Persona identifier (e.g., PERSONA-001)
        template_name: Template filename (default: interpret.j2)
    
    Returns:
        One of: 'pending-interpret', 'ready-to-resolve', 'done', 'unknown'
    """
    pending_dir = bundle / ".pending"
    persona_dir = pending_dir / persona_id
    
    if not pending_dir.exists():
        return "done"
    
    if not persona_dir.exists():
        return "unknown"
    
    template_path = persona_dir / template_name
    output_name = template_name.replace(".j2", ".md")
    output_path = persona_dir / output_name
    
    if template_path.exists() and not output_path.exists():
        return "pending-interpret"
    
    if output_path.exists() and not template_path.exists():
        return "done"  # Resolved, template removed
    
    if output_path.exists() and template_path.exists():
        return "ready-to-resolve"  # Both exist (edge case)
    
    return "unknown"


def resolve_bundle(
    bundle: Path,
    stage: str = "interpret",
    streaming: bool = False,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Resolve completed sidecars for a bundle.
    
    Applies completed .md outputs to final location, cleans up .pending
    directories for resolved items, and reports status.
    
    Args:
        bundle: Path to bundle directory
        stage: Pipeline stage (interpret, brief, etc.)
        streaming: If True, apply completed items immediately; if False,
                   require full batch
        output_dir: Final output directory (default: bundle parent)
    
    Returns:
        Dict with 'applied', 'pending', 'failed' counts and error details
    
    Performance:
        Must complete in <10 seconds per bundle.
    """
    pending_dir = bundle / ".pending"
    
    if not pending_dir.exists():
        return {"applied": 0, "pending": 0, "failed": 0, "errors": []}
    
    if output_dir is None:
        output_dir = bundle.parent
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    applied = 0
    pending_count = 0
    failed = 0
    errors = []
    
    for persona_dir in pending_dir.iterdir():
        if not persona_dir.is_dir():
            continue
        
        persona_id = persona_dir.name
        
        # Determine stage
        stage_result = get_stage(bundle, persona_id)
        
        if stage_result == "ready-to-resolve":
            # Has both template and output - apply it
            output_file = persona_dir / f"{stage}.md"
            target_file = output_dir / f"{persona_id}.md"
            
            try:
                # Validate output has content
                content = output_file.read_text()
                if not content.strip():
                    raise ValueError(f"Empty output for {persona_id}")
                
                # Apply to final location
                target_file.write_text(content)
                
                # Clean up pending directory
                import shutil
                shutil.rmtree(persona_dir)
                
                applied += 1
                
            except Exception as e:
                failed += 1
                errors.append(f"{persona_id}: {str(e)}")
                
        elif stage_result == "pending-interpret":
            pending_count += 1
            
        elif stage_result == "done" and not streaming:
            # Already resolved, clean up if streaming
            pass
    
    # Clean up empty .pending directory in streaming mode
    if streaming and pending_dir.exists() and not any(pending_dir.iterdir()):
        pending_dir.rmdir()
    
    return {
        "applied": applied,
        "pending": pending_count,
        "failed": failed,
        "errors": errors,
    }