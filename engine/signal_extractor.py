from signal_dictionary import SIGNAL_PATTERNS
from preprocess import preprocess_text

#
# class SignalExtractor:
#
#     def __init__(self):
#         self.patterns = SIGNAL_PATTERNS
#
#     def extract_signals(self, text: str):
#
#         cleaned_text = preprocess_text(text)
#
#         detected_signals = []
#
#         for signal, phrases in self.patterns.items():
#
#             for phrase in phrases:
#
#                 normalized_phrase = preprocess_text(phrase)
#
#                 if normalized_phrase in cleaned_text:
#                     detected_signals.append(signal)
#                     break
#
#         return list(set(detected_signals))

NEGATION_WORDS = [
    "not",
    "dont",
    "don't",
    "never",
    "no longer",
    "stopped"
]


class SignalExtractor:

    def __init__(self):
        self.patterns = SIGNAL_PATTERNS

    def has_negation(self, text, phrase):

        phrase_index = text.find(phrase)

        if phrase_index == -1:
            return False

        window_start = max(0, phrase_index - 30)

        context_window = text[window_start:phrase_index]

        for neg_word in NEGATION_WORDS:
            if neg_word in context_window:
                return True

        return False

    def extract_signals(self, text: str):

        cleaned_text = preprocess_text(text)

        text_tokens = set(cleaned_text.split())

        detected_signals = {}

        for signal, phrases in self.patterns.items():

            matched_phrases = []
            confidence = 0

            for phrase in phrases:

                normalized_phrase = preprocess_text(phrase)

                if normalized_phrase in cleaned_text:

                    if self.has_negation(cleaned_text, normalized_phrase):
                        continue

                    matched_phrases.append(phrase)
                    confidence += 1
                    continue

                phrase_tokens = normalized_phrase.split()

                matched_tokens = sum(
                    1 for token in phrase_tokens
                    if token in text_tokens
                )

                overlap_ratio = matched_tokens / len(phrase_tokens)

                if overlap_ratio >= 0.5:

                    matched_phrases.append(phrase)
                    confidence += overlap_ratio

            if matched_phrases:

                detected_signals[signal] = {
                    "confidence": round(
                        min(confidence / len(phrases), 1.0),
                        2
                    ),
                    "matched_phrases": list(set(matched_phrases))
                }

        return detected_signals