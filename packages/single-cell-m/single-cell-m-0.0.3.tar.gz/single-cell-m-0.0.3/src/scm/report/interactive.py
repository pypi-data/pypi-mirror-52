import pandas
import logging

import bokeh
import bokeh.models
import bokeh.models.tools
from bokeh.models import HoverTool, BoxZoomTool, CustomJS
from bokeh.layouts import gridplot, column

from bokeh.resources import CDN
from bokeh.embed import file_html
import bokeh.plotting
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, TextInput, Div
from bokeh.models.sources import ColumnDataSource

import mgkit.plots
import mgkit.utils.sequence

from .common import get_gtdb_like_taxonomy


LOG = logging.getLogger(__name__)


def contig_colors(taxonomy, anc_colors, sequences, lca_dict, rank, unknown_col='#999999'):
    seq_colors = {}
    for seq_id, value in lca_dict.items():
        if value['taxon_id'] is None:
            continue
        anc_id = taxonomy.get_ranked_taxon(
            value['taxon_id'],
            rank=rank
        ).taxon_id

        try:
            seq_colors[seq_id] = anc_colors[anc_id]
        except KeyError:
            continue

    seq_colors.update(
        {
            seq_id: unknown_col
            for seq_id in set(sequences) - set(seq_colors)
        }
    )
    return seq_colors


def create_bokeh_data_source(dataframes, lca_dict, seq_colors, taxonomy, seq_ids_training, seqs, sep, contig_coverage, clustered, training_alpha=0.25):
    LOG.info("Create Bokeh Data Source")

    dataframes = pandas.concat(dataframes)
    lineages = {
        (seq_id, index): 'Unknown' if (seq_id not in lca_dict) or (lca_dict[seq_id]['taxon_id'] is None) else get_gtdb_like_taxonomy(lca_dict[seq_id]['taxon_id'], taxonomy, sep=sep)
        for seq_id, index in dataframes.index
    }
    dataframes['lineage'] = pandas.Series(lineages)
    dataframes['alpha'] = pandas.Series(
        {
            (seq_id, index): training_alpha if seq_id in seq_ids_training else 1.
            for seq_id, index in dataframes.index
        }
    )
    dataframes['target_taxon'] = pandas.Series(
        {
            (seq_id, index): seq_id in seq_ids_training
            for seq_id, index in dataframes.index
        }
    )
    dataframes['seq_id'] = pandas.Series(dataframes.index.get_level_values(0), index=dataframes.index)

    dataframes['color'] = pandas.Series(
        {
            (seq_id, index): seq_colors[seq_id]
            for seq_id, index in dataframes.index
        }
    )
    dataframes['length'] = pandas.Series(
        {
            (seq_id, index): len(seqs[seq_id])
            for seq_id, index in dataframes.index
        }
    )
    dataframes['coverage'] = pandas.Series(
        {
            (seq_id, index): contig_coverage.get(seq_id, 0)
            for seq_id, index in dataframes.index
        }
    )
    dataframes['cluster'] = pandas.Series(
        {
            (seq_id, index): clustered[seq_id]
            for seq_id, index in dataframes.index
        }
    )

    LOG.debug("Returning dataframe")

    return dataframes.sort_index(level=0).sort_values(by='target_taxon', ascending=False)


def prepare_plot(dataframes, seq_colors, seq_ids_training, title='', plot_width=400, plot_height=400, x_range=None, y_range=None, x_label='', y_label='', x_col='X', y_col='Y', datasource=None):
    LOG.info("Prepare PCA plot for %s and %s", x_col, y_col)

    if datasource is None:
        datasource = ColumnDataSource(dataframes)
    figure = bokeh.plotting.figure(
        plot_width=plot_width,
        plot_height=plot_height,
        tools=','.join(
            [
                "pan",
                "box_zoom",
                "save",
                "reset",
                "tap",
                "lasso_select",
                "box_select",
                # "resize", # doesn't work with the layout
                "wheel_zoom"
            ]
        ),
        title=title,
        x_range=x_range,
        y_range=y_range
    )

    LOG.debug("Drawing Lines")

    lines_x = []
    lines_y = []
    lines_color = []
    lines_alpha = []
    for seq_id in dataframes.index.get_level_values(0).unique():
        # Using loc[(seq_id,), x_col] triggers a PerformanceWarning from pandas
        # loc[seq_id, x_col] can't be used because the index is a MultiIndex
        lines_x.append(dataframes.loc[seq_id].loc[:, x_col].values)
        lines_y.append(dataframes.loc[seq_id].loc[:, y_col].values)
        lines_color.append(seq_colors[seq_id])
        lines_alpha.append(0.25 if seq_id in seq_ids_training else 1.)
    line_source = ColumnDataSource({'X': lines_x, 'Y': lines_y, 'color': lines_color, 'alpha': lines_alpha})
    ml = bokeh.models.MultiLine(xs='X', ys='Y', line_color='color', line_alpha='alpha')
    figure.add_glyph(source_or_glyph=line_source, glyph=ml)

    LOG.debug("Drawing Circles")

    c = bokeh.models.Circle(x=x_col, y=y_col, fill_color='color', fill_alpha=1., line_color=None, radius=1.5)
    c_render = figure.add_glyph(source_or_glyph=datasource, glyph=c)
    hover = HoverTool(
        renderers=[c_render],
        tooltips=[
            ("LCA", "@lineage"),
            ("Contig", "@seq_id"),
            ("Length", "@length"),
            ("Coverage (%)", '@coverage'),
            ("Cluster", "@cluster"),
        ]
    )
    figure.add_tools(hover)

    figure.xaxis.axis_label = x_label
    figure.yaxis.axis_label = y_label

    return figure, datasource


