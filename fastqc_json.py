#!/usr/bin/python

import subprocess
import argparse
import tempfile
import json
import os

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("reads", help="Input FASTQ, SAM, or BAM file")
    parser.add_argument("output", help="Output path for QC file (json formatted)")
    parser.add_argument("--fastqc", default="fastqc", help="path to fastqc executable")
    args = parser.parse_args()

    outdir = tempfile.mkdtemp()

    cmd = [args.fastqc, args.reads, "--extract", "-o", outdir]
    r = subprocess.call(cmd)
    if r != 0:
        # raise exception instead?
        raise Exception("FastQC failed!")

    out = {}
    outsubdir = os.path.splitext(os.path.basename(args.reads))[0] + "_fastqc"
    data_filename = os.path.join(outdir, outsubdir, "fastqc_data.txt")

    with open(data_filename) as f:
        for line in f.readlines():
            line = line.strip() # trim endline
            if (line == ">>END_MODULE"):
                out[module_name] = d
            elif (line[0:2] == "##"):
                out["FastQC Version"] = line.split("\t")[1]
            elif (line[:2] == ">>" and line[:12] != ">>END_MODULE"): # for each module grab summary data
                module_name = line[2:-5] # grab module name
                d = {}
                d["status"] = line[-4:] # and overall status pass/warn/fail
            elif (line[:2] != ">>" and line[0] == "#"): # grab details under each module
                d["data"] = []
                cols = line.lstrip("#").split("\t")
            else:
                vals = line.split("\t")
                d["data"].append(dict(zip(cols, vals)))

    json.dump(out, open(args.output, 'w'), indent=4)

