import os

from resources import dataframe_from_files
from ops import (
    aggregate_references,
    sluggify_columns,
    references_from_source,
    write_to_json,
    most_referencing_journal,
)


def references_graph(drugs_path, clinical_trials_path, pubmed_paths, output_path):
    """
    Job that compute the reference graph of all drugs for all clinical trials and pubmeds
    """
    # Data Loading
    drugs = dataframe_from_files(drugs_path)
        
    pubmed = [
        dataframe_from_files(file_name)
        for file_name in pubmed_paths
    ]

    clinical_trials = dataframe_from_files(
        clinical_trials_path
    )


    # Preprocessing
    drugs = sluggify_columns(drugs, ["drug"])
    clinical_trials = sluggify_columns(clinical_trials, ["scientific_title"])
    pubmed = [
        sluggify_columns(df, ["title"])
        for df in pubmed
    ]

    # computation
    clinical_references = references_from_source(
        drugs, "clinical_trials", clinical_trials, "scientific_title_slug"
    )
    
    all_pubmed_references = [
        references_from_source(
            drugs, "pubmed", pubmed_df, "title_slug"
        )
        for pubmed_df in pubmed
    ]
  
    # Aggregation
    aggregated = aggregate_references(clinical_references, *all_pubmed_references)

    # Report
    write_to_json(aggregated, output_path)
    return aggregated


if __name__ == "__main__":
    DATA_PATH = os.path.join(os.getcwd(), "data")
    result = references_graph(
        drugs_path = os.path.join(DATA_PATH, "drugs.csv"),
        clinical_trials_path=os.path.join(DATA_PATH, "clinical_trials.csv"),
        pubmed_paths=[
            os.path.join(DATA_PATH, file_name)
            for file_name in ["pubmed.csv",  "pubmed.json"]
        ],
        output_path= os.path.join(DATA_PATH, "result.json")
    )
    most_referencing_journal(result)
