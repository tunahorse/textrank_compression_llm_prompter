# Work in Progress: Solving the Problem of Small LLMs Being Slow and Limited by Small Context Windows

This is a "dumb" tool prioritizing working offline and on small hardware (e.g., Raspberry Pi).

## The Script Combines Text Summarization and Prompt Engineering:

### 1. Text Summarization:
- Uses the TextRank algorithm for extractive summarization.
- Splits input text into sentences, treating each as a node in a graph.
- Calculates similarity scores between sentences.
- Applies TextRank to rank sentences by importance.
- Selects top-ranking sentences and arranges them in original order for coherence.
- Outputs the summary to a separate file.

### 2. Prompt Formatting: (ROUGH WIP)
- Applies prompt engineering principles to the summarized text.
- Removes politeness phrases, uses affirmative language.
- Randomly incorporates task-oriented phrases and thinking prompts.
- Adds delimiters and output primers.
- Writes formatted prompts to a separate file.

### TLDR:
This tool aims to compress large texts into summaries and well-formatted prompts, making them more suitable for small context window LLMs.

Also, if you want a C version of compression, I'm better with Python so I made this but will eventually be 100% C.

[GitHub Repository](https://github.com/tunahorse/TextRank_local_text_summarizer)

## Usage

To run the script:

```
python textrank_prompt_formatter.py <input_file> <compression_percentage>
```

Example:
```
python textrank_prompt_formatter.py input.txt 20
```

See text files for examples of compressing a PG essay and a compressed essay being passed to a prompt format (buggy).

Format:
```
script/text_file/percentage_to_compress_down_to
```

I am currently obsessed with solving this problem if you want to chat shoot me an email at fabiananguiano@gmail DOT com 