def output_html_pca(source, pca_plot_main, pca_plot_sub, file_name):
    LOG.info("Ouput PCA plot to %s", file_name)

    columns = [
        TableColumn(field='seq_id', title='Contig'),
        TableColumn(field='lineage', title='Lineage'),
        TableColumn(field='length', title='Length'),
        TableColumn(field='coverage', title='Coverage (%)'),
        TableColumn(field='cluster', title='Cluster'),
        TableColumn(field='target_taxon', title='Target Taxon'),
    ]
    data_table = DataTable(
        source=source,
        columns=columns,
        width=1024,
        height=600
    )

    div_change = Div(
        sizing_mode="stretch_both",
        text="",
        width=200,
        height=800
    )
    source.callback = CustomJS(args=dict(ti=div_change, dt=source), code="""
            var inds = cb_obj.selected['1d'].indices;
            var d1 = cb_obj.data;

            var contigs = [];

            for (i = 0; i < inds.length; i++){
                contigs.push(d1['seq_id'][inds[i]])
            }

            contigs = Array.from(new Set(contigs));
            contigs.sort();
            ti.text = contigs.join("<br>");
        """)

    grid_plot = gridplot(
        [[pca_plot_main], pca_plot_sub, [data_table], [div_change]],
        merge_tools=False,
        toolbar_location='left',
        sizing_mode="fixed",
    )
    # grid_plot.sizing_mode = 'scale_height'

    html = file_html(grid_plot, CDN, "PCA Contigs")

    open(file_name, 'w').write(html)


def prepare_gc_data(sequences, bins):
    LOG.info("Calculate GC content")

    gc_content = {
        seq_id: mgkit.utils.sequence.sequence_gc_content(seq) * 100
        for seq_id, seq in sequences.items()
    }
    gc_content = pandas.Series(gc_content)
    dataframe = pandas.DataFrame(
        {
            'bin': pandas.cut(gc_content, bins=bins),
            'gc_content': gc_content
        }
    ).sort_values(by='bin')

    gc_counts = dataframe.groupby(by='bin').count()
    gc_counts['bin'] = [str(x) for x in gc_counts.index]
    gc_counts['left'] = pandas.cut(gc_content, bins=bins, retbins=True)[1][:-1]
    gc_counts['avg_gc'] = dataframe.groupby(by='bin').mean()
    gc_counts['contigs'] = dataframe.groupby(by='bin').apply(
        lambda x: '<br>'.join(x.index)
    )

    gc_counts.index = range(len(gc_counts))

    return gc_counts


def output_html_gc_content(gc_counts, file_name):
    LOG.info("Ouput GC plot to %s", file_name)

    datasource = ColumnDataSource(gc_counts)

    div_change = Div(
        sizing_mode="stretch_both", text="", width=800, height=200
    )
    callback = CustomJS(
        args=dict(div=div_change, ds=datasource),
        code="""
        var indices = cb_data.index['1d'].indices;
        var div_content = [];
        var datas = ds.data;
        for (i=0; i < indices.length; i++) {
            div_content.push(datas['contigs'][indices[i]]);
        }
        div_content.sort();
        if (div_content.length > 0) {
            div.text = div_content.join("<br>");
        }
        """
    )

    hover = HoverTool(
        tooltips=[
            ('Average GC %', '@avg_gc'),
            ('Number of Contigs', '@gc_content'),
        ],
        callback=callback
    )

    figure = bokeh.plotting.figure(
        width=800,
        height=300,
        tools=','.join(
            [
                "pan",
                "box_zoom",
                "save",
                "reset",
                "tap",
                "lasso_select",
                "box_select",
                # "resize", # doesn't work with the layout
                "wheel_zoom"
            ]
        ),
    )

    width = (
        gc_counts.left[1:].values - gc_counts.left[:-1].values
    ).min() * 0.8

    figure.vbar(
        x='left',
        width=width,
        top='gc_content',
        source=datasource,
    )
    figure.xaxis.axis_label = 'GC %'
    figure.yaxis.axis_label = 'Number of Contigs'

    figure.add_tools(hover)

    grid = column(
        figure,
        div_change,
        sizing_mode='scale_width',
    )

    html = file_html(grid, CDN, "GC% Contigs")

    open(file_name, 'w').write(html)
