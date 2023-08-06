import pandas as pd
import numpy as np
import sys
import click
from functools import reduce

@click.command()
@click.option('--input_file', '-i', default='', help='file to parse')
@click.option('--labels', '-l', default='', help='comma separated list of labels (treated as AND)')
@click.option('--output_file', '-o', default='', help='file to write out')
def run(input_file, labels, output_file):

    cards_df = pd.read_csv(input_file, header=None)
    cards_df.columns = cards_df.iloc[0]
    cards_df = cards_df.reindex(cards_df.index.drop(0)).reset_index(drop=True)
    cards_df["Labels"] = cards_df["Labels"].fillna("")
    labels_list = [l.replace(" ", "") for l in labels.split(",")]

    match_masks = []
    
    for l in labels_list:    
        match_masks.append(cards_df["Labels"].str.contains(l))

    final_match_mask = reduce(lambda acc, x: np.logical_and(acc, x), match_masks)
    
    write_df = pd.DataFrame(cards_df[final_match_mask])

    write_df.to_csv(output_file, index=False)
