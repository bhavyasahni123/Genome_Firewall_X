import json
import time
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd
from tqdm import tqdm

from config import OUTPUT_DIR, TEMP_DIR, AMRFINDER, MAX_WORKERS

TARGET_FOLDER = "genome_10"

DISCOVERY_DIR = OUTPUT_DIR / "discovery"
AMRFINDER_DIR = OUTPUT_DIR / "amrfinder"
DISCOVERY_DIR.mkdir(parents=True, exist_ok=True)
AMRFINDER_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_DIR = AMRFINDER_DIR / TARGET_FOLDER
CHUNK_DIR.mkdir(parents=True, exist_ok=True)

GENOME_LIST = DISCOVERY_DIR / "genome_list.json"
FINAL_PARQUET = AMRFINDER_DIR / f"{TARGET_FOLDER}.parquet"
SUMMARY_FILE = AMRFINDER_DIR / f"{TARGET_FOLDER}_summary.json"
PROCESSED_FILE = AMRFINDER_DIR / f"{TARGET_FOLDER}_processed.txt"
FAILED_FILE = AMRFINDER_DIR / f"{TARGET_FOLDER}_failed.txt"

FLUSH_INTERVAL = 200
_chunk = 0

def load_genomes():
    with open(GENOME_LIST) as f:
        genomes = json.load(f)
    return [g for g in genomes if g["folder"] == TARGET_FOLDER]

def load_processed():
    if not PROCESSED_FILE.exists():
        return set()
    return set(PROCESSED_FILE.read_text().splitlines())

def mark_processed(gid):
    with open(PROCESSED_FILE,"a") as f:
        f.write(gid + "\n")

def mark_failed(gid, reason):
    with open(FAILED_FILE,"a") as f:
        f.write(f"{gid}\t{reason}\n")

def run_amrfinder(genome):
    gid = genome["genome_id"]
    out = TEMP_DIR / f"{gid}.tsv"
    cmd = [AMRFINDER, "-n", genome["path"], "-o", str(out)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status":"success","genome_id":gid,"tsv":str(out)}
    except Exception as e:
        return {"status":"failed","genome_id":gid,"reason":str(e)}

def flush_buffer(buffer):
    global _chunk
    if not buffer:
        return
    dfs=[]
    for item in buffer:
        tsv=Path(item["tsv"])
        if not tsv.exists():
            continue
        try:
            df=pd.read_csv(tsv,sep="\t")
            df["Genome_ID"]=item["genome_id"]
            dfs.append(df)
        finally:
            tsv.unlink(missing_ok=True)
    if dfs:
        _chunk+=1
        pd.concat(dfs,ignore_index=True).to_parquet(CHUNK_DIR/f"chunk_{_chunk:05d}.parquet",index=False,engine="pyarrow")
    buffer.clear()

def merge_chunks():
    files=sorted(CHUNK_DIR.glob("chunk_*.parquet"))
    if not files:
        return
    df=pd.concat([pd.read_parquet(f) for f in files],ignore_index=True)
    df.to_parquet(FINAL_PARQUET,index=False,engine="pyarrow")

def main():
    start=time.time()
    genomes=[g for g in load_genomes() if g["genome_id"] not in load_processed()]
    buffer=[]
    ok=bad=0
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures={ex.submit(run_amrfinder,g):g for g in genomes}
        for fut in tqdm(as_completed(futures),total=len(futures)):
            r=fut.result()
            if r["status"]!="success":
                bad+=1
                mark_failed(r["genome_id"],r["reason"])
                continue
            ok+=1
            mark_processed(r["genome_id"])
            buffer.append(r)
            if len(buffer)>=FLUSH_INTERVAL:
                flush_buffer(buffer)
    flush_buffer(buffer)
    merge_chunks()
    with open(SUMMARY_FILE,"w") as f:
        json.dump({"processed":ok,"failed":bad,"runtime_minutes":round((time.time()-start)/60,2)},f,indent=2)

if __name__=="__main__":
    main()
