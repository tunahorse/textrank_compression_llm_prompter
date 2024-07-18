import re
import math
import argparse
from typing import List, Tuple

class Sentence:
    def __init__(self, content: str, score: float, index: int):
        self.content = content
        self.score = score
        self.index = index

def tokenize_sentences(text: str) -> List[Sentence]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [Sentence(sent.strip(), 1.0, i) for i, sent in enumerate(sentences)]

def tokenize_words(sentence: str) -> List[str]:
    words = re.findall(r'\b\w+\b', sentence.lower())
    return [word for word in words if not is_stop_word(word)]

def is_stop_word(word: str) -> bool:
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "from", "up", "about", "into", "over", "after"}
    return word in stop_words

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

def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filename: str, sentences: List[Sentence]):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Summary:\n\n")
        for sentence in sentences:
            file.write(f"{sentence.content}\n")

def main():
    parser = argparse.ArgumentParser(description="Text summarization using TextRank algorithm")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to the output summary file")
    parser.add_argument("summary_percentage", type=float, help="Percentage of sentences to include in the summary")
    args = parser.parse_args()

    text = read_file(args.input_file)
    sentences = tokenize_sentences(text)
    num_sentences = math.ceil(len(sentences) * args.summary_percentage / 100)

    text_rank(sentences)
    summary = summarize(sentences, num_sentences)
    write_file(args.output_file, summary)

    print(f"Summary written to {args.output_file}")
    print(f"Total sentences in summary: {len(summary)}")

if __name__ == "__main__":
    main()