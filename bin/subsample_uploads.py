"""Select a single DIASource from each input upload files"""
from glob import glob
import csv
import click
import random
import gzip


@click.command()
@click.argument("indir")
@click.argument("outfile")
def subsample(indir: str, outfile: str):


    with open(outfile, 'w') as f:

        f.write(',diaSourceId,local_path,relative_path,dataId\n')
        for upload in glob(f"{indir}/upload*.csv.gz"):
            print(upload)
            try:
                with gzip.open(upload,'rt') as csvfile:
                    rows = []
                    for row in csvfile:
                        rows.append(row)

                    random_row = random.choice(rows)
                    # avoid the initial line
                    while random_row.startswith(','):
                        random_row = random.choice(rows)
                    f.write(random_row)
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    subsample()

