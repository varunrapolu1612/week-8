from collections import defaultdict
import re
import random

class MarkovText(object):

    def __init__(self, corpus):
        self.corpus = corpus
        # Tokenize the corpus into a list of words, using regex to split on spaces, keeping punctuation attached to words.
        # Note: If you wanted cleaner tokens, you'd use re.split(r'\s+', corpus.lower()) 
        # and remove punctuation here, but we'll stick to the simpler tokenization for now.
        self.tokens = re.findall(r'\S+', self.corpus)
        # Build the dictionary immediately upon initialization
        self.term_dict = self.get_term_dict()

    # --- Exercise 1: Build the Transition Dictionary ---
    def get_term_dict(self):
        """
        Builds the transition dictionary. 
        Key: current word. Value: list of all next words.
        Duplicates are included to correctly represent transition probabilities.
        """
        term_dict = defaultdict(list)
        tokens = self.tokens

        # Loop up to the second-to-last token
        for i in range(len(tokens) - 1):
            current_word = tokens[i]
            next_word = tokens[i+1]

            # Append the next word. The frequency in this list defines the probability.
            term_dict[current_word].append(next_word)

        # The term_dict is stored as an instance variable and returned as a standard dict
        return dict(term_dict)

    # --- Exercise 2: Create a Text Generator ---
    def generate(self, seed_term=None, term_count=15):
        """
        Generates text of a given length using the Markov property 
        (random sampling from the list of followers).
        """
        
        # 1. Handle seed_term selection and validation
        if seed_term:
            if seed_term not in self.term_dict:
                # The term must exist as a key (meaning it has at least one follower)
                raise ValueError(f"Seed term '{seed_term}' is not in the corpus or only appears as the last word.")
            current_word = seed_term
        else:
            # If no seed is provided, select a random starting word from the dictionary keys
            current_word = random.choice(list(self.term_dict.keys()))

        # 2. Initialize output
        generated_text = [current_word]

        # 3. Iteratively generate the rest of the text
        for _ in range(term_count - 1):
            
            # 4. Edge Case Handling: Check if the current word has followers
            if current_word not in self.term_dict:
                # Chain stopped because the word only appeared at the end of the corpus
                generated_text.append("[...chain stopped]")
                break
            
            # 5. Random Selection: Sample from the list of followers
            possible_next_words = self.term_dict[current_word]
            next_word = random.choice(possible_next_words)

            generated_text.append(next_word)
            current_word = next_word

        # 6. Format Output
        return " ".join(generated_text)
