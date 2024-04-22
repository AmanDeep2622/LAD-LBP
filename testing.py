from sklearn.metrics import confusion_matrix, accuracy_score
import ast
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

df_full = pd.read_csv(r'KDDTRAIN_CSV_numerical-25k.csv')
test_df = df_full.tail(10000)
train_df = pd.read_csv(r'KDDTRAIN_CSV_numerical-25k.csv')
patterns_df = pd.read_csv(r'patterns.csv')
# result_df = pd.DataFrame()

def evaluate_term(term, data_point):
    # Extracting column index from the term
    col_index = int(term[term.index('[') + 1:term.index(']')])

    # Extracting condition from the term
    condition = term.split('  ')[1]

    # Get the actual value from the data point using column index
    value = data_point[col_index - 1]

   # Evaluate the condition
    if '>=' in condition:
        return value >= float(condition[2:])
    elif '==' in condition:
        return value == float(condition[2:])
    elif '!=' in condition:
        return value != float(condition[2:])
    elif '<=' in condition:
        return value <= float(condition[2:])
    elif '<' in condition:
        return value < float(condition[1:])
    elif '>' in condition:
        return value > float(condition[1:])
    else:
        raise ValueError("Invalid condition format!")


def testing(test_df, train_df, patterns_df):
    # Check if column types of testing and training dataframes are the same
    if not test_df.dtypes.equals(train_df.dtypes):
        raise ValueError(
            "Column types of testing and training dataframes do not match!")

    # Create a new dataframe with a column named 'result'
    result_df = pd.DataFrame()
    result_df["actual_result"] = test_df["class"].copy()
    result_df["pred_result"] = None
    # Iterate through each data point in the testing dataset
    for index, row in test_df.iterrows():
        match_found = False

        # Check if the data point matches any of the conditions given in the patterns
        for _, pattern_row in patterns_df.iterrows():
            pattern = ast.literal_eval(pattern_row['col2'])
            condition_matched = True
            for term in pattern:
                if not evaluate_term(term, row):
                    condition_matched = False
                    break
            if condition_matched:
                match_found = True
                break

        # Append 1 to the 'result' column if a match is found, else append 0
        if match_found:
            result_df.at[index, "pred_result"] = 1
        else:
            result_df.at[index, "pred_result"] = 0
    result_df['pred_result'] = result_df['pred_result'].astype(int)

    return result_df


result_df = testing(test_df, train_df, patterns_df)
result_df.to_csv("result_testing.csv", index=None)

# Check for missing values in the target columns
# missing_values_actual = result_df['actual_result'].isnull().sum()
# missing_values_pred = result_df['pred_result'].isnull().sum()
# print("Missing values in actual_result:", missing_values_actual)
# print("Missing values in pred_result:", missing_values_pred)

# Compute and display classification metrics
precision = precision_score(
    y_true=result_df['actual_result'], y_pred=result_df['pred_result'])
recall = recall_score(
    y_true=result_df['actual_result'], y_pred=result_df['pred_result'])
f1 = f1_score(y_true=result_df['actual_result'],
              y_pred=result_df['pred_result'])
print("\n\nClassification Metrics")
print("Precision:\t{:.4f}".format(precision))
print("Recall:\t\t{:.4f}".format(recall))
print("F1 Score:\t{:.4f}".format(f1))

# Assuming result_df is your DataFrame containing both actual and predicted labels
y_true = result_df['actual_result']
y_pred = result_df['pred_result']

# Calculate the confusion matrix
conf_matrix = confusion_matrix(y_true, y_pred)
# Extract values from confusion matrix
tn, fp, fn, tp = conf_matrix.ravel()
accuracy = accuracy_score(y_true, y_pred)
print("Accuracy:", accuracy)
print("False Positives (FP):", fp)
print("False Negatives (FN):", fn)
