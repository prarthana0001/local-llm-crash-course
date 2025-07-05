import re
from collections import defaultdict


class CoverageTracker:
    def __init__(self):
        # Structure: {feature_name: {"positive": bool, "negative": bool, "edge": bool}}
        self.coverage = defaultdict(lambda: {
            "positive": False,
            "negative": False,
            "edge": False
        })

    def parse_input(self, user_input: str):
        """
        Extracts feature name and test type from user input using simple heuristics.
        """
        feature = self.extract_feature(user_input)
        test_type = self.extract_test_type(user_input)
        return feature, test_type

    def extract_feature(self, user_input: str):
        """
        Naive feature name extraction: looks for terms after 'for' or 'of'.
        """
        match = re.search(r"(?:for|of)\s+([a-zA-Z_ ]+)", user_input, re.IGNORECASE)
        feature = match.group(1).strip().lower() if match else "unknown_feature"
        return feature.replace(" ", "_")

    def extract_test_type(self, user_input: str):
        """
        Categorizes test type based on common keywords.
        """
        lowered = user_input.lower()
        if any(word in lowered for word in ["valid", "happy path", "positive"]):
            return "positive"
        elif any(word in lowered for word in ["invalid", "error", "negative", "fail", "duplicate"]):
            return "negative"
        elif any(word in lowered for word in ["edge", "boundary", "limit", "corner"]):
            return "edge"
        else:
            return "positive"  # Default guess if unknown

    def update_coverage(self, user_input: str):
        """
        Updates the internal coverage state based on the parsed feature and test type.
        """
        feature, test_type = self.parse_input(user_input)
        self.coverage[feature][test_type] = True
        return feature, self.coverage[feature]

    def get_coverage_state(self):
        return dict(self.coverage)

    def get_missing_categories(self, feature):
        """
        Returns test types not yet covered for the given feature.
        """
        if feature not in self.coverage:
            return ["positive", "negative", "edge"]
        return [cat for cat, covered in self.coverage[feature].items() if not covered]