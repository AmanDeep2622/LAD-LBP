import pandas as pd
import mlxtend
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import json


def construct_hypergraph_dataframe(hyperedges_file):
    """
    Constructs a DataFrame representing the hypergraph from a JSON file with the specified format.

    Args:
        hyperedges_file (str): Path to the JSON file containing hyperedges.

    Returns:
        pandas.DataFrame: DataFrame containing hyperedge information.
    """
    with open(hyperedges_file, "r") as f:
        hyperedges = json.load(f)

    data = []
    for key, value in hyperedges.items():
        features = value[0]
        class_label = value[1]
        if class_label==1:
            data.append(features)

    return data

def fhm_fp_growth(hyperedges_df, min_support):
    """
    Performs FHM using FP-Growth on a hypergraph DataFrame for positive class identification.

    Args:
        hyperedges_df (pandas.DataFrame): DataFrame containing hyperedge information.
        min_support (float): Minimum support threshold for frequent hyperedges.

    Returns:
        pandas.DataFrame: DataFrame of frequent hyperedges with support counts for the positive class.
    """
    te = TransactionEncoder()
    print(1)
    te_ary = te.fit(hyperedges_df).transform(hyperedges_df)
    print(2)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    print(3)
    frequent_hyperedges_df = fpgrowth(
        df, min_support=min_support, use_colnames=True)
    print(3)
    return frequent_hyperedges_df


# Example usage
hyperedges_file = "HG/hypergraph_hyperedges.json"
min_support = 0.5

hyperedges_df = construct_hypergraph_dataframe(hyperedges_file)
frequent_hyperedges_df = fhm_fp_growth(hyperedges_df, min_support)

print("Positive Class Frequent Hyperedges:")
print(frequent_hyperedges_df)


def load_feature_names(nodes_file):
  """
  Loads feature names from a JSON file (hypergraph_nodes.json).

  Args:
      nodes_file (str): Path to the JSON file containing feature names.

  Returns:
      dict: Dictionary where keys are feature IDs and values are feature names.
  """
  with open(nodes_file, "r") as f:
    nodes = json.load(f)

  feature_names = {}
  for feature_name, feature_id in nodes.items():
    # Split feature name and condition (if present)
    # parts = feature_name.split("=")
    # clean_feature_name = parts[0].strip()  # Remove leading/trailing whitespace

    # Store feature name directly in dictionary using feature ID as key
    feature_names[feature_id] = feature_name

  return feature_names


def generate_rules(frequent_hyperedges_df, feature_names):
    """
    Generates rules from frequent hyperedges DataFrame.

    Args:
        frequent_hyperedges_df (pandas.DataFrame): DataFrame of frequent hyperedges.
        feature_names (dict): Dictionary mapping feature IDs to feature names.

    Returns:
        list: List of rules as strings.
    """
    rules = []
    for index, row in frequent_hyperedges_df.iterrows():
        itemsets = row['itemsets']
        support = row['support']
        feature_set = [feature_names.get(f) for f in itemsets]
        rule = " & ".join(feature_set)
        rules.append(rule)
    return rules


nodes_file = "HG/hypergraph_nodes.json"
feature_names = load_feature_names(nodes_file)
rules = generate_rules(frequent_hyperedges_df, feature_names)

print("Generated Rules:")
for rule in rules:
    print(f"Rule: {rule}")

df2 = pd.DataFrame(data={"col2": rules})
print(df2)
y = "HG/demoRules.csv"
df2.to_csv(y, index=None)
