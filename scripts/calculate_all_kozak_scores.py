import argparse
from Bio import SeqIO
import csv
import re
import sys

def read_fasta(filepath):
    """Reads a FASTA file and returns dictionaries of sequences and headers indexed by header."""
    sequences = {}
    headers = {}
    with open(filepath, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            full_index = record.description.split()[0]
            sequences[full_index] = str(record.seq)
            headers[full_index] = record.description
    return sequences, headers

def calculate_kozak_score(transcript, orf):
    """Calculates the Kozak score based on specific nucleotide preferences at key positions."""
    start_index = transcript.find(orf[:3])  # Find the start codon index in the transcript
    if start_index == -1 or start_index < 6 or start_index + 1 >= len(transcript):
        return 'NA'  # Not applicable or insufficient context
    sequence = transcript[start_index-6:start_index] + transcript[start_index+3:start_index+4]
    if len(sequence) != 7:
        return 'NA'
    kozak_score = 3 * sum((sequence[0] == "G", sequence[3] in "AG", sequence[-1] == "G")) + sum((sequence[1] == "C", sequence[2] == "C", sequence[4] == "C", sequence[5] == "C"))
    return kozak_score

def parse_header_info(header, tool):
    """Parses the header based on the specified tool."""
    details = {}
    if tool == 'orfipy':
        parts = header.split()
        details['name'] = parts[0]
        details['orf'] = parts[1]
        details['start'] = parts[2].split('[')[1].split('-')[0]
        details['stop'] = parts[2].split('-')[1].split(']')[0]
        details['strand'] = parts[2][-2]
        details['type'] = parts[3].split(':')[1]
        details['length'] = parts[4].split(':')[1]
        details['frame'] = parts[5].split(':')[1]
        details['start_codon'] = parts[6].split(':')[1]
        details['stop_codon'] = parts[7].split(':')[1]
    elif tool == 'transdecoder':
        parts = header.split(' ', 2)
        details['name'] = re.sub(r'\.p\d+$', '', parts[0])
        details['orf'] = parts[0]
        if len(parts) > 2:
            additional_info = parts[2]
            range_strand_match = re.search(r'(\d+)-(\d+)\((\+|-)\)', additional_info)
            details['start'] = range_strand_match.group(1) if range_strand_match else 'N/A'
            details['stop'] = range_strand_match.group(2) if range_strand_match else 'N/A'
            details['strand'] = range_strand_match.group(3) if range_strand_match else 'N/A'
            type_match = re.search(r'type:([^\s,]+)', additional_info)
            details['type'] = type_match.group(1) if type_match else 'N/A'
            length_match = re.search(r'len:(\d+)', additional_info)
            details['length'] = length_match.group(1) if length_match else 'N/A'
    return details

def write_results(output_file, results, tool):
    """Writes the results to a TSV file."""
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        headers = ['name', 'orf', 'start', 'stop', 'strand', 'type', 'length', 'kozak_score'] if tool == 'transdecoder' else \
                  ['name', 'orf', 'start', 'stop', 'strand', 'type', 'length', 'frame', 'start_codon', 'stop_codon', 'kozak_score']
        writer.writerow(headers)
        for result in results:
            writer.writerow(result)

def main():
    parser = argparse.ArgumentParser(description="Calculate the Kozak sequence score for given transcripts and ORFs and output to a TSV file.")
    parser.add_argument("--transcript", required=True, help="Path to the transcript multi-FASTA file")
    parser.add_argument("--orf", required=True, help="Path to the ORF multi-FASTA file")
    parser.add_argument("--output", required=True, help="Output TSV file path")
    parser.add_argument("--tool", choices=['orfipy', 'transdecoder'], required=True, help="Tool used to generate ORF file")

    args = parser.parse_args()

    transcripts, _ = read_fasta(args.transcript)
    orfs, orf_headers = read_fasta(args.orf)
    results = []

    for header, orf_seq in orfs.items():
        transcript_header = re.sub(r'\.p\d+$', '', header) if args.tool == 'transdecoder' else header
        transcript_seq = transcripts.get(transcript_header)
        if transcript_seq:
            kozak_score = calculate_kozak_score(transcript_seq, orf_seq)
            header_info = parse_header_info(orf_headers[header], args.tool)
            result = [header_info[key] for key in header_info] + [kozak_score]
            results.append(result)

    write_results(args.output, results, args.tool)
    print(f"Results written to {args.output}")

if __name__ == "__main__":
    main()
