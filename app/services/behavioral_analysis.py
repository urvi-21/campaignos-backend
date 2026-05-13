from app.services.embedding_service import generate_embeddings
from app.services.clustering_service import cluster_signals


def analyze_behavioral_patterns(texts):

    embeddings = generate_embeddings(texts)

    labels = cluster_signals(
        embeddings,
        num_clusters=3
    )

    clustered_results = []

    for text, label in zip(texts, labels):

        clustered_results.append({
            "text": text,
            "cluster": int(label)
        })

    return clustered_results