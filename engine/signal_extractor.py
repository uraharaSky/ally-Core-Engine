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


class SignalExtractor:

    def __init__(self):
        self.patterns = SIGNAL_PATTERNS

    def extract_signals(self, text: str):

        cleaned_text = preprocess_text(text)

        text_tokens = set(cleaned_text.split())

        detected_signals = []

        for signal, phrases in self.patterns.items():

            for phrase in phrases:

                normalized_phrase = preprocess_text(phrase)

                # Exact phrase match
                if normalized_phrase in cleaned_text:
                    detected_signals.append(signal)
                    break

                # Token overlap match
                phrase_tokens = normalized_phrase.split()

                matched_tokens = sum(
                    1 for token in phrase_tokens
                    if token in text_tokens
                )

                overlap_ratio = matched_tokens / len(phrase_tokens)

                if overlap_ratio >= 0.5:
                    detected_signals.append(signal)
                    break

        return list(set(detected_signals))