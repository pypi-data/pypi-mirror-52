"""
LCA Command
============

Take the output of the **filter** command and finds the Last Common Ancestor
for each sequence in the assembly. The result of this command is 2 files with
the LCA information (lca-contigs.tsv and lca-contigs.json), in the output
directory.

Additionally, a file (lca-contigs.krona) is written. This can be passed to the
*ktImportText* script installed with Krona to produce an HTML file with a Krona
graph. Example::

    $ ktImportText -q -o lca-contigs.html lca-contigs.krona

Requirements
------------

The requirements are a taxonomy file (-t option) which takes the same taxonomy
file previously used, in addition to the GFF produced by the **filter**
command. Optionally an output directory can be specified.
"""
import os
import json
import logging

from mgkit import taxon
from mgkit.io import gff
from mgkit.io.utils import open_file

from ..ui.utils import write_manifest

LOG = logging.getLogger(__name__)


def lca_annotations(taxonomy, seq_ann):
    taxon_ids = (a.taxon_id for a in seq_ann)
    try:
        lca_id = taxon.last_common_ancestor_multiple(taxonomy, taxon_ids)
    except taxon.NoLcaFound:
        lca_id = None

    if lca_id is None:
        lineage = '',
    else:
        lineage = ';'.join(
            taxon.get_lineage(
                taxonomy,
                lca_id,
                names=True,
                with_last=True,
                only_ranked=True
            )
        )

    return lca_id, lineage


def lca_contig_command(options):
    try:
        os.mkdir(options.output_dir)
    except OSError:
        pass
        # Add exit if directory exists?

    taxonomy = taxon.UniprotTaxonomy(options.taxonomy)

    iterator = gff.parse_gff_files(options.input_file)
    iterator = gff.group_annotations_sorted(
        iterator,
        key_func=lambda x: x.seq_id
    )

    lca_dict = {}

    for seq_ann in iterator:
        lca_id, lineage = lca_annotations(taxonomy, seq_ann)

        lca_dict[seq_ann[0].seq_id] = {
            'taxon_id': lca_id,
            'lineage': lineage
        }

    json.dump(
        lca_dict,
        open(
            os.path.join(options.output_dir, 'lca-contigs.json'),
            'w'
        ),
        indent=4
    )

    csv_file = open(
        os.path.join(options.output_dir, 'lca-contigs.tsv'),
        'w'
    )

    krona_file = open(
        os.path.join(options.output_dir, 'lca-contigs.krona'),
        'w'
    )

    for seq_id, value in lca_dict.items():
        csv_file.write(
            "{seq_id}\t{taxon_id}\t{lineage}\n".format(seq_id=seq_id, **value)
        )

        if value['taxon_id'] is None:
            krona_file.write('No LCA\n')
        else:
            krona_file.write(
                "\t".join(
                    taxon.get_lineage(
                        taxonomy,
                        value['taxon_id'],
                        names=True,
                        with_last=True,
                        only_ranked=True
                    )
                ) + '\n'
            )

    write_manifest(options.output_dir)
