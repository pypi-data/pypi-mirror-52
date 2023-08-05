"""
Single Cell M
=============

The script is split into 3 commands:

* filter
* lca
* report

Which are supposed to be run in that order, since the output of **filter** is
used by **lca** and so on. However, they can be run in a out of order fashion
to experiment with different options to refine the analysis.

A separate command called *orf* can be used to report the Last Common Ancestor
for Open Read Frame (ORF) called used Prodigal.

Requirements
------------

The script is intended to be used on an already assembled single cell sample,
on which a BLAST (blastn/blastx/tblastx) or Diamond (blastx) similarity search
was performed. The output from BLAST is filtered (*filter*), the LCA (*lca*)
for each contig is searched and finally a series of reports and figures
(*report*) is produced, which directs the analysis of the sample for
contaminations and unwanted genetic material.

Exit Codes
----------

* 1 - Taxon name was not found
* 2 - Taxon name has more than 1 ID
* 3 - Taxon ID was not found in the Taxonomy
* 4 - The training set (PCA) has no contigs
* 5 - The coverage file could not be loaded
* 6 - Not enough sequences (less than 2) can be loaded.
* 7 - The taxa table was not found in the HDF5 file supplied
* 8 - Fails the DB tests on the *wf* command
* 9 - The taxonomy file cannot be found
* 10 - The HDF5 table file can't be found
"""
from __future__ import division
import sys
import argparse
import logging
import matplotlib

# Necessary before another backend may be selected
matplotlib.use('Agg')

import mgkit
import mgkit.taxon

from . import lca
from . import blast_filter
from . import workflow
from . import report
from .ui.utils import basic_ui_options

LOG = logging.getLogger(__name__)


def set_common_parser(parser):
    parser.add_argument(
        '-t',
        '--taxonomy',
        action='store',
        type=str,
        default=None,
        required=True,
        help='Taxonomy file',
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        action='store',
        default='report-output',
        help='Output directory',
    )
    parser.add_argument(
        '--log',
        action='store',
        default=None,
        help='File to log messages',
    )


def set_report_parser(parser):
    set_common_parser(parser)
    parser.add_argument(
        '-f',
        '--sequences',
        action='store',
        type=argparse.FileType('rb'),
        required=True,
        help='Fasta file',
    )
    target_taxon = parser.add_mutually_exclusive_group(required=False)
    target_taxon.add_argument(
        '-i',
        '--target-taxon-id',
        action='store',
        type=int,
        default=None,
        required=False,
        help='Target Taxon ID',
    )
    target_taxon.add_argument(
        '-n',
        '--target-taxon-name',
        action='store',
        type=str,
        default=None,
        required=False,
        help='Target Taxon name',
    )
    parser.add_argument(
        '-e',
        '--target-threshold',
        action='store',
        type=float,
        default=50.,
        required=False,
        help='Percentage of sequences to find the target taxon (0 to 100)'
    )
    parser.add_argument(
        '-l',
        '--lca-json',
        action='store',
        type=argparse.FileType('r'),
        default=None,
        required=True,
        help='LCA json file from the *lca* command',
    )
    parser.add_argument(
        '-g',
        '--rank',
        action='store',
        choices=mgkit.taxon.TAXON_RANKS,
        default='genus',
        required=False,
        help='Taxonomic rank to group taxa',
    )
    parser.add_argument(
        '-p',
        '--lineage-separator',
        action='store',
        type=str,
        default=';',
        required=False,
        help='Separator for elements of the lineage',
    )
    parser.add_argument(
        '-w',
        '--window-size',
        action='store',
        type=int,
        default=5000,
        required=False,
        help='Window size for kmer counting'
    )
    parser.add_argument(
        '-s',
        '--step',
        action='store',
        type=int,
        default=500,
        required=False,
        help='Step for kmer counting'
    )
    parser.add_argument(
        '-k',
        '--kmer-size',
        action='store',
        type=int,
        default=5,
        required=False,
        help='kmer counting size'
    )
    parser.add_argument(
        '-b',
        '--bins',
        action='store',
        type=int,
        default=20,
        required=False,
        help='Number of bins for the GC plot'
    )
    parser.add_argument(
        '-x',
        '--exclude-seq',
        action='store',
        type=argparse.FileType('rb'),
        default=None,
        required=False,
        help='Contigs to exclude from the analysis (one per line)'
    )
    parser.add_argument(
        '-r',
        '--coverage-file',
        action='store',
        type=argparse.FileType('r'),
        default=None,
        # required=True,
        help='Contig coverage file (JSON)'
    )
    parser.add_argument(
        '-c',
        '--min-cov',
        action='store',
        type=float,
        default=None,
        required=False,
        help='Minimum annotation coverage to keep the sequence, requires *-r*'
    )
    parser.add_argument(
        '-q',
        '--fastq',
        action='store_true',
        default=False,
        help='The sequences are in FASTQ format',
    )
    parser.add_argument(
        'input_file',
        nargs='*',
        help='Filtered GFF(s)',
        type=argparse.FileType('rb'),
        default=sys.stdin
    )
    parser.set_defaults(func=report.report_command)


