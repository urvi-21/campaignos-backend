from sklearn.cluster import KMeans


def cluster_signals(embeddings, num_clusters=3):

    model = KMeans(
        n_clusters=num_clusters,
        random_state=42
    )

    labels = model.fit_predict(embeddings)

    return labels