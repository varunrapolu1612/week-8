from collections import defaultdict


class MarkovText(object):

    def __init__(self, corpus):
        self.corpus = corpus
        self.term_dict = None  # you'll need to build this

    def get_term_dict(self):

        # your code here ...
        ''' Build a term dictionary of Markov States where each key is token from the corpus , 
        and each value is a list of tokens directly follows the key in the corpus.
         The resulting term dictionary is stored in the self.term_dict.
         Returns: None.'''
        
        term_dict = defaultdict(list)

        for i in range(len(self.corpus) - 1):
            current_token = self.corpus[i]
            next_token = self.corpus[i + 1]
            term_dict[current_token].append(next_token)

        self.term_dict = dict(term_dict)

        return None
    



    def generate(self, seed_term=None, term_count=15):

        ''' Generate sentences (sequence of terms) based on the Markov chain model.
        If seed_term is provided, the generated text starts with that term.
        If seed_term is None, a random term from the term dictionary is chosen as the starting term.
        The generated text will contain term_count terms.
        Parameters:
        seed_term (str, optional): The starting token for generation.
        term_count (int): Number of tokens to generate.
        Returns: A string representing the generated text.'''
        
        # your code here ...
        if self.term_dict is None:
            raise ValueError("Term dictionary not initialized. Call get_term_dict() first.")

        if seed_term:
            if seed_term not in self.term_dict:
                raise ValueError(f"Seed term '{seed_term}' not found in corpus.")
            current_term = seed_term
        else:
            current_term = np.random.choice(list(self.term_dict.keys()))

        output = [current_term]

        for _ in range(term_count - 1):
            followers = self.term_dict.get(current_term)
            if not followers:
                break  # No known followers; end early
            next_term = np.random.choice(followers)
            output.append(next_term)
            current_term = next_term

        return ' '.join(output)

   
