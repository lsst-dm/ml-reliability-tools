"""Select a single DIASource from each input upload files"""
from glob import glob
import pandas as pd
import csv
import click
import random
import gzip

from lsst.daf.butler import Butler


@click.command()
@click.argument("infile")
@click.argument("outfile")
@click.argument("repo")
@click.argument("collection")
def subsample(infile: str, outfile: str, repo: str, collection: str):

    df = pd.read_csv(infile)

    butler = Butler(repo, collections=collection)

    sampled_rows = []
    for idx, row in df.iterrows():

            dataId_str = row['dataId']

            # work around the string dump in drp_cutouts.py which 
            # doesn't quote the keys
            for key in ['instrument', 'detector', 'visit', 'band', 'day_obs', 'physical_filter']:
                dataId_str = dataId_str.replace(key, '"'+key+'"')

            dataId = eval(dataId_str)

            try:
                diasrc = butler.get('goodSeeingDiff_diaSrcTable', 
                        dataId = dataId)
                sampled_diasrc = diasrc[diasrc['diaSourceId'] == row['diaSourceId']].copy()

                # propagate in what's needed for the full dataId
                sampled_diasrc['instrument'] = dataId['instrument']
                sampled_diasrc['day_obs'] = dataId['day_obs']
                sampled_diasrc['physical_filter'] = dataId['physical_filter']
                sampled_rows.append(sampled_diasrc)

            except Exception as e:
                print(e)
                continue

    df_out = pd.concat(sampled_rows, ignore_index=True)
    df_out.to_csv(outfile)


if __name__ == "__main__":
    subsample()

