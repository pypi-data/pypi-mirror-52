"""
Workflow Command
================

This command prepares a bash script that can be used to run in succession the
commands necessary to perform the analysis, from the sequence file (FASTA or
FASTQ) to the final report. The options used for each command are the mostly
conservative or the default ones and they should be customised for better
performance and analysis. If the templates here don't fit your workflow, it is
still a good idea to generate a similar one and customise the resulting bash
script.

The command produces 3 different templates based on the type of database (DB)
chosen and the software to seach for similarity between DB and sequences
provided. The DBs supported with this command are NCBI (*nt* and *nr*) and
Uniprot. The supported software is *blastn* (for NCBI *nt*), *blastx* (for NCBI
*nr*) and diamond (for Uniprot).

Options/Requirements
--------------------

Requirements
************

The script requires, besides the sequence file to analyse, a BLAST/Diamond DB
and the file containing the ID->Taxon table and a taxonomy file.

Obtain a DB
^^^^^^^^^^^

To obtain a copy of NCBI BLAST DBs, you can download all files from `NCBI FTP`_:

    * files starting with **nr** for proteins (used *blastx*)
    * files starting with **nt** for nucleotides (use *blastn*)

The files should be compressed (ending with .gz) and after using `gunzip` they
can be used. The files ending with .md5 are used to check the download was
correct.

To obtain a copy of Uniprot DBs, you need to download them at `Uniprot`_, and
there is both reviewed and unreviewed DBs:

* Reviewed: ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
* Unreviewed: ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz

The DBs are in FASTA format and need to be indexed with `Diamond`_, for example::

    $ diamond makedb --in uniprot_sprot.fasta.gz -d swissprot

Will index the reviewed Uniprot DB and make an index file called swissprot.dmnd.

If you need to combine the 2 databases and index them, you can use a command
like this (in bash shell)::

    $ diamond makedb --in <(gunzip -c uniprot_sprot.fasta.gz uniprot_trembl.fasta.gz) -d uniprot

This command will create an index file called uniprot.dmnd that contains both
DBs.

Obtain the ID->Taxon file
^^^^^^^^^^^^^^^^^^^^^^^^^

You can get the correct file by runnig the included script `scm-download-taxa.sh`.
To get the correct file, you pass:

* *nucl* to get the NCBI *nt* references
* *prot* to get the NCBI *nr* references
* *uniprot* to get the Uniprot (both Reviewed and Unreviewed) references

For example, to download the NCBI *nt* references, you can run::

    $ scm-download-taxa.sh nucl

A file (HDF5 format) called *taxa-tables.hdf* will be created and it will
contain a *ncbi-nucl* table.

Taxonomy file
^^^^^^^^^^^^^

To downlad the taxonomy file, you can run the script::

    $ download-taxonomy.sh

That will create a file called *taxonomy.pickle* and this is included in MGKit,
which is installed along this package.

Options
*******

positional arguments:
  sequence_files        Sequence files to process

optional arguments:
  -h, --help            show this help message and exit
  -d DB, --db DB        DB to be used with blastn/blastx/diamond
  -b {ncbi-nucl,uniprot,ncbi-prot}, --db-type {ncbi-nucl,uniprot,ncbi-prot}
                        DB used, ncbi-* assumes a NCBI BLAST index, for
                        Uniprot Diamond will be used if the DB ends in .dmnd
  -a TABLE, --table TABLE
                        HDF5 file with gene_id to taxon_id table
  --table-name TABLE_NAME
                        HDF5 table inside the file, defaults to --db-type
  -t TAXONOMY, --taxonomy TAXONOMY
                        Taxonomy file
  -w, --overwrite       If passed, overwrites the content of the output
                        directories while the default is to skip existing
                        directories
  -s SUFFIX, --suffix SUFFIX
                        Suffix to add to the fasta file name (after removing
                        its extension and adding a hyphen) as the output
                        directory
  --log LOG             File to log messages
  -q, --fastq           The sequences are in FASTQ format
  -v, --verbose         more verbose - includes debug messages
  --quiet               less verbose - only error and critical messages
  --manual              Show the script manual
  --version             show program's version number and exit


Links
=====

.. _NCBI FTP: ftp://ftp.ncbi.nlm.nih.gov/blast/db/
.. _Diamond: https://github.com/bbuchfink/diamond
.. _Uniprot: https://www.uniprot.org/downloads
"""

