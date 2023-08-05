"""
Blast Filter Command
====================

This commmand will filter output(s) from BLAST, used with the option
*-outfmt 6*, which outputs a tab delimited file. The result of this command is
a GFF file (blast-hits.gff) with the filtered hits in the output directory.
Additionally, 2 more files are produced with the bp covered in annotations:

    * contig-cov.json
    * contig-cov.tsv

The first is used with the *report* command if contigs with a low coverage of
of annotations (-c and -r options there). The second contains is a tab
separated file with 3 columns:

    * contig header
    * contig length
    * coverage

Options/Requirements
--------------------

Requirements
************

Besides the output file(s) from BLAST, the script requires a taxonomy file and
another that contains the mappings from the database IDs to the taxonomic IDs.

The taxonomy can be obtained using the `MGKit`_ script **download-taxonomy.sh**,
which is installed as a requirement by this package, preferably using::

    $ download-taxonomy.sh taxonomy.msgpack

Passing the **.msgpack** extension results in a different format, which is
faster to load than the default one, while the rest of the name can be changed.
This is passed to the script via the **-t** option, wihch is required.

The second file that is required is the mapping of database IDs to taxonomic
IDs. This file is dependent on the database used with BLAST and by default
the headers are expected to be in EMBL/NCBI format, with elements separated by
pipe ("|") characters. `MGKit`_ provides 3 different scripts for downloading
such information, in a way that can be used by this command.

Two scipts, *download-uniprot-taxa.sh* and *download-ncbi-taxa.sh* download the
necessary files, from Uniprot and NCBI respectively, while the third,
*taxon-utils* process the files from the previous comamnds to a HDF5 file, that
is required by this command.

...

Which will download the mappings from NCBI *nt* to taxonomic IDs and can be
passed to the **-a** option of this command.

Another requirement is the FASTA file with the assembly, which is used to
filter contigs whose hits cover less than the specified percentage of the
contig's length (disabled by default).

Optional
********

Several parameter are set to default value that can be changed to suit
different type of analysis. A brief summary:

* -o output directory to store files
* -d type of DB used, which defaults to NCBI blast DBs, in particular

    * ncbi (default): NCBI blast DBs download from NCBI, contains only the
        versioned ID
    * uniprot: a '|' separated header, used by Uniprot
    * other: the entire header is used as ID for the taxonomy
    * ncbi-full: similar to *uniprot*, but specific to NCBI

* -i identity quantile to use for filtering sequences, default to 97% of the
    sequence identity distribution
* -f Fasta file with the sequences used
* -a HDF5 file, followed by a colon and the table to be used, (e.g.
    taxa.hdf:uniprot)
* -e minimum E-value to accept a BLAST hit
* -x exclude viral hits from analysis
* -c minimum coverage
* -m maximum number of hits to use for each contig

The minimum coverage options (-c) is used to exclude contigs where the hits from
BLAST (after filtering) cover less than a certain threshold. The default
behaviour is to keep all contigs.

ORF Filter and LCA
==================

Another command, **orf** allows to get the last common ancestor (LCA) of genes
called using prodigal. This gives more information on the accuracy of the LCA
call on the contigs. Most parameters are the same as the **filter** command.

Files produced:

    * orf-hits.gff
    * orf-hits.tsv

The GFF file contains the LCA information for each gene and the coordinates it
was called on. The same information is available in the TSV file.

Links
=====

.. _MGKit: https://bitbucket.org/setsuna80/mgkit
"""

from __future__ import division

import os
import itertools
import functools
import logging
import json

import pandas
import progressbar

from mgkit import taxon
from mgkit.io import blast, gff, fasta, fastq
from mgkit.io.utils import group_tuples_by_key, open_file
from mgkit.filter import gff as filter_gff
from mgkit.utils.dictionary import HDFDict
from mgkit.utils.common import ranges_length

from ..lca.command import lca_annotations
from ..ui.utils import write_manifest

LOG = logging.getLogger(__name__)


