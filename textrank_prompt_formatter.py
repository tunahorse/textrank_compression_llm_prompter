import re
import math
import random
from typing import List, Tuple
import sys

class Sentence:
    def __init__(self, content: str, score: float, index: int):
        self.content = content
        self.score = score
        self.index = index

def tokenize_sentences(text: str) -> List[Sentence]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [Sentence(sent.strip(), 1.0, i) for i, sent in enumerate(sentences)]

def tokenize_words(sentence: str) -> List[str]:
    return re.findall(r'\b\w+\b', sentence.lower())

def calculate_similarity(sentence1: str, sentence2: str) -> float:
    words1 = set(tokenize_words(sentence1))
    words2 = set(tokenize_words(sentence2))
    common_words = words1.intersection(words2)
    return len(common_words) / (math.log(len(words1) + 1) + math.log(len(words2) + 1))

def text_rank(sentences: List[Sentence], iterations: int = 20, damping: float = 0.85):
    for _ in range(iterations):
        for i, sentence in enumerate(sentences):
            score = 1 - damping
            for j, other_sentence in enumerate(sentences):
                if i != j:
                    similarity = calculate_similarity(sentence.content, other_sentence.content)
                    score += damping * similarity * other_sentence.score
            sentence.score = score

def summarize(sentences: List[Sentence], num_sentences: int) -> List[Sentence]:
    ranked_sentences = sorted(sentences, key=lambda s: s.score, reverse=True)
    selected_sentences = sorted(ranked_sentences[:num_sentences], key=lambda s: s.index)
    return selected_sentences

def format_prompt(text: str) -> str:
    # Apply principle 1: Remove politeness
    text = re.sub(r"\b(please|kindly|if you don't mind|thank you|I would like to)\b", "", text, flags=re.IGNORECASE)

    # Apply principle 4: Use affirmative language
    text = text.replace("don't", "do")

    # Apply principle 9: Incorporate "Your task is" and "You MUST"
    if random.choice([True, False]):
        text = f"Your task is to {text} You MUST complete this."

    # Apply principle 12: Add "think step by step"
    if random.choice([True, False]):
        text += " Let's think step by step."

    # Apply principle 17: Use delimiters
    text = f"```{text}```"

    # Apply principle 20: Use output primers
    if random.choice([True, False]):
        text += " Answer:"

    return text

def process_file(input_file: str, output_file: str, summary_percentage: float):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        sentences = tokenize_sentences(text)
        num_sentences = max(1, math.ceil(len(sentences) * summary_percentage / 100))

        text_rank(sentences)
        summary = summarize(sentences, num_sentences)

        formatted_summary = [format_prompt(sent.content) for sent in summary]

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Compressed and Formatted Summary:\n\n")
            file.write("\n\n".join(formatted_summary))

        print(f"Processed summary written to {output_file}")
        print(f"Total sentences in summary: {len(summary)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <output_file> <summary_percentage>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        summary_percentage = float(sys.argv[3])
        if not 0 < summary_percentage <= 100:
            raise ValueError("Summary percentage must be between 0 and 100")
    except ValueError as e:
        print(f"Invalid summary percentage: {str(e)}")
        sys.exit(1)

    process_file(input_file, output_file, summary_percentage)