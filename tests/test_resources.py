import pytest
import os 
from app import dataframe_from_files

DATA_PATH = os.path.join(os.getcwd(), "data")

@pytest.fixture
def pubmed_df():
    pubmed = dataframe_from_files(
        os.path.join(DATA_PATH, "pubmed.csv"),
    )
    return pubmed


@pytest.fixture
def drugs_df():
    drugs = dataframe_from_files(
        os.path.join(DATA_PATH, "drugs.csv")
    )
    return drugs

@pytest.fixture
def clinical_trials_df():
    clinical_trials = dataframe_from_files(
        os.path.join(DATA_PATH, "clinical_trials.csv"),
    )
    return clinical_trials

def test_load_drugs(drugs_df):
    assert list(drugs_df.columns) == ["atccode","drug"]
    assert len(drugs_df) == 7

def test_load_clinical_trials(clinical_trials_df):
    assert list(clinical_trials_df.columns) == [
        "id","scientific_title","date","journal"
    ]
    assert len(clinical_trials_df) == 8

def test_load_pubmed(pubmed_df):
    assert list(pubmed_df.columns) == ["id", "title", "date", "journal"]
    assert len(pubmed_df) == 8
