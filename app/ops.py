import json
from typing import AnyStr, Dict

from utils import sluggify


def sluggify_columns(df, columns):
    for column in columns:
        df[column + "_slug"] = df[column].apply(sluggify, args=" ")
    return df


def references_from_source(drugs, source_name, mention_source, title_column):
    drugs = sluggify_columns(drugs, ["drug"])
    references = {}
    for drug in drugs["drug_slug"]:
        mentions = mention_source[title_column].str.contains(drug)
        records = mention_source[mentions].to_dict(orient="records")
        references[drug] = {source_name: records, "journal": []}

        for record in records:
            references[drug]["journal"].append(
                {"journal": record["journal"], "date": record["date"]}
            )
    return references


def aggregate_references(*references):
    """
    Iterate over all the references

    A reference is a dict containing drugs 
    each drug contains differents mentions from differents source type as a key
    and records as values
    
    concatenate all the records according to the source key
    """
    result = {}
    for reference in references:
        for drug, records_source in reference.items():
            for record_type, records in records_source.items():
                result[drug] = result.get(drug, {})
                result[drug][record_type] = result[drug].get(record_type, [])
                result[drug][record_type].extend(records)
    return result


def write_to_json(item, path):
    """
    Utility to write to file
    Could be modified to export to a remote location
    """
    with open(path, "w") as handle:
        json.dump(item, handle, indent=4)


def most_referencing_journal(drug_graph: Dict) -> AnyStr:
    """
    Compute most referencing journal from the output of 
    the `references_graph`job

    """
    journals = {}
    most_citing = None
    max_citation = 0
    for graph in drug_graph.values():
        seen = set()
        for journal in graph["journal"]:
            name = journal["journal"]
            if name in seen:
                continue
            seen.add(name)
            journals[name] = journals.get(name, 0)
            journals[name] += 1
            if max_citation < journals[name]:
                max_citation = journals[name]
                most_citing = name
    return most_citing
