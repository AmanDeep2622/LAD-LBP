import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.fpm import FPGrowth
import json

def construct_hypergraph_dataframe(hyperedges_file, spark):
  """
  Constructs a PySpark DataFrame representing the hypergraph from a JSON file with the specified format.

  Args:
      hyperedges_file (str): Path to the JSON file containing hyperedges.
      spark (SparkSession): SparkSession object.

  Returns:
      pyspark.sql.DataFrame: DataFrame containing hyperedge information.
  """
  with open(hyperedges_file, "r") as f:
    hyperedges = json.load(f)

  data = []
  for key, value in hyperedges.items():
    features = value[0]
    class_label = value[1]
    data.append((features, class_label))

  return spark.createDataFrame(data, ["features", "class_label"])


def fhm_fp_growth(hyperedges_df, min_support):
  """
  Performs FHM using FP-Growth on a hypergraph DataFrame for positive class identification.

  Args:
      hyperedges_df (pyspark.sql.DataFrame): DataFrame containing hyperedge information.
      min_support (float): Minimum support threshold for frequent hyperedges.

  Returns:
      pyspark.sql.DataFrame: DataFrame of frequent hyperedges with support counts for the positive class.
  """
  # Filter for positive class hyperedges (class_label=1)
  positive_hyperedges_df = hyperedges_df.where(col("class_label") == 1)

  fp_growth = FPGrowth(minSupport=min_support, itemsCol="features")
  model = fp_growth.fit(positive_hyperedges_df)
  frequent_hyperedges_df = model.freqItemsets.sort(
      "items").select("items", "freq")

  return frequent_hyperedges_df


# Example usage
spark = SparkSession.builder.appName("FHM_LAD").getOrCreate()

# Replace with your actual file path
hyperedges_file = "HG/hypergraph_hyperedges.json"
min_support = 0.8

try:
  hyperedges_df = construct_hypergraph_dataframe(hyperedges_file, spark)
  frequent_hyperedges_df = fhm_fp_growth(hyperedges_df, min_support)

  # Print generated frequent hyperedges
  print("Positive Class Frequent Hyperedges:")
  frequent_hyperedges_df.show(truncate=False)
except ValueError as e:
  print("Error:", e)

# spark.stop()


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
      frequent_hyperedges_df (pyspark.sql.DataFrame): DataFrame of frequent hyperedges.
      feature_names (dict): Dictionary mapping feature IDs to feature names.

  Returns:
      list: List of rules as strings.
  """
  # No change is needed in DataFrame transformation, assuming feature IDs remain in "items" column

  rules = frequent_hyperedges_df.rdd.map(lambda row: " & ".join([feature_names[f] for f in row.items])) \
                                .collect()
  return rules



# Example usage (assuming frequent_hyperedges_df and feature_names are available)
nodes_file = "HG/hypergraph_nodes.json"
feature_names = load_feature_names(nodes_file)
rules = generate_rules(frequent_hyperedges_df, feature_names)

print(feature_names)


def get_feature_set(rule, feature_names):
  """
  Extracts feature set from a rule string using feature names dictionary.

  Args:
      rule (str): Rule string.
      feature_names (dict): Dictionary mapping feature IDs to feature names.

  Returns:
      list: List of feature IDs corresponding to the rule.
  """
  return [feature_names.get(f) for f in rule.split(" & ")]


def filter_prime_sufficient_rules(rules, hyperedges_df):
  """
  Filters rules based on potential "prime" and "sufficient" characteristics.

  Args:
      rules (list): List of generated rules as strings.
      hyperedges_df (pyspark.sql.DataFrame): DataFrame containing hyperedges.

  Returns:
      list: List of filtered rules considered potentially prime and sufficient.
  """
  some_threshold=0.1
  filtered_rules = []
  print(len(rules))
  i = 1
  for rule in rules:
    print(i)
    i=i+1
    # Convert rule string to list of features (feature names)
    rule_features = rule.split(" & ")

    # Check if removing any feature from the rule reduces coverage significantly
    # (Needs domain knowledge to define "significant reduction")
    for i in range(len(rule_features)):
      reduced_rule = " & ".join(rule_features[:i] + rule_features[i+1:])
      reduced_coverage = hyperedges_df.where(col("features").isin(
          get_feature_set(reduced_rule, feature_names))).count()
      original_coverage = hyperedges_df.where(
          col("features").isin(get_feature_set(rule, feature_names))).count()
      if original_coverage - reduced_coverage > some_threshold:  # Adjust threshold based on your domain
        continue  # Skip if removing a feature reduces coverage significantly

    filtered_rules.append(rule)
  return filtered_rules



filtered_rules = filter_prime_sufficient_rules(rules, hyperedges_df)

print("Filtered Rules (Potentially Prime and Sufficient):")
for rule in filtered_rules:
    print(rule)
df2 = pd.DataFrame(data={"col2": filtered_rules})
print(df2)
y = "HG/rules.csv"
df2.to_csv(y, index=None)
  
spark.stop()

# O(ml * ln(l))
# m- number of hyperedges
# l- average number of features per hyperedge
