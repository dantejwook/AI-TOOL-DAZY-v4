from hdbscan import HDBSCAN
from config import MIN_CLUSTER_SIZE, MIN_SAMPLES

def cluster(vectors):
    return HDBSCAN(
        min_cluster_size=MIN_CLUSTER_SIZE,
        min_samples=MIN_SAMPLES,
    ).fit_predict(vectors)
