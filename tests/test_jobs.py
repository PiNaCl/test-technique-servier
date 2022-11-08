from app.jobs import references_graph
import os

from app.ops import most_referencing_journal 

def test_references_graph():

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

    most_citing = most_referencing_journal(result)
    assert most_citing == "Psychopharmacology"
