import pandas as pd
from efdir import fs
import json
import ltdict.ltdict as ltlt
import edict.edict as eded

def csv_wcols(src_fn,from_file=True):
    df = pd.read_csv(src_fn)
    js = df.to_json()
    dst_fn = fs.repl_suffix(src_fn,"col.json")
    fs.wfile(dst_fn,js)


def csv2cols(src_fn,from_file=True):
    df = pd.read_csv(src_fn)
    columns = df.columns
    js = df.to_json()
    d = json.loads(js)
    cols = eded.mapvV(d,lambda ele:ltlt.json2ltdict(ele))
    return((list(columns),cols))

def csv_wdtb(src_fn,from_file=True):
    df = pd.read_csv(src_fn)
    js = df.T.to_json()
    dst_fn = fs.repl_suffix(src_fn,"dtb.json")
    fs.wfile(dst_fn,js)

def csv2dtb(src_fn,from_file=True):
    df = pd.read_csv(src_fn)
    columns = df.columns
    js = df.T.to_json()
    d = json.loads(js)
    dtb = ltlt.json2ltdict(d)
    dtb = ltlt.to_list(dtb)
    return(dtb)
