import multiprocessing
import re
import sys
from pathlib import Path

import config

tsek = "་"
shed = "།"

def tokenize_syl(text):
    segments = text.split(shed)
    syls = []
    for segment in segments:
        segment = segment.strip()
        if not segment or segment == shed:
            continue
        syls.extend(re.findall(r'[^་]+་?', segment))
    return syls

# Function to process lines in parallel
def process_file_lines(lines):
    processed_lines = []
    for line in lines:
        syls = tokenize_syl(line)
        processed_lines.append(" ".join(syls))
    return processed_lines

def get_syls_sentences_parallel():
    # Gather all text files from the data path
    files = list(config.DATA_PATH.glob("*.txt"))[:10000]

    # List to store all lines from all files
    all_lines = []

    # Read lines from each file and collect them
    for fn in files:
        print(fn)
        lines = fn.read_text().splitlines()
        all_lines.extend(lines)

    # Determine the number of processes to use
    num_workers = multiprocessing.cpu_count()

    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_workers) as pool:
        # Split lines into roughly equal chunks for each process
        chunk_size = len(all_lines) // num_workers
        if chunk_size == 0:
            chunk_size = 1  # In case there are fewer lines than workers

        # Distribute the work and process in parallel
        result_chunks = pool.map(process_file_lines, [all_lines[i:i + chunk_size] for i in range(0, len(all_lines), chunk_size)])

    # Flatten the results into a single list of processed lines
    flat_results = [line for sublist in result_chunks for line in sublist]
    return flat_results

def detokenize_syls(syls):
    result = ""
    for syl in syls:
        if not syl.endswith("་"):
            syl += " "
        result += syl
    return result

def create_dataset(name="dataset.txt"):
    dataset_fn = config.DATA_PATH / name

    # Collect all syllable sentences using parallel processing
    syls_sentences = get_syls_sentences_parallel()

    # Write the dataset to the output file
    with open(str(dataset_fn), 'w') as f:
        for syls in syls_sentences:
            f.write(syls)
            f.write("\n")

    print("Dataset created at", dataset_fn)

if __name__ == "__main__":
    create_dataset()