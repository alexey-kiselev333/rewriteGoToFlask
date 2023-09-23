import ast
from pathlib import Path

import rethinkdb as r



import ast
from pathlib import Path
from typing import List, Union

import numpy as np
import random_name
import simplejson

data_dir = Path.home() / "whooshBack" / "dataset"
filename = Path("graph.csv")

# file = open('/home/alexey/pythonProject2/mockinghack/back/dataset/purchases.csv','r')
#
# arr = []
#
# for row in file:
#     arr.append(row)
#
#
#
# print(arr[0].split(";"))


def get_data(
    data_dir: Union[Path, str],
    filename: str,
    embedding_field="embedding",
    load_embedding=True,
    ext=".json",
    parse_meta: bool = False,
    lazy: bool = False,
    sep: str = ",",
    encoding: str = "utf-8-sig",
    as_record: bool = False,
    rename_columns: dict = None,
    engine: str = "pandas",
    **kwargs,
):
    assert engine in ("pandas", "polars")
    if engine == "polars":
        import polars as pd
    else:
        import pandas as pd
    data_dir = Path(data_dir)
    db_filename = filename
    db_filepath = data_dir / (db_filename + ext)

    if ext in (".csv", ".tsv", ".xlsx", ".pickle", ".gz"):
        columns_needed = list(rename_columns.keys()) if rename_columns else None
        if ext == ".xlsx":
            df = pd.read_excel(db_filepath, engine="openpyxl") if engine == "pandas" else pd.read_excel(db_filepath)
        elif ext in (".tsv", ".csv"):
            if engine == "pandas":
                df = pd.read_csv(
                    db_filepath,
                    encoding=encoding,
                    usecols=columns_needed,
                    skipinitialspace=True,
                    sep=sep,
                    **kwargs,
                )
            else:
                df = pd.read_csv(db_filepath, encoding=encoding, sep=sep)
                df = df[columns_needed] if columns_needed else df
        elif ext in (".pickle"):
            df = pd.read_pickle(db_filepath, **kwargs)
        else:
            df = pd.read_csv(db_filepath, header=0, error_bad_lines=False, **kwargs)
        if rename_columns is not None:
            df = df.rename(rename_columns) if rename_columns else df
        if as_record:
            yield df.to_dict(orient="records")
        else:
            yield df
        raise StopIteration()
    with open(str(db_filepath), "r", encoding=encoding) as j_ptr:
        if lazy:
            for jline in j_ptr:
                yield simplejson.loads(jline)
        else:
            docs = simplejson.load(j_ptr)

    if lazy:
        raise StopIteration()

    if parse_meta:
        for d in docs:
            d["meta"] = ast.literal_eval(d["meta"])

    if embedding_field is not None:
        if load_embedding:
            index_filename = filename + "_index" + ".npy"
            index_filepath = data_dir / index_filename
            embeddings = np.load(str(index_filepath))
            for iDoc, iEmb in zip(docs, embeddings):
                iDoc[embedding_field] = iEmb
        else:
            for iDoc in docs:
                iDoc[embedding_field] = np.nan

    yield docs


df = next(get_data(data_dir=data_dir,filename=filename.stem, ext=filename.suffix, engine="pandas", sep=","))
df = df.fillna('')
arr = df.to_dict(orient="records")

rdb = r.RethinkDB()
conn = rdb.connect(host='rethinkdb', port=28015)

if not rdb.db_list().contains('whoosh').run(conn):
    rdb.db_create('whoosh').run(conn)

if not rdb.db('whoosh').table_list().contains('graph').run(conn):
    rdb.db('whoosh').table_create('graph').run(conn)

if not rdb.db('whoosh').table_list().contains('dijkstra').run(conn):
    rdb.db('whoosh').table_create('dijkstra',primary_key='idx').run(conn)

for row in arr:
    rdb.db('whoosh').table('graph').insert({'index': row["index"], '0': row["0"],'1':row["1"],
                                                     '2': row["2"],'3': row["3"],'4': row["4"],
                                                            '5': row["5"],'6': row["6"],'7': row["7"],
                                                            '8': row["8"],
                                                            '9': row["9"],
                                                            '10': row["10"],
                                                            '11': row["11"],
                                                            '12': row["12"],
                                                            '13': row["13"],
                                                            '14': row["14"],
                                                            '15': row["15"],
                                                            '16': row["16"],
                                                            '17': row["17"],
                                                            }).run(conn)



__all__ = ["get_data"]

