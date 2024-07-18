import re
import math
import random
from typing import List, Tuple
import sys
from collections import defaultdict
import time
import os

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

def calculate_similarity(words1: set, words2: set) -> float:
    common_words = words1.intersection(words2)
    return len(common_words) / (math.log(len(words1) + 1) + math.log(len(words2) + 1))

def text_rank(sentences: List[Sentence], iterations: int = 30, damping: float = 0.85, threshold: float = 0.0001):
    sentence_words = [set(tokenize_words(sentence.content)) for sentence in sentences]
    similarity_matrix = defaultdict(dict)
    
    print("[TextRank] Calculating sentence similarities...")
    for i in range(len(sentences)):
        for j in range(i+1, len(sentences)):
            similarity = calculate_similarity(sentence_words[i], sentence_words[j])
            if similarity > 0:
                similarity_matrix[i][j] = similarity
                similarity_matrix[j][i] = similarity

    print(f"[TextRank] Starting algorithm (max {iterations} iterations)...")
    for iteration in range(iterations):
        prev_scores = [sentence.score for sentence in sentences]
        for i, sentence in enumerate(sentences):
            score = 1 - damping
            for j in similarity_matrix[i]:
                score += damping * sentences[j].score * similarity_matrix[i][j]
            sentence.score = score
        
        diff = sum(abs(s.score - prev) for s, prev in zip(sentences, prev_scores))
        print(f"[TextRank] Iteration {iteration + 1}, score diff: {diff:.6f}")
        if diff < threshold:
            print(f"[TextRank] Converged after {iteration + 1} iterations.")
            break
    else:
        print(f"[TextRank] Reached maximum iterations ({iterations}).")

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

def process_file(input_file: str, summary_file: str, prompt_file: str, summary_percentage: float):
    try:
        print(f"[Input] Reading file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        print("[Tokenization] Splitting text into sentences...")
        sentences = tokenize_sentences(text)
        num_sentences = max(1, math.ceil(len(sentences) * summary_percentage / 100))
        print(f"[Info] Total sentences: {len(sentences)}, Target summary sentences: {num_sentences}")

        print(f"[TextRank] Processing {len(sentences)} sentences...")
        start_time = time.time()
        text_rank(sentences)
        end_time = time.time()
        print(f"[TextRank] Completed in {end_time - start_time:.2f} seconds")

        print("[Summary] Generating summary...")
        summary = summarize(sentences, num_sentences)

        print(f"[Output] Writing summary to: {summary_file}")
        with open(summary_file, 'w', encoding='utf-8') as file:
            file.write("TextRank Summary:\n\n")
            file.write("\n".join(sent.content for sent in summary))

        print("[Formatting] Applying prompt engineering principles...")
        formatted_summary = [format_prompt(sent.content) for sent in summary]

        print(f"[Output] Writing formatted prompts to: {prompt_file}")
        with open(prompt_file, 'w', encoding='utf-8') as file:
            file.write("Compressed and Formatted Prompts:\n\n")
            file.write("\n\n".join(formatted_summary))

        print(f"[Complete] Summary sentences: {len(summary)}")
        print(f"[Complete] Original text size: {len(text)} characters")
        print(f"[Complete] Summary size: {sum(len(s.content) for s in summary)} characters")
        print(f"[Complete] Compression ratio: {sum(len(s.content) for s in summary) / len(text):.2%}")

    except FileNotFoundError as e:
        print(f"[Error] File not found: {e.filename}")
        sys.exit(1)
    except PermissionError as e:
        print(f"[Error] Permission denied when accessing file: {e.filename}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"[Error] Unable to decode {input_file}. Please ensure it's a valid text file.")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <summary_percentage>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        summary_percentage = float(sys.argv[2])
        if not 0 < summary_percentage <= 100:
            raise ValueError("Summary percentage must be between 0 and 100")
    except ValueError as e:
        print(f"[Error] Invalid summary percentage: {str(e)}")
        sys.exit(1)

    # Generate output filenames based on input filename
    base_name = os.path.splitext(input_file)[0]
    summary_file = f"{base_name}_summary.txt"
    prompt_file = f"{base_name}_compressed_prompt.txt"

    process_file(input_file, summary_file, prompt_file, summary_percentage)