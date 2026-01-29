"""
Model Factory - Creates pipeline instances for story generation.

Provides two pipelines:
- PhotorealisticPipeline (photorealistic style)
- Cartoon3DPipeline (stylized/animated portrait style)
"""

from app.ai.pipelines.photorealistic_pipeline import PhotorealisticPipeline


class ModelFactory:
    """Factory for creating AI pipeline instances."""

    @classmethod
    def create_photorealistic_pipeline(cls) -> "PhotorealisticPipeline":
        """Create the photorealistic pipeline."""
        return PhotorealisticPipeline()


# Convenience function
def get_photorealistic_pipeline():
    """Get photorealistic pipeline instance."""
    return ModelFactory.create_photorealistic_pipeline()


def get_pipeline_for_style(style: str):
    """
    Get appropriate pipeline based on art style.
    
    Args:
        style: Either 'photorealistic' or 'cartoon_3d'
        
    Returns:
        Pipeline instance (PhotorealisticPipeline or Cartoon3DPipeline)
    """
    if style == "cartoon_3d":
        from app.ai.pipelines.cartoon3d_pipeline import Cartoon3DPipeline
        return Cartoon3DPipeline()
    else:
        # Default to photorealistic
        return get_photorealistic_pipeline()
