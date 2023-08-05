"""
Report Command
==============

The command will output a figure and a HMTL file with a plot/table that can be
used to inspect the kmer counts on a series of windows for each contig.

Options/Requirements
--------------------

Required
********

* taxonomy file (-t option), same in other commands
* assembly file (-f option), FASTA file with the contigs
* LCA JSON file (-l option) from the **lca** commnad

The taxonomy file is the same requirement for commands run earlier in the
pipeline, while the assembly file is the same file that was used to make the
BLAST ouput used with the **filter** command. It is expected to be a FASTA file.

The LCA (last common ancestor) file is the output of the **lca** command, and
is a JSON file that contains the information about is needed to direct the
target taxon assignment.

Optional
********

* taxonomic rank used to group the taxa by colour (-g option)
* contig coverage JSON file (-r option), from the *filter* command
* lineage separator (-s option)
* options for the kmer counting
* number of bins for the GC content histogram
* exclude contigs from analysis
* exclude contigs based on their annotation coverage
* target Taxon, either a name (e.g. bacteria, escherichia) or ID from NCBI taxonomy

The rank (defaults to *genus*) is used to colour groups of taxa, so can they be
visually identified. The ranks are the ones accepted in the taxonomy (e.g.
family, order, phylum, etc.).

The lineage separator is the character(s) used to separate the taxa the lineage
consists of. It's used in all outputs from this command.

The options for kmer counting change the behaviour of the plot by setting the
window size (-w option, defaults to 5000), step (-s option, defaults to 500),
and kmer length (-k option, defaults to 5). Lower window sizes and steps make
the contigs appear more similar, while a greater kmer size make the computation
more memory demanding. Usually a value of 4 or 5 is used, with 9 requiring
much more memory. Moreover, any contig whose length is less than the window
size specified will be excluded from the analysis.

It is also possible to exclude some contigs (-x option) from the computation by
passing a text file with the headers to exclude, as copied from the HTML report,
with one header per line.

Another option is to exclude contigs with a coverage less than the chosen
threshold (-c option, values from 0 to 100).

The target taxon is based on `NCBI taxonomy <https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?db=Taxonomy>`_
and all the taxa below the target one are then marked as target. For example if
the target taxon is set to "escherichia", all species that belong to that genus
will be marked as meeting the target. It can be specified as either a name (-n
option) or as a ID (numeric, -i option). The name is not accepted if the name
is not unique in the taxonomy, in which case the script exit. Valid target taxa
are high level ones like *bacteria*, *archaea* or *viruses*.

A target taxon is automatically chosen by getting a taxon that contains at
least half of all the sequences identified (via LCA). The percentage value can
be modified by using the *-e* option, passing a value between 0 and 100, but
very high or low numbers should be avoided.

The file *contig-cov.json* (produced by the **filter** command) needs to be
passed (-r option) and it's used to put information in *PCA* plot.

HTML Reports
------------

The HTML (file **pca-plot.html**) report contains a PCA plot of the first 2
dimentions, using the contigs that are within the target taxon as training set.
The plot is linked to the a sortable table below it, which can be also be used
to select points in the plot (alternative to using the lasso selection). Any
contigs selected in the plot or table will be written appear under the table,
so it can be copied in a file (for example if in a further analysis they must
be excluded). Moreover, the colours of the lines/dots are the same as the other
plot (a PDF file) that is in the same directory.

Another HTML file is produced (**gc-plot.html**) that contains an histogram of
the GC content of the contigs analysed. When hovering over one of the bars,
some information is displayed as tooltip and the headers of the contigs
included in that bin is displayed in a section underneat the histogram.
"""
from __future__ import division

import os
import logging
import json
from collections import Counter

import pandas
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift
import distance

from mgkit.workflow.utils import exit_script
from mgkit.io import fasta, fastq
from mgkit import taxon
from mgkit.utils import sequence

from . import static
from . import interactive
from ..ui.utils import write_manifest

LOG = logging.getLogger(__name__)


def training_sets(sequences, lca_dict, taxonomy, target_taxon):
    seq_ids_training = list(
        seq_id
        for seq_id in sequences
        if (seq_id in lca_dict) and taxonomy.is_ancestor(
            lca_dict[seq_id]['taxon_id'], int(target_taxon)
        )
    )

    seq_ids_unknown = list(
        set(sequences) - set(seq_ids_training)
    )

    return seq_ids_training, seq_ids_unknown


