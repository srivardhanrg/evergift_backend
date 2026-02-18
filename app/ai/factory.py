"""
Model Factory - Creates pipeline instances for story generation.

Provides pipelines:
- PhotorealisticPipeline (photorealistic style)
- CartoonTwoStagePipeline (two-stage scene + face swap approach)

Note: Cartoon3DPipeline has been deprecated in favor of CartoonTwoStagePipeline
which provides better identity preservation via face-swap technology.
"""

from app.ai.pipelines.photorealistic_pipeline import PhotorealisticPipeline
from app.ai.pipelines.cartoon_twostage_pipeline import CartoonTwoStagePipeline


class ModelFactory:
    """Factory for creating AI pipeline instances."""

    @classmethod
    def create_photorealistic_pipeline(cls) -> "PhotorealisticPipeline":
        """Create the photorealistic pipeline."""
        return PhotorealisticPipeline()

    @classmethod
    def create_cartoon_pipeline(cls, use_twostage: bool = None) -> "CartoonTwoStagePipeline":
        """
        Create cartoon pipeline.

        Args:
            use_twostage: Ignored (kept for API compatibility). Always uses two-stage.

        Returns:
            CartoonTwoStagePipeline instance
        """
        # Always use two-stage pipeline (Cartoon3DPipeline deprecated)
        return CartoonTwoStagePipeline()


# Convenience function
def get_photorealistic_pipeline():
    """Get photorealistic pipeline instance."""
    return ModelFactory.create_photorealistic_pipeline()


def get_cartoon_pipeline(use_twostage: bool = None):
    """
    Get cartoon pipeline instance.

    Args:
        use_twostage: Ignored (kept for API compatibility). Always uses two-stage.

    Returns:
        CartoonTwoStagePipeline instance
    """
    return ModelFactory.create_cartoon_pipeline(use_twostage)


def get_pipeline_for_style(style: str, use_twostage_cartoon: bool = None):
    """
    Get appropriate pipeline based on art style.

    Args:
        style: Either 'photorealistic' or 'cartoon_3d'
        use_twostage_cartoon: Ignored (kept for API compatibility).

    Returns:
        Pipeline instance (PhotorealisticPipeline or CartoonTwoStagePipeline)
    """
    if style == "cartoon_3d":
        return get_cartoon_pipeline(use_twostage_cartoon)
    else:
        # Default to photorealistic
        return get_photorealistic_pipeline()
