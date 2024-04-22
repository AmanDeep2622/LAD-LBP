import pandas as pd
from collections import defaultdict
import json

def construct_hypergraph(data_file):
  """
  Constructs a hypergraph from a CSV file of binarized features using pandas.

  Args:
      data_file (str): Path to the CSV file.

  Returns:
      None: Saves the hypergraph (nodes and hyperedges) to separate JSON files.
  """
  nodes = defaultdict(int)  # Map feature names to node IDs (unique integer)
  next_node_id = 0

  # Map data point ID to list of connected feature IDs and value
  hyperedges = defaultdict(list)

  # Read CSV data using pandas
  data = pd.read_csv(data_file,nrows=20000)

  # Assign unique IDs to features (nodes)
  # Assuming class label is in the last column
  for feature in data.columns[:-1]:
    if feature not in nodes:
      nodes[feature] = next_node_id
      next_node_id += 1

  for row_id, row in data.iterrows():
    # Extract features and class label
    features = [nodes[f]
                for f in data.columns[:-1] if row[f] == 1]  # Get active features
    class_label = int(row[-1])  # Assuming class label is in the last column

    # Create hyperedge and add to dictionary
    hyperedges[row_id] = (features, class_label)

  # Store nodes and hyperedges in separate JSON files
  with open("HG/hypergraph_nodes.json", "w") as f:
    json.dump(nodes, f)
  with open("HG/hypergraph_hyperedges.json", "w") as f:
    json.dump(hyperedges, f)


# Example usage
data_file = "HG/ss1.csv"
# total_rows = sum(1 for line in open('HG/ss1.csv'))
# skip_rows = total_rows - 20000
# test_df = pd.read_csv('HG/ss1.csv', skiprows=range(1, skip_rows),nrows=10000)
# y = "HG/test.csv"  # input("enter path name")
# test_df.to_csv(y, index=None)
construct_hypergraph(data_file)

print("Hypergraph information saved to JSON files.")