def kmer_counting(sequences, kmer_size, window_size, step):
    LOG.info(
        "Kmer counting (kmer %i, window %i, step %i) for %i sequences",
        kmer_size,
        window_size,
        step,
        len(sequences)
    )

    matrix = sequence.signatures_matrix(
        sequences.items(),
        k_size=kmer_size,
        w_size=window_size,
        step=step
    )

    matrix.sort_index(level=0, inplace=True)

    return matrix


def pca_transform(matrix, seq_ids_training, seq_ids_unknown):

    LOG.info("Performing PCA transform")

    pca = PCA(n_components=3, whiten=False)

    pca.fit(matrix.loc[seq_ids_training])

    tsf_training = pandas.DataFrame(
        pca.transform(matrix.loc[seq_ids_training]),
        index=matrix.loc[seq_ids_training].index,
        columns=['X', 'Y', 'Z']
    )
    if len(seq_ids_unknown) > 0:
        tsf_unknown = pandas.DataFrame(
            pca.transform(matrix.loc[seq_ids_unknown]),
            index=matrix.loc[seq_ids_unknown].index,
            columns=['X', 'Y', 'Z']
        )
    else:
        LOG.warning(
            "The unknown set contains no contigs. All fall within the " +
            "specified target"
        )
        tsf_unknown = None

    LOG.info("Explained variance %r", pca.explained_variance_ratio_ * 100)

    return tsf_training, tsf_unknown, pca.explained_variance_ratio_ * 100


def ms_cluster(matrix):

    LOG.info("Performing MeanShift clustering")

    pca = PCA(n_components=3, whiten=False)

    centroids = matrix.groupby(level=0).mean()

    transformed = pca.fit_transform(centroids)

    ms = MeanShift()

    return dict(
        zip(
            centroids.index,
            ms.fit_predict(transformed),
        )
    )


def count_sequences(lca_dict, taxonomy, rank):
    counts = Counter(
        d['taxon_id'] if rank is None else taxonomy.get_ranked_taxon(d['taxon_id'], rank).taxon_id
        for seq_id, d in lca_dict.items()
        if d['taxon_id'] is not None
    )
    counts = pandas.Series(counts).sort_values(ascending=False)
    return counts.divide(counts.sum()) * 100


def find_target_taxon(lca_dict, taxonomy, threshold=50.):
    LOG.info("Finding target taxon (>= %.2f of contigs)", threshold)
    counts = count_sequences(lca_dict, taxonomy, None)
    if counts.iloc[0] >= threshold:
        return counts.index[0]

    for rank in reversed(taxon.TAXON_RANKS):
        counts = count_sequences(lca_dict, taxonomy, rank)
        if counts.iloc[0] >= threshold:
            return counts.index[0]


