import itertools
import logging
import seaborn
import numpy

import mgkit.plots

from .common import get_gtdb_like_taxonomy

seaborn.set_style('whitegrid')

LOG = logging.getLogger(__name__)


def group_seq_lengths(seqs, lca_dict, taxonomy, rank):
    LOG.debug("Grouping sequences lengths")
    seq_lengths = {}
    for seq_id, seq in seqs.items():
        if seq_id in lca_dict:
            taxon_id = lca_dict[seq_id]['taxon_id']
        else:
            taxon_id = None

        if taxon_id is None:
            anc_id = None
        else:
            anc_id = taxonomy.get_ranked_taxon(taxon_id, rank=rank).taxon_id

        if anc_id not in seq_lengths:
            seq_lengths[anc_id] = {}

        try:
            seq_lengths[anc_id][taxon_id].append(len(seq))
        except KeyError:
            seq_lengths[anc_id][taxon_id] = [len(seq)]

    return {
        anc_id: {
            taxon_id: numpy.array(values)
            for taxon_id, values in seq_data.items()
        }
        for anc_id, seq_data in seq_lengths.items()
    }


def lca_contig_count_and_length(seq_lengths, file_name, taxonomy, sep, fontsize=14, unknown_col='#999999'):

    LOG.info(
        "Outputting box/bar plot for contig length and abundance to (%s)",
        file_name
    )

    anc_order = sorted(
        (
            (anc_id, numpy.concatenate(list(seq_data.values())).mean())
            for anc_id, seq_data in seq_lengths.items()
        ),
        key=lambda x: x[1]
    )
    anc_order = [anc_id for anc_id, value in anc_order]
    anc_colors = {
        taxon_id: unknown_col if taxon_id is None else mgkit.plots.float_to_hex_color(*color)
        for taxon_id, color in zip(anc_order, seaborn.color_palette('hls', len(anc_order)))
    }

    plot_order = []
    for anc_id in anc_order:
        for taxon_id, lengths in seq_lengths[anc_id].items():
            plot_order.append(
                (anc_id, taxon_id)
            )

    n_rows = len(plot_order)
    fig, gs = mgkit.plots.get_grid_figure(
        1,
        2,
        figsize=(15, .25 * n_rows),
        width_ratios=[1, .75],
        wspace=.0
    )

    axb = fig.add_subplot(gs[0])

    data = [
        seq_lengths[anc_id][taxon_id]
        for anc_id, taxon_id in plot_order
    ]

    plot_data = axb.boxplot(data, vert=False, patch_artist=True, widths=0.6)

    for index, (anc_id, taxon_id) in enumerate(plot_order):
        plot_data['boxes'][index].set(
            edgecolor='black',
            facecolor=anc_colors[anc_id],
            lw=0.5
        )
        plot_data['medians'][index].set_color('black')
        plot_data['whiskers'][index].set(color='black', linestyle='--', lw=1)
        plot_data['whiskers'][index+len(plot_order)].set(
            color='black',
            linestyle='--',
            lw=1
        )
        plot_data['caps'][index].set(color='black', ls='-')

        axb.scatter(
            seq_lengths[anc_id][taxon_id],
            numpy.ones(len(seq_lengths[anc_id][taxon_id])) + index,
            color=anc_colors[anc_id],
            s=50
        )

    axb.invert_xaxis()

    axb.grid(True, which='major', axis='both')
    minor_tick = (axb.get_xticks(minor=False)[1] - axb.get_xticks(minor=False)[0]) // 2
    axb.set_xticks(
        numpy.arange(0, axb.get_xlim()[0], minor_tick),
        minor=True
    )
    axb.grid(True, which='minor', axis='both', linestyle='--')

    # _ = axb.set_xlim(right=c_df.min().min() - minor_tick)
    _ = axb.set_ylim(bottom=0, top=len(plot_order) + 0.5)

    axb.set_title('Contig Length', fontsize=fontsize)
    axb.set_xlabel('Length in bp', fontsize=fontsize)

    axc = fig.add_subplot(gs[1], sharey=axb)

    axc.barh(
        numpy.arange(1., len(plot_order) + 1., 1),
        [
            len(seq_lengths[anc_id][taxon_id])
            for anc_id, taxon_id in plot_order
        ],
        height=0.8,
        color=[anc_colors[anc_id] for anc_id, taxon_id in plot_order],
        lw=0.5
    )
    _ = axc.set_ylim(bottom=0.5, top=len(plot_order) + 0.5)

    group_labels = []
    for anc_id in anc_order:
        if anc_id is None:
            lineage = 'Unknown'
        else:
            lineage = get_gtdb_like_taxonomy(anc_id, taxonomy, sep=sep)
        group_labels.append(lineage)

    mgkit.plots.heatmap.grouped_spine(
        [seq_lengths[anc_id].keys() for anc_id in anc_order],
        group_labels,
        axc,
        start=0.5,
        spine_opts=dict(fontsize=fontsize)
    )

    axb.yaxis.set_visible(False)

    axc.set_title('Number of Contigs Assigned', fontsize=fontsize)
    axc.set_xlabel('Count', fontsize=fontsize)

    for text in axb.get_xticklabels() + axc.get_xticklabels():
        text.set_fontsize(fontsize * .75)

    fig.savefig(file_name, bbox_inches='tight')

    return anc_colors


# not used at the moment
def contig_decomposition_plot(tsf_training, tsf_unknown, seq_colors, train_alpha=0.25, fname='test-pca.pdf', include_training=True):
    fig, gs = mgkit.plots.get_grid_figure(3, 1, figsize=(7.5, 7.5 * 3))
    for gs_index, (column1, column2) in enumerate(itertools.combinations(tsf_training.columns, 2)):
        ax = fig.add_subplot(gs[gs_index])
        if include_training:
            for seq_id in tsf_training.index.get_level_values(0).unique():
                ax.plot(
                    tsf_training.loc[seq_id, column1],
                    tsf_training.loc[seq_id, column2],
                    color=seq_colors[seq_id],
                    alpha=train_alpha,
                    marker='o',
                    lw=0.75
                )
        for seq_id in tsf_unknown.index.get_level_values(0).unique():
            ax.plot(
                tsf_unknown.loc[seq_id, column1],
                tsf_unknown.loc[seq_id, column2],
                color=seq_colors[seq_id],
                alpha=1.,
                marker='o',
                lw=1.5
            )
        ax.set_xlabel(column1)
        ax.set_ylabel(column2)

        fig.savefig(fname, bbox_inches='tight')
