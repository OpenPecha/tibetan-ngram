import struct

def load_vocab(vocab_file):
    """Load the vocabulary from the null-delimited vocab file."""
    with open(vocab_file, 'rb') as f:
        vocab_data = f.read()
    # Split the file by null characters and decode from bytes to strings
    vocab_list = vocab_data.split(b'\x00')
    # Filter out any empty strings caused by consecutive nulls
    vocab_list = [word.decode('utf-8') for word in vocab_list if word]
    return vocab_list

def extract_ngrams_counts(counts_file, order, vocab):
    """Extract n-grams and their counts from the binary counts file."""
    ngrams_by_order = {1: [], 2: [], 3: []}  # Dictionary to store unigrams, bigrams, and trigrams
    
    for current_order in range(1, order + 1):  # Loop for each n-gram order
        record_size = current_order * 4 + 8  # Each n-gram has `current_order` 4-byte ints + 8-byte count

        with open(counts_file, 'rb') as f:
            while True:
                record = f.read(record_size)
                if len(record) < record_size:
                    break  # End of file reached
                
                # Unpack the binary record: `current_order` integers for n-gram, 1 integer for count
                values = struct.unpack("=" + "I" * current_order + "Q", record)
                ngram_indices = values[:current_order]  # First part is the n-gram indices
                count = values[-1]                     # Last part is the count
                
                # Convert indices to the actual words from the vocabulary
                try:
                    ngram_words = [vocab[idx] for idx in ngram_indices]
                except IndexError:
                    continue
                # Store the n-gram and its count based on the order
                ngrams_by_order[current_order].append((ngram_words, count))
    
    return ngrams_by_order

def save_ngrams_to_single_file(ngrams_by_order, output_file):
    """Save all n-grams (unigrams, bigrams, trigrams) into a single text file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for order, ngrams in ngrams_by_order.items():
            for ngram, count in ngrams:
                ngram_str = ''.join(ngram)
                f.write(f"{ngram_str} {count}\n")
    print(f"All n-grams saved to {output_file}")

# File paths
vocab_file = "lm.vocab"
counts_file = "lm.counts"
output_file = "1-3gram_counts.txt"  # Single output file for all n-grams
max_order = 3  # Maximum n-gram order (up to trigrams)

# Load the vocabulary
vocab = load_vocab(vocab_file)

# Extract n-grams and their counts up to order=3 (unigrams, bigrams, trigrams)
ngrams_by_order = extract_ngrams_counts(counts_file, max_order, vocab)

# Save the n-grams and counts to a single text file
save_ngrams_to_single_file(ngrams_by_order, output_file)