def report_command(options):
    try:
        os.mkdir(options.output_dir)
    except OSError:
        pass
        # Add exit if directory exists?

    try:
        contig_coverage = json.load(options.coverage_file)
    except (ValueError, AttributeError):
        if options.min_cov is not None:
            exit_script(
                "To use the coverage filter you need to pass the " +
                "coverage file (JSON)", 5
            )
        else:
            contig_coverage = {}

    taxonomy = taxon.UniprotTaxonomy(options.taxonomy)

    lca_dict = json.load(options.lca_json)

    if (options.target_taxon_id is None) and (options.target_taxon_name is not None):
        try:
            target_taxon = taxonomy.find_by_name(options.target_taxon_name)
        except KeyError:
            names = sorted(
                distance.ifast_comp(
                    options.target_taxon_name,
                    (x.s_name for x in taxonomy)
                )
            )[:10]
            exit_script(
                "Taxon name '{}' not found, possible alternatives: {}".format(
                    options.target_taxon_name,
                    ', '.join(x[1] for x in names)
                ),
                1
            )
        if len(target_taxon) > 1:
            exit_script(
                "Taxon name '{}' has multiple taxa ID".format(
                    options.target_taxon_name
                ),
                2
            )
        target_taxon = target_taxon[0]
    elif (options.target_taxon_id is not None) and (options.target_taxon_name is None):
        if options.target_taxon_id not in taxonomy:
            exit_script(
                "Taxon ID '{}' was not found in the Taxonomy".format(
                    options.target_taxon_id
                ),
                3
            )
        target_taxon = options.target_taxon_id
    else:
        target_taxon = find_target_taxon(
            lca_dict,
            taxonomy,
            options.target_threshold
        )

    LOG.info(
        "The target taxon is '%s' (rank '%s')",
        taxonomy[target_taxon].s_name,
        taxonomy[target_taxon].rank
    )

    if options.exclude_seq is None:
        exclude_seqs = set()
    else:
        exclude_seqs = set(
            line.strip()
            for line in options.exclude_seq
        )

    if options.min_cov is not None:
        LOG.info(
            "Accepting only contigs with %.2f%% of coverage",
            options.min_cov
        )
        for seq_id, cov in contig_coverage.items():
            if cov < options.min_cov:
                exclude_seqs.add(seq_id)

    load_sequences_func = fastq.load_fastq_rename if options.fastq else fasta.load_fasta_rename
    sequences = dict(
        sequence[:2]
        for sequence in load_sequences_func(options.sequences)
        if (len(sequence[1]) >= options.window_size) and (sequence[0] not in exclude_seqs)
    )

    if len(sequences) < 2:
        exit_script(
            "Not enough ({}) sequences could be loaded (min {} in length)".format(
                len(sequences),
                options.window_size
            ),
            6
        )

    seq_lengths = static.group_seq_lengths(
        sequences,
        lca_dict,
        taxonomy,
        options.rank
    )

    anc_colors = static.lca_contig_count_and_length(
        seq_lengths,
        os.path.join(options.output_dir, 'length-abundance-figure.pdf'),
        taxonomy,
        options.lineage_separator,
        fontsize=14
    )

    # Interactive plot

    seq_colors = interactive.contig_colors(
        taxonomy,
        anc_colors,
        sequences,
        lca_dict,
        rank=options.rank
    )

    seq_ids_training, seq_ids_unknown = training_sets(
        sequences,
        lca_dict,
        taxonomy,
        target_taxon
    )

    if len(seq_ids_training) == 0:
        exit_script(
            "The training set contains no contigs: a higher taxon should " +
            "be used as target", 4
        )

    matrix = kmer_counting(
        sequences,
        options.kmer_size,
        options.window_size,
        options.step
    )

    tsf_training, tsf_unknown, explained_variance = pca_transform(
        matrix,
        seq_ids_training,
        seq_ids_unknown
    )

    clustered = ms_cluster(matrix)

    dataframes = interactive.create_bokeh_data_source(
        [tsf_training] if tsf_unknown is None else [tsf_training, tsf_unknown],
        lca_dict,
        seq_colors,
        taxonomy,
        seq_ids_training,
        sequences,
        options.lineage_separator,
        contig_coverage,
        clustered
    )

    dataframes.to_csv(
        os.path.join(options.output_dir, 'pca_data.csv')
    )

    pca_plot_x_y, source = interactive.prepare_plot(
        dataframes,
        seq_colors,
        seq_ids_training,
        title='Components 1 and 2',
        plot_height=1024,
        plot_width=1024,
        x_label='PCA 1 ({:.2f}%)'.format(explained_variance[0]),
        y_label='PCA 2 ({:.2f}%)'.format(explained_variance[1]),
        x_col='X',
        y_col='Y',
    )
    pca_plot_x_z, source = interactive.prepare_plot(
        dataframes,
        seq_colors,
        seq_ids_training,
        title='Components 1 and 3',
        plot_height=1024 // 2,
        plot_width=1024 // 2,
        x_label='PCA 1 ({:.2f}%)'.format(explained_variance[0]),
        y_label='PCA 3 ({:.2f}%)'.format(explained_variance[2]),
        x_col='X',
        y_col='Z',
        datasource=source,
        x_range=pca_plot_x_y.x_range
    )
    pca_plot_y_z, source = interactive.prepare_plot(
        dataframes,
        seq_colors,
        seq_ids_training,
        title='Components 2 and 3',
        plot_height=1024 // 2,
        plot_width=1024 // 2,
        x_label='PCA 2 ({:.2f}%)'.format(explained_variance[1]),
        y_label='PCA 3 ({:.2f}%)'.format(explained_variance[2]),
        x_col='Y',
        y_col='Z',
        datasource=source,
        x_range=pca_plot_x_y.y_range,
        y_range=pca_plot_x_z.y_range
    )

    pca_plot_x_y.x_range = pca_plot_x_z.x_range
    pca_plot_x_y.y_range = pca_plot_y_z.x_range
    pca_plot_x_z.y_range = pca_plot_x_z.y_range

    interactive.output_html_pca(
        source,
        pca_plot_x_y,
        [pca_plot_x_z, pca_plot_y_z],
        os.path.join(options.output_dir, 'pca-plot.html')
    )

    gc_counts = interactive.prepare_gc_data(
        sequences,
        options.bins
    )

    interactive.output_html_gc_content(
        gc_counts,
        os.path.join(options.output_dir, 'gc-plot.html')
    )

    write_manifest(options.output_dir)
