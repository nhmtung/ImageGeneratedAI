name: Bug report
description: Create a report to help us reproduce and fix bugs under low-resource local hardware constraints.
labels: [bug]
body:
  - type: markdown
    attributes:
      value: |
        Please fill out the information below to help us debug issues. Remember, this project runs on highly constrained local hardware (2 GB VRAM).
  - type: textarea
    id: hardware
    attributes:
      label: Hardware Details
      description: Spec details of the local machine running the application.
      placeholder: |
        GPU: NVIDIA GeForce MX330 (2 GB VRAM)
        RAM: 7.8 GB DDR4
        CPU: Intel Core i5-1035G1
        OS: Windows 11 Home
    validations:
      required: true
  - type: input
    id: vram
    attributes:
      label: VRAM Consumption
      description: Peak VRAM consumed when the issue occurred (if known).
      placeholder: e.g., 1810 MiB, or "Crash due to CUDA OOM"
    validations:
      required: false
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Detailed steps to reproduce the behavior.
      placeholder: |
        1. Run `python app.py`
        2. Upload an image of size 1024x1024
        3. Brush mask over the dress area
        4. Click Generate
    validations:
      required: true
  - type: textarea
    id: behavior
    attributes:
      label: Expected vs Actual Behavior
      description: Explain what you expected to happen and what actually happened.
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs & Tracebacks
      description: Paste any relevant console output or Python exception tracebacks here.
      render: py
    validations:
      required: false
