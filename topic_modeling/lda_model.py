from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def perform_topic_modeling(comments):
    vectorizer = CountVectorizer(max_features=1000, min_df=1)
    X = vectorizer.fit_transform(comments)

    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(X)

    topics = []
    for idx, topic in enumerate(lda.components_):
        topics.append([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])
    
    return topics