def filter_sequence(iterator, id_quantile, evalue):

    for annotations in iterator:
        annotations = [
            annotation
            for annotation in annotations
            if annotation.get_attr('evalue', float) < evalue
        ]
        identity_threshold = pandas.Series(
            annotation.get_attr('identity', float) for annotation in annotations
        ).quantile(id_quantile)

        yield [
            annotation
            for annotation in annotations
            if annotation.get_attr('identity', float) >= identity_threshold
        ]


def add_taxa_ids(iterator, taxa_dict, taxonomy, name_func, exclude_virus, max_hits=100, no_taxa_filter=False):

    iterator = blast.parse_blast_tab(
        iterator,
        ret_col=(0, 1, 2, 6, 7, 8, 9, 10, 11),
        value_funcs = (
            str,
            name_func,
            float,
            int,
            int,
            int,
            int,
            float,
            float
        )
    )

    iterator = group_tuples_by_key(
        (seq_hit for key, seq_hit in iterator),
        key_func=lambda x: x[0]
    )

    try:
        taxa_dict = HDFDict(taxa_dict[0], taxa_dict[1])
    except ValueError as e:
        utils.exit_script(
            str(e),
            7
        )

    include_taxa = (
        taxon.CELLULAR_ORGANISMS,
        taxon.VIRUS
    )
    if exclude_virus:
        include_taxa = include_taxa[0]

    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

    for seq_hits in bar(iterator):
        if len(seq_hits) > max_hits:
            seq_hits = seq_hits[:max_hits]

        annotations = []

        for seq_hit in seq_hits:
            try:
                gene_id = seq_hit[1]
            except IndexError:
                LOG.critical('Cannot find gene_id')
                continue

            try:
                taxon_id = taxa_dict[gene_id]
            except KeyError:
                LOG.debug("No taxon_id found for gene_id (%s)", gene_id)
                continue

            if (not no_taxa_filter) and (not taxonomy.is_ancestor(taxon_id, include_taxa)):
                continue

            annotation = gff.from_nuc_blast(
                seq_hit,
                'TEST',
                feat_type='HIT',
                taxon_id=taxon_id,
            )

            annotations.append(annotation)

        yield annotations


def get_choose_func():
    choose_func = lambda a1, a2: min(
        a1,
        a2,
        key=lambda el: tuple(
            [
                el.get_attr('identity', float),
                el.bitscore,
                len(el)
            ]
        )
    )

    choose_func = functools.partial(
        filter_gff.choose_annotation,
        overlap=100,
        choose_func=choose_func
    )

    return choose_func


def filter_overlap(iterator, gff_file, min_cov, sequences):

    choose_func = get_choose_func()

    contig_coverage = {}

    for annotations in iterator:

        annotations = gff.group_annotations(
            annotations,
            key_func=lambda x: (x.seq_id, x.strand)
        ).values()

        filtered_annotations = []

        for strand_annotations in annotations:
            filtered = filter_gff.filter_annotations(
                strand_annotations,
                choose_func=choose_func,
                sort_func=lambda x: x.bitscore,
                reverse=True
            )

            filtered_annotations.extend(filtered)

        # Needed if no annotations are kept, the following
        # filtered_annotations[0].seq_id
        # raises an IndexError exception
        if not filtered_annotations:
            continue

        # Calculate the coverage in percentage of the length
        coverage = ranges_length(
            gff.elongate_annotations(filtered_annotations)
        ) / sequences[filtered_annotations[0].seq_id] * 100

        contig_coverage[filtered_annotations[0].seq_id] = coverage

        # Check if minimum coverage is satisfied
        if coverage < min_cov:
            continue

        for annotation in filtered_annotations:
            annotation.to_file(gff_file)

    for seq_id in set(sequences) - set(contig_coverage):
        contig_coverage[seq_id] = 0.

    return contig_coverage