def set_lca_contig_parser(parser):
    set_common_parser(parser)
    parser.add_argument(
        'input_file',
        nargs='*',
        help='Filtered GFF(s)',
        type=argparse.FileType('rb'),
        default=sys.stdin
    )
    parser.set_defaults(func=lca.lca_contig_command)


def parse_hdf5_arg(argument):
    file_name, table = argument.strip().split(':')
    return (file_name, table)


def set_filter_options(parser):
    parser.add_argument(
        '-d',
        '--db-type',
        action='store',
        type=str,
        default='ncbi',
        choices=('ncbi', 'uniprot', 'other', 'ncbi-full'),
        help='DB Used - *ncbi* refers to both *nt* and *nr*',
    )
    parser.add_argument(
        '-i',
        '--identity',
        action='store',
        type=float,
        default=.97,
        help='Quantile to keep out of all hits',
    )
    parser.add_argument(
        '-f',
        '--sequences',
        action='store',
        type=argparse.FileType('rb'),
        required=True,
        help='Fasta file',
    )
    parser.add_argument(
        '-e',
        '--evalue',
        action='store',
        type=float,
        default=.01,
        help='Only hits with an evalue lower than this will be kept (if found)',
    )
    parser.add_argument(
        '-a',
        '--table',
        action='store',
        type=parse_hdf5_arg,
        default=None,
        required=True,
        help='HDF5 file with gene_id to taxon_id table (e.g. taxa-table.hf5:ncbi-nucl)',
    )
    parser.add_argument(
        '-x',
        '--exclude-virus',
        action='store_true',
        default=False,
        help='Exclude hits on viruses',
    )
    parser.add_argument(
        '-r',
        '--no-taxa-filter',
        action='store_true',
        default=False,
        help='No taxa filter based on Cellular Organisms or Viruses',
    )
    parser.add_argument(
        '-q',
        '--fastq',
        action='store_true',
        default=False,
        help='The sequences are in FASTQ format',
    )
    parser.add_argument(
        '-m',
        '--max-hits',
        action='store',
        default=100,
        help='Maximum number of hits to use per contig (defaults to 100)',
    )


def set_orf_parser(parser):
    set_common_parser(parser)
    set_filter_options(parser)
    parser.add_argument(
        'input_file',
        nargs='*',
        help='Blast output(s)',
        type=argparse.FileType('rb'),
        default=sys.stdin
    )
    parser.set_defaults(func=blast_filter.orf_filter_command)


def set_filter_blast(parser):
    set_common_parser(parser)
    set_filter_options(parser)
    parser.add_argument(
        '-c',
        '--coverage',
        action='store',
        type=float,
        default=0.,
        help='Minimum percentage of the contig that needs to be covered',
    )
    parser.add_argument(
        'input_file',
        nargs='*',
        help='Blast output(s)',
        type=argparse.FileType('rb'),
        default=sys.stdin
    )
    parser.set_defaults(func=blast_filter.blast_filter_command)


