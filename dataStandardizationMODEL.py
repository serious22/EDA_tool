import pandas as pd
import numpy as np
from collections import defaultdict
from fuzzywuzzy import process


def fuzzy_grouping(column, threshold=80):
    # Create a mapping for grouped values
    column = column.astype(str).fillna('')
    grouped = defaultdict(list)
    
    # Sort unique values by frequency
    unique_values = column.value_counts().index.tolist()

    # Iterate over the unique values and apply fuzzy matching
    for value in unique_values:
        if not any(value in group for group in grouped.values()):
            # Find close matches using fuzzy matching
            matches = process.extractBests(value, unique_values, score_cutoff=threshold)
            grouped[value] = [match[0] for match in matches]
    
    # Create a reverse lookup for standardization
    reverse_mapping = {}
    for group, values in grouped.items():
        for value in values:
            reverse_mapping[value] = group

    # Standardize the column values
    return column.map(reverse_mapping)

def find_optimal_top_n(column):
    # Get the frequency of unique values
    value_counts = column.value_counts()


    # You can further implement a mathematical elbow detection algorithm to find the optimal top_n
    # For now, return the point where the frequency drops significantly (as a simple heuristic)
    differences = value_counts.diff().abs()
    
    # Define a threshold for a large drop (this can be tuned)
    threshold = 0.4 * value_counts.max()
    
    # Find the index where the difference is greater than the threshold
    elbow_point = differences[differences > threshold].index
    if len(elbow_point) == 0:
        top_n = len(value_counts)  # Default to all values
    else:
        # Get location of the elbow and add 1 to make it 1-based
        top_n = value_counts.index.get_loc(elbow_point[0])
    
    return top_n

def standardised_set(column, top_n):
    column = column.str.lower().str.strip()
    correct_labels = column.value_counts().nlargest(top_n).index.tolist()

    mapping = defaultdict(str)
    for value in column.unique():
        closest_match = process.extractOne(value, correct_labels)[0]
        mapping[value] = closest_match

    return column.map(mapping)