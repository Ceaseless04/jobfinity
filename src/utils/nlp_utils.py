# src/utils/nlp_utils.py
import spacy
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NLPUtils:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load('en_core_web_md')
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text using TF-IDF."""
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Remove stopwords and punctuation
        processed_text = ' '.join([token.text for token in doc if not token.is_stop and not token.is_punct])
        
        # Create a corpus with just this text
        corpus = [processed_text]
        
        # Fit and transform the text
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
        
        # Get feature names
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        
        # Get TF-IDF scores
        tfidf_scores = zip(feature_names, tfidf_matrix.toarray()[0])
        
        # Sort by score
        sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
        
        # Return top N keywords
        return [item[0] for item in sorted_scores[:top_n]]
    
    def calculate_similarity(self, text1, text2, method='tfidf'):
        """Calculate similarity between two texts using various methods."""
        if method == 'tfidf':
            # Use TF-IDF and cosine similarity
            vectors = self.tfidf_vectorizer.fit_transform([text1, text2])
            return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        elif method == 'spacy':
            # Use spaCy's built-in similarity
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            return doc1.similarity(doc2)
        elif method == 'word2vec':
            # Use Word2Vec embeddings
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            
            # Get document vectors by averaging word vectors
            vec1 = sum([token.vector for token in doc1 if not token.is_stop and not token.is_punct]) / len(doc1)
            vec2 = sum([token.vector for token in doc2 if not token.is_stop and not token.is_punct]) / len(doc2)
            
            # Calculate cosine similarity
            return cosine_similarity([vec1], [vec2])[0][0]
            
    def extract_skills(self, text, skills_db):
        """Extract skills from text using a predefined skills database."""
        doc = self.nlp(text.lower())
        
        # Process each token and its surrounding context
        found_skills = set()
        for token in doc:
            # Check single tokens
            if token.text in skills_db:
                found_skills.add(token.text)
            
            # Check bigrams
            if token.i < len(doc) - 1:
                bigram = token.text + ' ' + doc[token.i + 1].text
                if bigram in skills_db:
                    found_skills.add(bigram)
            
            # Check trigrams
            if token.i < len(doc) - 2:
                trigram = token.text + ' ' + doc[token.i + 1].text + ' ' + doc[token.i + 2].text
                if trigram in skills_db:
                    found_skills.add(trigram)
        
        return list(found_skills)
