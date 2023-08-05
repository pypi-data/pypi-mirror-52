from mgkit import taxon


def get_gtdb_like_taxonomy(taxon_id, taxonomy, sep=';'):
    lineage = []
    taxa = taxon.get_lineage(
        taxonomy,
        taxon_id,
        only_ranked=True,
        with_last=True
    )
    for taxon_id in taxa:
        taxon_name = taxonomy[taxon_id]
        taxon_name = "{}_{}".format(
            taxon_name.rank[0] if taxon_name.rank != 'superkingdom' else 'k',
            taxon_name.s_name
        )
        lineage.append(taxon_name)
    return sep.join(lineage)
