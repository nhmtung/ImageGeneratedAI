name: Feature request
description: Suggest an idea or feature for this offline fashion editor.
labels: [enhancement]
body:
  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: A clear and concise description of what the feature is and why it's needed.
    validations:
      required: true
  - type: select
    id: phase
    attributes:
      label: Which Phase does this belong to?
      description: Refer to docs/plans/master-plan.md to categorize this request.
      options:
        - "Phase 1: Data Crawling & Collection"
        - "Phase 2: Preprocessing & Dataset"
        - "Phase 3: LoRA Fine-tuning"
        - "Phase 4: Inference Pipeline"
        - "Phase 5: Gradio UI"
        - "Phase 6: Review & Optimization"
        - "Phase 7: Packaging & Deploy"
        - "Other / Cross-phase"
    validations:
      required: true
  - type: textarea
    id: constraints_check
    attributes:
      label: Hardware Constraint Alignment
      description: Explain how this feature respects the 2 GB VRAM limit and CPU-offload constraints.
      placeholder: |
        e.g., "This feature performs pre-calculation strictly on the CPU, and the SD pipeline receives input sequentially so VRAM budget is untouched."
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any other context, screenshots, or references here.
    validations:
      required: false