def set_wf_parser(parser):

    # Blast/Diamond options
    parser.add_argument(
        '-d',
        '--db',
        action='store',
        type=str,
        default=None,
        required=True,
        help='DB to be used with blastn/blastx/diamond',
    )
    # Filter options
    parser.add_argument(
        '-b',
        '--db-type',
        action='store',
        type=str,
        default='ncbi-nucl',
        choices=('ncbi-nucl', 'uniprot', 'ncbi-prot'),
        help='''DB used, ncbi-* assumes a NCBI BLAST index, for Uniprot
            Diamond will be used if the DB ends in .dmnd''',
    )
    parser.add_argument(
        '-a',
        '--table',
        action='store',
        type=str,
        default=None,
        required=True,
        help='HDF5 file with gene_id to taxon_id table',
    )
    parser.add_argument(
        '--table-name',
        action='store',
        type=str,
        default=None,
        help='HDF5 table inside the file, defaults to --db-type',
    )
    # Other
    parser.add_argument(
        '-t',
        '--taxonomy',
        action='store',
        type=str,
        default=None,
        required=True,
        help='Taxonomy file',
    )
    parser.add_argument(
        '-w',
        '--overwrite',
        action='store_true',
        default=False,
        help='''If passed, overwrites the content of the output directories
            while the default is to skip existing directories'''
    )
    parser.add_argument(
        '-s',
        '--suffix',
        default='output',
        action='store',
        type=str,
        help="""Suffix to add to the fasta file name (after removing its
            extension and adding a hyphen) as the output directory"""
    )
    parser.add_argument(
        '--log',
        action='store',
        default=None,
        help='File to log messages',
    )
    parser.add_argument(
        '-q',
        '--fastq',
        action='store_true',
        default=False,
        help='The sequences are in FASTQ format',
    )
    parser.add_argument(
        'sequence_files',
        action='store',
        type=argparse.FileType('rb'),
        nargs='+',
        help='Sequence files to process'
    )

    parser.set_defaults(func=workflow.workflow_command)


def set_parser():
    """
    Sets command line arguments parser
    """
    parser = argparse.ArgumentParser(
        description='Single Cell-M',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers()

    # Batch file creation
    parser_wf_contig = subparsers.add_parser(
        'wf',
        help='Makes a batch file to executes all commands'
    )
    set_wf_parser(parser_wf_contig)
    basic_ui_options(parser_wf_contig, manual=workflow.command.__doc__)

    # LCA
    parser_lca_contig = subparsers.add_parser(
        'lca',
        help='Produces a Last Common Ancestor table'
    )

    set_lca_contig_parser(parser_lca_contig)
    basic_ui_options(parser_lca_contig, manual=lca.command.__doc__)

    # Filter Blast/Diamond Output
    parser_filter_blast = subparsers.add_parser(
        'filter',
        help='Filters BLAST hits'
    )

    set_filter_blast(parser_filter_blast)
    basic_ui_options(parser_filter_blast, manual=blast_filter.command.__doc__)

    # Report
    parser_report = subparsers.add_parser(
        'report',
        help='Produces HTML reports and figures'
    )

    set_report_parser(parser_report)
    basic_ui_options(parser_report, manual=report.command.__doc__)

    # Filter prodigal aa
    parser_orf_filter = subparsers.add_parser(
        'orf',
        help='Filters BLAST hits from Open Reading Frames'
    )

    set_orf_parser(parser_orf_filter)
    basic_ui_options(parser_orf_filter, manual=blast_filter.command.__doc__)

    # for the main command
    basic_ui_options(parser, manual=__doc__)

    return parser


def main():
    "Main function"

    options = set_parser().parse_args()

    if options.log is not None:
        mgkit.logger.config_log_to_file(
            level=logging.DEBUG,
            output=options.log
        )

    mgkit.logger.config_log(options.verbose)

    # Set the minimum level of messages, but the console messages will be only
    # at the value in options.verbose
    logging.getLogger().setLevel(logging.DEBUG)

    options.func(options)
