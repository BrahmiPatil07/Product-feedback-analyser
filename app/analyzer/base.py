from abc import ABC, abstractmethod
from typing import List
from app.models import AnalysisResponse

class BaseFeedbackAnalyzer(ABC):
    """Abstract interface for feedback analysis engines."""

    @abstractmethod
    def analyze_reviews(self, reviews: List[str]) -> AnalysisResponse:
        """
        Analyze a batch of review strings and return a structured AnalysisResponse.
        
        :param reviews: List of raw customer review texts.
        :return: AnalysisResponse containing sentiments, theme stats, pain points, recommendations, and product brief.
        """
        pass
