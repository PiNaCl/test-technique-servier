# from test_resources import clinical_trials[_df, drugs_df, pubmed_df
from pandas import DataFrame as DF
from app.ops import sluggify_columns

def test_sluggify_cols():
    df = DF([["A#B", 1], ["B#A", 2]], columns=["text", "int"])
    df_res = sluggify_columns(df, ["text"])
    assert list(df_res["text_slug"]) == ["a b", "b a"]
