Work in progress, trying to solve the problem of small LLM's being slow and small cotext windows. 

This is "dumb" tool and is prioritizing working offline, and on small hardware (thik rpi)

The script combines text summarization and prompt engineering:

1. Text Summarization:
   - Uses the TextRank algorithm for extractive summarization.
   - Splits input text into sentences, treating each as a node in a graph.
   - Calculates similarity scores between sentences.
   - Applies TextRank to rank sentences by importance.
   - Selects top-ranking sentences and arranges them in original order for coherence.
   - Outputs the summary to a separate file.

2. Prompt Formatting: (ROUGH WIP)
   - Applies prompt engineering principles to the summarized text.
   - Removes politeness phrases, uses affirmative language.
   - Randomly incorporates task-oriented phrases and thinking prompts.
   - Adds delimiters and output primers.
   - Writes formatted prompts to a separate file.

TLDR: 

This tool aims to compress large texts into summaries and well-formatted prompts, making them more suitable for small context window LLMs.


Also if you want a C version of compression, im better with python so I made this but will eventually be 100% C 

https://github.com/tunahorse/TextRank_local_text_summarizer