def blast_filter_command(options):

    try:
        os.mkdir(options.output_dir)
    except OSError:
        pass
        # Add exit if directory exists?

    if options.db_type == 'ncbi-full':
        name_func = lambda x: x.split('|')[3].split('.')[0]
    elif options.db_type == 'uniprot':
        name_func = lambda x: x.split('|')[1]
    elif options.db_type == 'other':
        name_func = lambda x: x
    elif options.db_type == 'ncbi':
        name_func = lambda x: x.split('.')[0]

    taxonomy = taxon.UniprotTaxonomy(options.taxonomy)

    if options.no_taxa_filter:
        LOG.info('No taxa will be filtered')

    gff_file = open_file(
        os.path.join(options.output_dir, 'blast-hits.gff'),
        'w'
    )

    LOG.info("Minimum contig coverage required %d%%", options.coverage)

    iterator = itertools.chain(*options.input_file)
    iterator = add_taxa_ids(
        iterator,
        options.table,
        taxonomy,
        name_func,
        options.exclude_virus,
        max_hits=options.max_hits,
        no_taxa_filter=options.no_taxa_filter
    )
    iterator = filter_sequence(
        iterator,
        options.identity,
        options.evalue
    )
    load_sequences_func = fastq.load_fastq_rename if options.fastq else fasta.load_fasta_rename
    sequences = {
        # The third argument in the tuple is only present if a FASTQ file is
        # used
        sequence[0]: len(sequence[1])
        for sequence in load_sequences_func(options.sequences)
    }
    contig_coverage = filter_overlap(iterator, gff_file, options.coverage, sequences)

    json.dump(
        contig_coverage,
        open(os.path.join(options.output_dir, 'contig-cov.json'), 'w')
    )

    with open(os.path.join(options.output_dir, 'contig-cov.tsv'), 'w') as f:
        for seq_id, cov in contig_coverage.items():
            f.write("{}\t{}\t{}\n".format(seq_id, sequences[seq_id], cov))

    write_manifest(options.output_dir)

def group_prodigal_aa(file_handle):
    return {
        d['prod_seq_id']: d
        for d in fasta.load_fasta_prodigal(file_handle)
    }


def orf_filter_command(options):

    try:
        os.mkdir(options.output_dir)
    except OSError:
        pass
        # Add exit if directory exists?

    if options.db_type == 'ncbi':
        name_func = lambda x: x.split('|')[3].split('.')[0]
    elif options.db_type == 'uniprot':
        name_func = lambda x: x.split('|')[1]
    elif options.db_type == 'other':
        name_func = lambda x: x

    taxonomy = taxon.UniprotTaxonomy(options.taxonomy)

    gff_file = open_file(
        os.path.join(options.output_dir, 'orf-hits.gff'),
        'w'
    )
    LOG.info("Writing a GFF file to (%s)", gff_file.name)

    tsv_file = open_file(
        os.path.join(options.output_dir, 'orf-hits.tsv'),
        'w'
    )

    LOG.info("Writing LCA information to (%s)", tsv_file.name)

    iterator = itertools.chain(*options.input_file)
    iterator = add_taxa_ids(
        iterator,
        options.table,
        taxonomy,
        options.exclude_virus
    )
    iterator = filter_sequence(
        iterator,
        options.identity,
        name_func,
        options.evalue
    )

    aa_seqs = group_prodigal_aa(options.sequences)

    tsv_file.write('seq_id\tindex\tlineage\tstart\tend\tstrand\ttaxon_id\tbest_hit\tgene_ids\n')

    for annotations in iterator:
        if not annotations:
            continue
        lca_id, lineage = lca_annotations(taxonomy, annotations)
        prod_seq_id = annotations[0].seq_id

        info = aa_seqs[prod_seq_id]

        tsv_file.write(
            '{seq_id}\t{idx}\t{lineage}\t{start}\t{end}\t{strand}\t{taxon_id}\t{best_hit}\t{gene_ids}\n'.format(
                taxon_id=lca_id,
                lineage=lineage,
                gene_ids=','.join(
                    set(annotation.gene_id for annotation in annotations)
                ),
                best_hit=max(annotations, key=lambda x: x.bitscore).gene_id,
                **info
            )
        )

        gff.Annotation(
            source='PRODIGAL',
            feat_type='CDS',
            taxon_id=lca_id,
            lineage=lineage,
            gene_ids=','.join(
                set(annotation.gene_id for annotation in annotations)
            ),
            best_hit=max(annotations, key=lambda x: x.bitscore).gene_id,
            **info
        ).to_file(gff_file)

    write_manifest(options.output_dir)
