from signal_extractor import SignalExtractor

extractor = SignalExtractor()

sample_text = """
I spiral into late night thoughts, and overthink about various situations. Although, i lock in and get my job done.
"""

signals = extractor.extract_signals(sample_text)

print(signals)