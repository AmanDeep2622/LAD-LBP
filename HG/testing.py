from sklearn.metrics import confusion_matrix, accuracy_score
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# df_full = pd.read_csv(r'KDDTRAIN_CSV_numerical-25k.csv')
# test_df = df_full.tail(10000)
# train_df = pd.read_csv(r'KDDTRAIN_CSV_numerical-25k.csv')
patterns_df = pd.read_csv(r'HG/rules.csv')

orig_df = pd.read_csv('HG/ss1.csv')

# Shuffle the rows
# orig_df = orig_df.sample(frac=1).reset_index(drop=True)
orig_df = orig_df.tail(5000)
# orig_df = pd.read_csv(r'HG/test.csv')
test_df = orig_df.drop('result', axis=1)


def evaluate_term(term, data_point):
    if (data_point[term]):
        return True
    else:
        return False


def testing(test_df, orig_df, patterns_df):
    # Check if column types of testing and training dataframes are the same
    # if not test_df.dtypes.equals(train_df.dtypes):
    #     raise ValueError(
    #         "Column types of testing and training dataframes do not match!")

    # Create a new dataframe with a column named 'result'
    result_df = pd.DataFrame()
    result_df["actual_result"] = orig_df["result"].copy()
    result_df["pred_result"] = None
    # Iterate through each data point in the testing dataset
    i=1
    for index, row in test_df.iterrows():
        print("Testing pattern number {}".format(i))
        i=i+1
        match_found = False

        # Check if the data point matches any of the conditions given in the patterns
        for _, pattern_row in patterns_df.iterrows():
            pattern = pattern_row['col2'].split(' & ')
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


result_df = testing(test_df, orig_df, patterns_df)
result_df.to_csv("HG/result_testing.csv", index=None)

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
