"""
Abstract base class for review sources.
"""

from abc import ABC, abstractmethod
from typing import List
from app.models import ProductSearchResult, ReviewFetchResponse

class BaseReviewSource(ABC):
    """Contract for searching products and retrieving customer reviews."""

    @abstractmethod
    async def search_products(self, query: str, country: str = "in") -> List[ProductSearchResult]:
        """Search for products/apps matching query string."""
        pass

    @abstractmethod
    async def fetch_reviews(
        self, product_id: str, product_name: str, country: str = "in"
    ) -> ReviewFetchResponse:
        """Fetch customer reviews for a given product."""
        pass
