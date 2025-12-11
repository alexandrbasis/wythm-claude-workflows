#!/usr/bin/env python3
"""
Twitter/X Tweet Analyzer

Analyzes tweets for character count, engagement potential, and provides optimization suggestions.
"""

import re
import sys
from typing import Dict, List


class TweetAnalyzer:
    """Analyzes tweets for various metrics and provides feedback."""

    # Character limits
    CHAR_LIMIT_FREE = 280
    CHAR_LIMIT_PREMIUM = 25000
    OPTIMAL_RANGE = (71, 100)  # 17% higher engagement

    def __init__(self, tweet_text: str, is_premium: bool = False):
        """
        Initialize the tweet analyzer.

        Args:
            tweet_text: The tweet content to analyze
            is_premium: Whether the account has Premium/Blue subscription
        """
        self.text = tweet_text
        self.is_premium = is_premium
        self.char_count = len(tweet_text)
        self.char_limit = (
            self.CHAR_LIMIT_PREMIUM if is_premium else self.CHAR_LIMIT_FREE
        )

    def analyze(self) -> Dict[str, any]:
        """
        Perform comprehensive tweet analysis.

        Returns:
            Dictionary with analysis results
        """
        return {
            "character_count": self.char_count,
            "character_limit": self.char_limit,
            "remaining_chars": self.char_limit - self.char_count,
            "is_within_limit": self.char_count <= self.char_limit,
            "is_optimal_length": self.OPTIMAL_RANGE[0]
            <= self.char_count
            <= self.OPTIMAL_RANGE[1],
            "optimal_range": self.OPTIMAL_RANGE,
            "word_count": len(self.text.split()),
            "line_count": len(self.text.split("\n")),
            "hashtag_count": len(self._find_hashtags()),
            "hashtags": self._find_hashtags(),
            "mention_count": len(self._find_mentions()),
            "mentions": self._find_mentions(),
            "url_count": len(self._find_urls()),
            "urls": self._find_urls(),
            "has_question": "?" in self.text,
            "has_emoji": self._has_emoji(),
            "suggestions": self._generate_suggestions(),
        }

    def _find_hashtags(self) -> List[str]:
        """Extract hashtags from tweet."""
        return re.findall(r"#\w+", self.text)

    def _find_mentions(self) -> List[str]:
        """Extract mentions from tweet."""
        return re.findall(r"@\w+", self.text)

    def _find_urls(self) -> List[str]:
        """Extract URLs from tweet."""
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        return re.findall(url_pattern, self.text)

    def _has_emoji(self) -> bool:
        """Check if tweet contains emojis."""
        emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags
            "\U00002702-\U000027b0"
            "\U000024c2-\U0001f251"
            "]+",
            flags=re.UNICODE,
        )
        return bool(emoji_pattern.search(self.text))

    def _generate_suggestions(self) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = []

        # Character count suggestions
        if self.char_count > self.char_limit:
            suggestions.append(
                f"❌ Tweet exceeds {self.char_limit} character limit by "
                f"{self.char_count - self.char_limit} characters"
            )
        elif self.char_count < self.OPTIMAL_RANGE[0]:
            suggestions.append(
                f"💡 Tweet is short ({self.char_count} chars). Consider expanding to "
                f"{self.OPTIMAL_RANGE[0]}-{self.OPTIMAL_RANGE[1]} chars for 17% higher engagement"
            )
        elif self.char_count > self.OPTIMAL_RANGE[1] and not self.is_premium:
            suggestions.append(
                f"💡 Tweet is longer than optimal ({self.char_count} chars). "
                f"Consider shortening to {self.OPTIMAL_RANGE[0]}-{self.OPTIMAL_RANGE[1]} chars "
                f"or converting to a thread"
            )
        else:
            suggestions.append(
                "✅ Tweet length is in the optimal range for engagement!"
            )

        # Hashtag suggestions
        hashtag_count = len(self._find_hashtags())
        if hashtag_count > 3:
            suggestions.append(
                f"⚠️ Using {hashtag_count} hashtags. Recommended: 2-3 max for clean appearance"
            )
        elif hashtag_count == 0:
            suggestions.append(
                "💡 Consider adding 1-2 relevant hashtags for discoverability"
            )

        # Engagement suggestions
        if not self._has_question_mark() and not self._has_call_to_action():
            suggestions.append(
                "💡 Consider adding a question or call-to-action to boost engagement"
            )

        # URL suggestions
        url_count = len(self._find_urls())
        if url_count > 1:
            suggestions.append(
                f"⚠️ Multiple URLs detected ({url_count}). Consider using a single link for clarity"
            )

        return suggestions

    def _has_question_mark(self) -> bool:
        """Check if tweet contains a question."""
        return "?" in self.text

    def _has_call_to_action(self) -> bool:
        """Check if tweet contains common CTAs."""
        ctas = [
            "bookmark",
            "save",
            "retweet",
            "rt",
            "share",
            "follow",
            "click",
            "check out",
            "learn more",
            "read",
            "watch",
            "join",
            "subscribe",
            "sign up",
            "download",
            "try",
            "comment",
            "reply",
            "tag",
            "dm me",
        ]
        text_lower = self.text.lower()
        return any(cta in text_lower for cta in ctas)

    def print_analysis(self):
        """Print formatted analysis results."""
        analysis = self.analyze()

        print("\n" + "=" * 60)
        print("TWEET ANALYSIS")
        print("=" * 60)

        # Character metrics
        print(f"\n📊 Character Metrics:")
        print(
            f"   Characters: {analysis['character_count']}/{analysis['character_limit']}"
        )
        print(f"   Remaining: {analysis['remaining_chars']}")
        print(
            f"   Optimal range: {analysis['optimal_range'][0]}-{analysis['optimal_range'][1]} "
            f"(current: {analysis['character_count']})"
        )

        if analysis["is_optimal_length"]:
            print(f"   ✅ In optimal range for engagement!")

        # Content metrics
        print(f"\n📝 Content Metrics:")
        print(f"   Words: {analysis['word_count']}")
        print(f"   Lines: {analysis['line_count']}")
        print(f"   Hashtags: {analysis['hashtag_count']} {analysis['hashtags']}")
        print(f"   Mentions: {analysis['mention_count']} {analysis['mentions']}")
        print(f"   URLs: {analysis['url_count']}")

        # Engagement indicators
        print(f"\n🎯 Engagement Indicators:")
        print(f"   Has question: {'✅ Yes' if analysis['has_question'] else '❌ No'}")
        print(f"   Has emoji: {'✅ Yes' if analysis['has_emoji'] else '❌ No'}")

        # Suggestions
        print(f"\n💡 Suggestions:")
        for suggestion in analysis["suggestions"]:
            print(f"   {suggestion}")

        print("\n" + "=" * 60 + "\n")


def main():
    """Main function to run the tweet analyzer from command line."""
    if len(sys.argv) < 2:
        print("Usage: python tweet_analyzer.py 'Your tweet text here' [--premium]")
        print("\nExample:")
        print(
            "  python tweet_analyzer.py 'This is my tweet about #AI and #MachineLearning'"
        )
        print("  python tweet_analyzer.py 'Premium account tweet' --premium")
        sys.exit(1)

    tweet_text = sys.argv[1]
    is_premium = "--premium" in sys.argv

    analyzer = TweetAnalyzer(tweet_text, is_premium)
    analyzer.print_analysis()


if __name__ == "__main__":
    main()
