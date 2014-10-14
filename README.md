# docker-ngsqc

NGS QC and pre-processing tools

## Installation

    docker pull quay.io/refgenomics/docker-ngsqc
    docker run  quay.io/refgenomics/docker-ngsqc

## Available binaries

### FASTQ QC statistics with `FastQC`

This image contains [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/). To run:

    docker run quay.io/refgenomics/docker-qc fastqc -help

There is also a convenience wrapper `fastqc_json`, which runs FastQC and outputs a JSON report:

    docker run quay.io/refgenomics/docker-qc fastqc_json [reads_file] [json_report]

### Adapter trimming with `skewer`

This image contains [Skewer](https://github.com/relipmoc/skewer). To run:

    docker run quay.io/refgenomics/docker-qc skewer --help

## Copyright and License

MIT License, see [LICENSE](LICENSE.md) for details.

Binaries within this docker may be using different licenses, please check before distributing.

Copyright (c) 2014 [One Codex](https://www.onecodex.com), [Nik Krumm](https://github.com/nkrumm), and contributors.
