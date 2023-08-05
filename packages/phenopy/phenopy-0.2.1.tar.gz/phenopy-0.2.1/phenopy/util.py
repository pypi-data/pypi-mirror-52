import csv
import sys
import networkx as nx
import pandas as pd


def export_pheno2genes_with_no_parents(pheno2genes_file, pheno2genes_no_parents_file, hpo_network, logger=None):
    """
    Load HPO terms associated to genes as annotated in https://hpo.jax.org/app/download/annotation.
    Filter the parent terms for each gene.
    Dump pheno2genes_no_parents_file

    :param pheno2genes_file: Phenotypes to genes file.
    :param pheno2genes_no_parents_file: Phenotypes to genes file with parents removed.
    :param hpo_network: The HPO networkx object.
    :param logger: Python `logging` logger instance.
    :return: None
    """
    try:
        df = pd.read_csv(
            pheno2genes_file,
            comment='#',
            names=['hpo_id', 'hpo_name', 'gene_id', 'gene_name'],
            sep='\t',
        )
    except (FileNotFoundError, PermissionError) as e:
        if logger is not None:
            logger.critical(e)
        else:
            sys.stderr.write(str(e))
        exit(1)

    no_parents_df = df.copy()
    for gene, annotations in df.groupby('gene_name'):
        termlist = [node for node in annotations['hpo_id'].tolist() if node in hpo_network.nodes()]
        termlist = remove_parents(termlist, hpo_network)
        parent_idx = annotations.loc[~annotations['hpo_id'].isin(termlist)].index
        no_parents_df.drop(parent_idx, inplace=True)

    try:
        no_parents_df.to_csv(pheno2genes_no_parents_file,
                             header=['#hpo_id', 'hpo_name', 'gene_id', 'gene_name'],
                             sep='\t',
                             index=False)
    except PermissionError as e:
        if logger is not None:
            logger.critical(e)
        else:
            sys.stderr.write(str(e))
        exit(1)


def read_records_file(records_file, no_parents, hpo_network, logger=None):
    try:
        # read records_file
        with open(records_file) as records_fh:
            reader = csv.reader(records_fh, delimiter='\t')
            records = {}
            for line in reader:
                if line[0].startswith('#'):
                    continue
                if no_parents is True:
                    records[line[0]] = remove_parents(line[1].split('|'), hpo_network)
                else:
                    records[line[0]] = line[1].split('|')
        return records
    except (FileNotFoundError, PermissionError) as e:
        logger.critical(e)
        raise e


def remove_parents(termlist, hpo_network):
    """remove parents from termlist
    :param termlist: List of HPO terms.
    :param hpo_network: The HPO networkx object.
    """
    terms_to_remove = set()
    for source_term in termlist:
        if source_term not in hpo_network.nodes:
            terms_to_remove.add(source_term)
            continue
        for target_term in termlist:
            if target_term not in hpo_network.nodes:
                terms_to_remove.add(target_term)
                continue
            # has_path will evaluate True for a term to itself, include additional check
            same_terms = source_term == target_term
            source_to_target = nx.has_path(hpo_network, source_term, target_term)
            target_to_source = nx.has_path(hpo_network, target_term, source_term)
            if source_to_target is True and not same_terms:
                terms_to_remove.add(target_term)
            if target_to_source is True and not same_terms:
                terms_to_remove.add(source_term)
    return set(termlist) - terms_to_remove