import logging
import os.path
import sys
from glob import glob
from datetime import datetime
import json

import pandas
from mgkit.workflow.utils import exit_script

from .. import VERSION

LOG = logging.getLogger(__name__)


def get_sequence_similarity_cmd(seq_file, db_type, db, output_file, fastq):

    if db_type == 'ncbi-nucl':
        prog_name = 'blastn'
    elif db_type == 'ncbi-prot':
        prog_name == 'blastx'
    else:
        if db.endswith('.dmnd'):
            prog_name = 'diamond blastx'
        else:
            prog_name = 'blastx'

    if prog_name.startswith('blast'):
        cmd_line = '{prog_name} -query {seq_file} -db {db} -outfmt 6 -out {output_file}'
        if seq_file.endswith('.gz'):
            seq_file = '<(gunzip -c {})'.format(seq_file)
    else:
        cmd_line = '# tested on diamond v.9.9\n{prog_name} -q {seq_file} -d {db} -f 6 -o {output_file}'
        if not fastq:
            cmd_line += ' --more-sensitive'

    return '# Sequence similarity search\n' + cmd_line.format(
        prog_name=prog_name,
        db=db,
        output_file=output_file,
        seq_file=seq_file
    )


def get_filter_cmd(seq_file, db_type, taxonomy, taxa_table, output_dir, tab_file,
                    script_name, fastq, db_table):

    db_type = 'ncbi' if db_type.startswith('ncbi') else 'uniprot'

    if fastq:
        more = '-m 3 -q'
    else:
        more = ''

    cmd_line = '{script_name} filter -o {output_dir} -t {taxonomy} -d {db_type} -f {seq_file} -a {taxa_table}:{db_table} {more} {tab_file}'

    return '# Similarity search filtering\n' + cmd_line.format(
        script_name=script_name,
        taxonomy=taxonomy,
        db_type=db_type,
        seq_file=seq_file,
        taxa_table=taxa_table,
        output_dir=output_dir,
        db_table=db_table,
        tab_file=tab_file,
        more=more
    )


def get_lca_cmd(gff_file, output_dir, taxonomy, script_name):
    cmd_line = '{script_name} lca -t {taxonomy} -o {output_dir} {gff_file}'

    return '# LCA processing\n' + cmd_line.format(
        script_name=script_name,
        output_dir=output_dir,
        gff_file=gff_file,
        taxonomy=taxonomy
    )


def get_report_cmd(script_name, taxonomy, output_dir, seq_file, lca_file, cov_file, fastq):
    cmd_line = "{script_name} report -t {taxonomy} -o {output_dir} -f {seq_file} -l {lca_file} -r {cov_file}"
    if fastq:
        cmd_line += '-q'

    return '# Report generation\n' + cmd_line.format(
        script_name=script_name,
        taxonomy=taxonomy,
        output_dir=output_dir,
        seq_file=seq_file,
        lca_file=lca_file,
        cov_file=cov_file
    )


def test_blast_db(db, db_prefix, db_exts):

    db_path, db_name = os.path.split(db)
    db_files = glob(os.path.join(db_path, '{}*'.format(db_prefix)))

    if not db_name.startswith(db_prefix):
        LOG.warning("The DB passed doesn't look like a DB from NCBI")

    if set(db_file.split('.')[-1] for db_file in db_files) != db_exts:
        exit_script("The DB passed doesn't contain a recognisable DB", 8)

    return os.path.join(db_path, db_prefix)


