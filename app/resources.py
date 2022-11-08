from typing import AnyStr, List, Optional
import pandas as pd
from yaml import SafeLoader, load as yaml_load


def dataframe_from_files(
    path: AnyStr,
    fformat: Optional[AnyStr] = None,
    encoding: Optional[AnyStr] = "UTF-8",
) -> pd.DataFrame:
    """
    Load a dataframe from a path.
    Supported format are actually json and csv
    :param path: where the file is located
    """
    result = None

    if fformat == "csv" or path.lower().endswith(".csv"):
        result = pd.read_csv(path, encoding=encoding, dtype=str)

    elif fformat == "json" or path.lower().endswith(".json"):
        with open(path, encoding=encoding) as handle:
            # Yaml can load json with trailing commas :)
            result = yaml_load(handle, Loader=SafeLoader)
            result = pd.DataFrame(result)
    if "date" in result.columns:
        result["date"] = pd.to_datetime(result["date"], dayfirst=True).astype(str)
    return result
