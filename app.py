import streamlit as st
from apputil import MarkovText
import requests
import re

st.set_page_config(layout="wide")

st.write(
'''
# Week 8: Markov Text Generator

This application uses a Markov Chain to generate new text based on a corpus of inspirational quotes.
''')

# --- 1. Corpus Setup (from exercises.ipynb) ---
@st.cache_data
def load_and_clean_corpus(): 
    """Fetches and cleans the text corpus for the Markov generator."""
    url = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/text/inspiration_quotes.txt'
    content = requests.get(url)
    quotes_raw = content.text
    
    quotes = quotes_raw.replace('\n', ' ')
    quotes = re.split("[“”]", quotes)
    quotes = quotes[1::2]
    
    corpus = ' '.join(quotes)
    corpus = re.sub(r"\s+", " ", corpus)
    corpus = corpus.strip()
    return corpus

corpus = load_and_clean_corpus()

# --- 2. MarkovText Initialization ---
# This initializes the class and runs Exercise 1 implicitly in the constructor
text_gen = MarkovText(corpus)

st.markdown("---")

## Exercise 1: Transition Dictionary (Term Dictionary)

st.header("Exercise 1: Transition Dictionary")
st.markdown(
    """
    The `get_term_dict` method creates the Markov model's transition map.
    The keys are the current words (states), and the values are lists of *all* words
    that follow them in the corpus. The frequency of words in these lists determines the
    transition probability.
    """
)

# Display Transition Dictionary Proof
st.code(f"Total unique words (states): {len(text_gen.term_dict)}")

# Display a few sample entries for validation
sample_keys = list(text_gen.term_dict.keys())
sample_display_keys = sample_keys[:5]

sample_dict = {}
for k in sample_display_keys:
    followers = text_gen.term_dict[k]
    # Show up to 5 followers plus '...' if the list is longer
    sample_dict[k] = followers[:5] + (['...'] if len(followers) > 5 else [])

st.markdown("Sample from the generated `term_dict`:")
st.code(sample_dict)
st.caption("The lists of follower words (values) contain duplicates to correctly represent transition probabilities for random sampling.")

st.markdown("---")

## Exercise 2: Markov Text Generation

st.header("Exercise 2: Markov Text Generator")
st.markdown(
    """
    The `generate` method uses the transition dictionary from Exercise 1.
    For each step, it randomly selects the next word from the list of followers
    for the current word, creating a new, coherent, but often nonsensical quote.
    """
)

col1, col2 = st.columns([1, 2])

with col1:
    term_count = st.slider("Words to Generate:", 
                           min_value=10, 
                           max_value=50, 
                           value=15, 
                           step=5)

with col2:
    seed_term = st.text_input("Optional Starting Word (e.g., 'Life', 'Happiness'):", value="")

if st.button("Generate Text"):
    try:
        # Run Exercise 2 implementation
        if seed_term.strip():
            generated_text = text_gen.generate(seed_term=seed_term.strip(), term_count=term_count)
        else:
            generated_text = text_gen.generate(term_count=term_count)
            
        st.subheader("Generated Quote:")
        st.info(generated_text)
        
    except ValueError as e:
        st.error(str(e))
        