def workflow_command(options):

    nt_exts = {'nal', 'nhd', 'nhi', 'nhr', 'nin', 'nnd', 'nni', 'nog', 'nsd', 'nsi',
                'nsq'}

    nr_exts = {'pal', 'phd', 'phi', 'phr', 'pin', 'pnd', 'pni', 'pog', 'ppd', 'ppi',
                'psd', 'psi', 'psq'}

    script_name = os.path.basename(sys.argv[0])

    # If the file name of the DB indicates that it's a diamond DB, switches to
    # using uniprot as DB type
    if options.db.endswith('.dmnd'):
        options.db_type = 'uniprot'

    # can be overid by passing the --table-name
    if options.db_type.startswith('ncbi-') and (options.table_name is None):
        # implies a BLAST DB, can be checked for consistency, to a point
        db_path = test_blast_db(
            options.db,
            'nt' if options.db_type.endswith('nucl') else 'nr',
            nt_exts if options.db_type.endswith('nucl') else nr_exts,
        )
    else:
        # too many possible cases, trusts the user to pass the correct one
        db_path = options.db

    # Tries to find the taxonomy file, exit the script otherwise
    if not os.path.exists(options.taxonomy):
        exit_script(
            'Cannot find a taxonomy file, check the file name or run the following command: download-taxonomy.sh {}'.format(options.taxonomy),
            9
        )

    # Tests the HDF5 file, suggesting the command relative to the DB used, if
    # not found
    if not os.path.exists(options.table):
        exit_script(
            'Cannot find the HDF5 table file, run the following command: scm-download-taxa.sh {}'.format(options.db_type.split('-')[-1]),
            10
        )
    #
    if options.table_name is not None:
        table_name = options.table_name
    else:
        table_name = options.db_type
    with pandas.HDFStore(options.table, mode='r') as hdf_file:
        if '/{}'.format(table_name) not in hdf_file.keys():
            exit_script(
                'Cannot find table "{}" in HDF5 file {}'.format(table_name, options.table),
                7
            )

    for sequence_file in options.sequence_files:
        sequence_file = sequence_file.name
        output_dir = "{}-{}".format(
            os.path.basename(os.path.splitext(sequence_file)[0]),
            options.suffix,
        )
        try:
            os.mkdir(output_dir)
        except OSError:
            # Skips existing directories
            if not options.overwrite:
                LOG.warning(
                    "Output directory %s for file %s exists, skipping it (pass -w if you want to overwrite it)",
                    output_dir,
                    sequence_file,
                )
                continue
        tab_file = os.path.join(
            output_dir,
            'blast-hits.tab'
        )

        commands = [
            '#!/bin/bash',
            '# Automatically generated by "{}" version {} on {}'.format(
                script_name,
                VERSION,
                datetime.now()
            )
        ]

        similarity_cmd = get_sequence_similarity_cmd(
            sequence_file,
            options.db_type,
            db_path,
            tab_file,
            options.fastq
        )
        commands.append(similarity_cmd)

        filter_cmd = get_filter_cmd(
            sequence_file,
            options.db_type,
            options.taxonomy,
            options.table,
            output_dir,
            tab_file,
            script_name,
            options.fastq,
            table_name
        )
        commands.append(filter_cmd)

        lca_cmd = get_lca_cmd(
            os.path.join(output_dir, 'blast-hits.gff'),
            output_dir,
            options.taxonomy,
            script_name
        )
        commands.append(lca_cmd)

        report_cmd = get_report_cmd(
            script_name,
            options.taxonomy,
            output_dir,
            sequence_file,
            os.path.join(output_dir, 'lca-contigs.json'),
            os.path.join(output_dir, 'contig-cov.json'),
            options.fastq
        )
        commands.append(report_cmd)

        with open(output_dir + '.bash', 'w') as output_file:
            output_file.write('\n\n'.join(commands))
            output_file.write('\n')
