"""
AI Pipelines.

Two pipelines available:
- PhotorealisticPipeline: For photorealistic style (photorealistic_pipeline.py)
- CartoonTwoStagePipeline: Two-stage approach (cartoon_twostage_pipeline.py)
  - Stage 1: Scene generation with NanoBanana (strong prompt adherence)
  - Stage 2: Face swap with Segmind (perfect identity preservation)

Note: Cartoon3DPipeline (cartoon3d_pipeline.py) is deprecated and no longer used.

Access pipelines via factory:
  - get_photorealistic_pipeline() - returns PhotorealisticPipeline
  - get_cartoon_pipeline() - returns CartoonTwoStagePipeline
  - get_pipeline_for_style(style) - auto-selects based on style parameter
"""
