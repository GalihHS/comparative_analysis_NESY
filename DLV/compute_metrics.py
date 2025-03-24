import time
import argparse

def load_triples(file_path):
    """Load triples from a file into a set."""
    triples = set()
    nodes = set()
    with open(file_path, 'r') as file:
        for line in file:
            id1, relation, id2 = line.strip().split()
            triples.add((id1, relation, id2))
            nodes.update([id1, id2])
    return triples, nodes

def compute_rank(test_triple, graph_triples, train_triples, total_nodes):
    """Compute the rank of a test triple based on the given graph for both head and tail prediction, excluding train triples."""
    id1, relation, id2 = test_triple
    
    # Tail prediction (predicting id2 given id1 and relation)
    found_tail_links = sum(1 for (s, p, o) in graph_triples if s == id1 and p == relation and (s, p, o) not in train_triples)
    if (id1, relation, id2) in graph_triples:
        tail_rank = found_tail_links / 2 + 0.5
    else:
        tail_rank = (total_nodes - 1) / 2 + found_tail_links / 2 + 0.5
    
    # Head prediction (predicting id1 given relation and id2)
    found_head_links = sum(1 for (s, p, o) in graph_triples if o == id2 and p == relation and (s, p, o) not in train_triples)
    if (id1, relation, id2) in graph_triples:
        head_rank = found_head_links / 2 + 0.5
    else:
        head_rank = (total_nodes - 1) / 2 + found_head_links / 2 + 0.5
    
    return (tail_rank + head_rank) / 2

def compute_metrics(test_file, graph_file, train_file):
    """Compute HITS@1, HITS@3, HITS@10, and MRR based on the given files."""
    test_triples, _ = load_triples(test_file)
    graph_triples, nodes = load_triples(graph_file)
    train_triples, _ = load_triples(train_file)
    total_nodes = len(nodes)
    
    ranks = []
    start_time = time.time()
    
    for triple in test_triples:
        rank = compute_rank(triple, graph_triples, train_triples, total_nodes)
        ranks.append(rank)
    
    end_time = time.time()
    evaluation_time = end_time - start_time
    
    hits_at_1 = sum(1 for r in ranks if r <= 1) / len(ranks)
    hits_at_3 = sum(1 for r in ranks if r <= 3) / len(ranks)
    hits_at_10 = sum(1 for r in ranks if r <= 10) / len(ranks)
    mrr = sum(1 / r for r in ranks) / len(ranks)
    
    return {
        "HITS@1": hits_at_1,
        "HITS@3": hits_at_3,
        "HITS@10": hits_at_10,
        "MRR": mrr,
        "Total Evaluation Time": evaluation_time
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute graph evaluation metrics.")
    parser.add_argument("test_file", help="Path to the test file.")
    parser.add_argument("saturated_file", help="Path to the saturated graph file.")
    parser.add_argument("train_file", help="Path to the train graph file.")
    args = parser.parse_args()
    
    metrics = compute_metrics(args.test_file, args.saturated_file, args.train_file)
    
    for metric, value in metrics.items():
        print(f"{metric}: {value:.6f}")
