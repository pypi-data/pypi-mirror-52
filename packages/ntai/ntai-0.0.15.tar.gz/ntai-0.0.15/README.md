# ntai
ntai stands for nucleotide (nt) artificial intelligence (A.I.). ntai is a small
python library for using fasta sequences with artificial intelligence (A.I.).

Currently there are two main modules that will be of use

1. `Codex`, and
2. `bedtools`

## Codex
`Codex` is a class for hot-encoding fasta sequences into channels and back.
`Codex` is useful because a character in a fasta sequences can encode multiple
nucleotides or even random repeats.

## bedtools

`bedtools` is a function exposing the `bedtools` library to python. This allows
users to extract fasta sequences from a reference genome with writing to /
reading from files.

## fetch
`fetch` is a module for fetching the necessary data for using `ntai`.
Currently `fetch.utils` supports the requests for:

- `fetch_hg38` acquires the fasta for hg38 gzipped
- `fetch_exons` acquires Gencode Comprehensive v28 exons in bed format
- `fetch_introns` acquires Gencode Comprehensive v28 introns in bed format

- `fetch_hg38_chrom_sizes` acquires the chromosome sizes for hg38 in tsv format

- `decompress` will decompress a `.gz` file


The function `fetch.fetch_files` will get all of these files and decompress hg38 in a specified directory.

[bedtools]: https://bedtools.readthedocs.io/en/latest/
