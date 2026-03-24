"""
Application settings loaded from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator
from functools import lru_cache
from typing_extensions import Self


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # App Configuration
    app_env: str = "development"
    app_debug: bool = False
    app_secret_key: str

    # Database (Supabase)
    supabase_url: str
    supabase_key: str
    database_url: str

    # Storage (Cloudflare R2)
    r2_account_id: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket_name: str = "magictales-storage"
    r2_public_url: str
    r2_endpoint_url: str

    # AI Services
    fal_api_key: str
    segmind_api_key: str = ""  # For Segmind FaceSwap Comic (cartoon pipeline)

    # AI Model Configuration
    realistic_model: str = "photorealistic"  # Primary model for photorealistic generation

    # Cartoon Pipeline Configuration (DEPRECATED)
    # Cartoon3D pipeline has been deprecated. CartoonTwoStagePipeline is always used.
    # This setting is kept for backward compatibility but is no longer read.
    use_twostage_cartoon_pipeline: bool = True  # Deprecated - always True now

    # Legacy model configurations (kept for backward compatibility)
    fallback_base_model: str = "flux_schnell"
    fallback_realistic_model: str = "photorealistic"  # Fallback uses same photorealistic pipeline

    # Testing Configuration
    testing_mode_enabled: bool = False  # Toggle for development vs production (default False for safety)
    testing_mode_pages: int = 5        # Generate only 5 pages in testing mode
    production_pages: int = 10         # Full 10 pages for production

    # Photorealistic Pipeline Settings
    vlm_model: str = "fal-ai/llava-next"      # Vision Language Model for face analysis
    page_aspect_ratio: str = "1:1"            # Square aspect ratio for all pages
    jpeg_quality: float = 0.95                # JPEG quality for PDF generation

    # Parallel Generation Settings
    parallel_batch_size: int = 3  # Number of pages to generate simultaneously (2-3 recommended)

    # Model Settings
    default_seed: int = 42
    guidance_scale: float = 7.5
    num_inference_steps: int = 30

    # Feature Flags
    enable_model_fallback: bool = True
    enable_model_logging: bool = True

    # Shopify (optional in development, required in production)
    shopify_shop_domain: str = ""
    shopify_webhook_secret: str = ""
    shopify_api_secret: str = ""  # For App Proxy HMAC verification
    shopify_product_variant_id: str = ""       # Digital PDF product variant
    shopify_physical_variant_id: str = ""      # Physical book product variant (DEPRECATED - use softcover/hardcover)
    shopify_softcover_variant_id: str = ""     # Softcover physical book variant (saddle stitch)
    shopify_hardcover_variant_id: str = ""     # Hardcover physical book variant (perfect bound)

    # Lulu Print API
    lulu_client_key: str = ""
    lulu_client_secret: str = ""
    lulu_api_base: str = "https://api.sandbox.lulu.com"
    lulu_auth_url: str = "https://api.sandbox.lulu.com/auth/realms/glasstree/protocol/openid-connect/token"
    lulu_pod_package_id: str = "0850X0850FCPRESS080CW444GXX"  # DEPRECATED - use softcover/hardcover
    lulu_pod_package_id_softcover: str = "0850X0850BCSADSTDLW444GXX"  # 8.5x8.5" B&W saddle stitch (24 pages)
    lulu_pod_package_id_hardcover: str = "0850X0850FCPERFGLOSSGW"     # 8.5x8.5" color perfect bound (24 pages)
    lulu_webhook_secret: str = ""  # Set to your lulu_client_secret value — Lulu uses it to sign webhooks

    # Rate Limiting
    rate_limit_previews_per_day: int = 3
    rate_limit_uploads_per_hour: int = 10

    # Email (Resend)
    resend_api_key: str = ""  # Get from resend.com
    from_email: str = "StoryGift <noreply@storygift.in>"
    
    # Frontend URL for email links (hash routing)
    # Format: base URL without trailing slash, preview path uses /#/preview/{id}
    frontend_url: str = "https://storygift-2061.myshopify.com/pages/create-story"

    # StoryGift Generation Settings
    default_theme: str = "storygift_magic_castle"  # Primary StoryGift theme
    default_style: str = "photorealistic"          # Only style supported now
    image_quality: str = "high"
    pdf_page_size: str = "10x10"                   # Square format (inches) for StoryGift layout

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @model_validator(mode="after")
    def validate_production_settings(self) -> Self:
        """Validate that required settings are present in production mode."""
        if self.app_env == "production":
            errors = []
            
            if not self.shopify_webhook_secret:
                errors.append(
                    "SHOPIFY_WEBHOOK_SECRET is required in production. "
                    "Get it from Shopify Admin > Settings > Notifications > Webhooks"
                )
            
            if not self.shopify_api_secret:
                errors.append(
                    "SHOPIFY_API_SECRET is required in production. "
                    "Get it from Shopify Partners > Your App > API credentials"
                )
            
            if not self.shopify_shop_domain:
                errors.append(
                    "SHOPIFY_SHOP_DOMAIN is required in production. "
                    "Example: your-store.myshopify.com"
                )
            
            if errors:
                raise ValueError(
                    "Production configuration errors:\n" + 
                    "\n".join(f"  - {e}" for e in errors)
                )
        
        return self


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
