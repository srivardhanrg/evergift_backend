"""
Concurrency control for AI API calls.

Global semaphore to limit concurrent fal.ai API requests and prevent rate limiting.
"""

import asyncio

# Global semaphore to limit concurrent fal.ai API calls to 3
# This prevents rate limiting and ensures stable generation
FAL_SEMAPHORE = asyncio.Semaphore(3)
