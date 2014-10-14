#!/usr/bin/python

import subprocess
import argparse
import tempfile
import json
import os

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("reads", nargs="+", help="Input FASTQ, SAM, or BAM file(s)")
    parser.add_argument("output", help="Output path for QC file (json formatted)")
    parser.add_argument("--fastqc", default="fastqc", help="path to fastqc executable")
    args = parser.parse_args()
    
    outjson = {}
    
    for read_filename in args.reads:
        outdir = tempfile.mkdtemp()
        out = {} 
        cmd = [args.fastqc, read_filename, "--extract", "-o", outdir]
        r = subprocess.call(cmd)
        if r != 0:
            out["status"] = "error"
            out["message"] = "FastQC failed to finish successfully"
        else:
            out["status"] = "success"
            out["modules"] = []
            # get the fastqc data filename
            fastqc_data_dir = os.path.splitext(os.path.basename(read_filename))[0] + "_fastqc"
            fastqc_data_filename = os.path.join(outdir, fastqc_data_dir, "fastqc_data.txt")

            with open(fastqc_data_filename) as f:
                for line in f.readlines():
                    line = line.strip() # trim endline
                    if (line == ">>END_MODULE"):
                        out["modules"].append(d)
                    elif (line[0:2] == "##"):
                        out["FastQC Version"] = line.split("\t")[1]
                    elif (line[:2] == ">>" and line[:12] != ">>END_MODULE"): # for each module grab summary data
                        module_name = line[2:-5] # grab module name
                        d = {}
                        d["name"] = module_name
                        d["status"] = line[-4:] # and overall status pass/warn/fail
                    elif (line[:2] != ">>" and line[0] == "#"): # grab details under each module
                        d["data"] = []
                        cols = line.lstrip("#").split("\t")
                    else:
                        vals = line.split("\t")
                        d["data"].append(dict(zip(cols, vals)))

        # save data in outjson, indexed by filename
        outjson[os.path.basename(read_filename)] = out
    
    json.dump(outjson, open(args.output, 'w'), indent=4)


