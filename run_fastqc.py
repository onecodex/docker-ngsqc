#!/usr/bin/python

import argparse
import json
import os
import shutil
import subprocess
import sys

def parse_fastqc_summary(f):
    out = {
        'status': 'success',
        'filename': '',
        'fastqc_version': '',
        'basic_statistics': {},
        'other_modules': {}
    }
    modules = {}
    capture_basic_stats = False
    for line in f:
        line = line.strip() # Trim newline
        if capture_basic_stats:
            if line.startswith('#'):
                continue
            if line == '>>END_MODULE':
                capture_basic_stats = False
                continue
            stat_name = line.split('\t')[0].replace(' ', '_').lower()
            stat_name = stat_name.replace('%', 'percent_')
            stat = line.split('\t')[1]
            out['basic_statistics'][stat_name] = stat
        elif line.startswith('##'):
            out['fastqc_version'] = line.split()[-1]
        elif line.startswith('>>Basic Statistics'):
            capture_basic_stats = True
        elif line.startswith('>>') and line != '>>END_MODULE':
            module_name = '_'.join(line.split()[:-1]).lower()[2:]
            module_status = line.split()[-1]
            out['other_modules'][module_name] = module_status
    out['filename'] = out['basic_statistics'].pop('filename', '')
    return out

def parse_fastqc_details(f):
    modules = []
    for line in f:
        line = line.strip() # trim endline
        if line == '>>END_MODULE':
            modules.append(d)
        elif line.startswith('##'):
            continue
        elif line.startswith('>>') and line != '>>END_MODULE': # for each module grab summary data
            module_name = '_'.join(line.split()[:-1]).lower()[2:]
            d = {}
            d['name'] = module_name
            d['status'] = line[-4:] # and overall status pass/warn/fail
        elif line[:2] != '>>' and line[0] == '#': # grab details under each module
            d['data'] = []
            cols = line.lstrip('#').split('\t')
        else:
            vals = line.split('\t')
            d['data'].append(dict(zip(cols, vals)))
    return modules

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('reads', help='Input FASTQ, SAM, or BAM file')
    parser.add_argument('output', help='Output folder')
    parser.add_argument('--fastqc', default='fastqc', help='path to fastqc executable')
    parser.add_argument('--report', action='store_true', default=False, help='Generate HTML report of QC values')
    parser.add_argument('--full-json', action='store_true', default=False, help='Include all data in JSON output')
    args = parser.parse_args()

    reads = os.path.abspath(args.reads)
    outdir = os.path.abspath(args.output)
    prefix, ext = os.path.splitext(os.path.basename(reads))
    if ext == '.gz':
        prefix = os.path.splitext(prefix)[0]
    out_prefix = prefix + '_fastqc_report'

    if not os.path.exists(reads):
        sys.exit('File does not exist')

    try:
        subprocess.check_call([args.fastqc, reads, '-o', outdir, '--extract'])
    except subprocess.CalledProcessError:
        out = {
            'status': 'error',
            'message': 'FastQC failed to finish successfully'
        }
    else:
        # get the fastqc data filename
        fastqc_dirname = prefix + '_fastqc'
        fastqc_data_filename = os.path.join(outdir, fastqc_dirname, 'fastqc_data.txt')
        with open(fastqc_data_filename) as f:
            fastqc_data = list(f)

        out = parse_fastqc_summary(fastqc_data)
        if args.full_json:
            out['results'] = parse_fastqc_details(fastqc_data)

        # Move fastqc_data.txt from temp to output directory
        shutil.move(fastqc_data_filename, os.path.join(outdir, out_prefix + '.txt'))

        # Save HTML report, if --report enabled
        if args.report:
            fastqc_report_src = os.path.join(outdir, fastqc_dirname, 'fastqc_report.html')
            fastqc_report_dest = out_prefix + '.html'
            shutil.move(fastqc_report_src, fastqc_report_dest)

    json.dump(out, open(os.path.join(outdir, out_prefix + '.json'), 'w'), indent=4)
