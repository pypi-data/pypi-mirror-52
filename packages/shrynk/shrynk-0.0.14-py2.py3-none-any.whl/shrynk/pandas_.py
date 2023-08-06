import os
import zipfile

import numpy as np
import pandas as pd
from pyarrow import ArrowTypeError


from shrynk.compressor import BaseCompressor
from shrynk.predictor import Predictor


def safelen(x):
    try:
        return len(x)
    except TypeError:
        return 0


class PandasCompressor(Predictor, BaseCompressor):
    bench_exceptions = (
        ValueError,
        ArrowTypeError,
        pd.errors.ParserError,
        zipfile.BadZipFile,
        UnicodeDecodeError,
        OSError,
        pd.errors.EmptyDataError,
    )
    compression_options = [
        ("csv", None),
        ("csv", "gzip"),
        ("csv", "bz2"),
        ("csv", "xz"),
        ("csv", "zip"),
        # pyarrow # {‘NONE’, ‘SNAPPY’, ‘GZIP’, ‘LZO’, ‘BROTLI’, ‘LZ4’, ‘ZSTD’}
        ("pyarrow", None),
        ("pyarrow", "snappy"),
        ("pyarrow", "gzip"),
        ("pyarrow", "brotli"),
        ("fastparquet", "GZIP"),
        ("fastparquet", "UNCOMPRESSED"),
        ("fastparquet", "BROTLI"),
        ("fastparquet", "LZ4"),
        ("fastparquet", "LZO"),
        # # # # # # ("fastparquet", "ZSTANDARD"),
        # fastparquet can do per column
        # pip install fastparquet[brotli]
        # pip install fastparquet[lz4]
        # pip install fastparquet[lzo]
        # pip install fastparquet[zstandard]
        # ("fastparquet", {str(x): "BROTLI" if x % 2 == 1 else "GZIP" for x in range(5)})
    ]

    def infer(self, file_path):
        endings = file_path.split(".")[-2:]
        engine = None
        compression = None
        for eng, comp in self.compression_options:
            if eng in endings:
                engine = eng
            if comp in endings:
                compression = comp
        if engine is None and "parquet" in endings:
            engine = "auto"
        return engine, compression

    def save(self, df, file_path_prefix, engine=None, compression=None):
        path = os.path.join(file_path_prefix, "shrynk.{}.{}".format(engine, compression))
        if engine is None or engine == "csv":
            df.to_csv(path)
        else:
            df.columns = [str(x) for x in df.columns]
            df.to_parquet(path, engine=engine, compression=compression)
        return path

    def load(self, file_path, engine=None, compression=None):
        if engine is None or engine == "csv":
            data = pd.read_csv(file_path)
        else:
            data = pd.read_parquet(file_path, engine=engine)
        return data

    def get_features(self, df):
        num_cols = df.shape[1]
        num_obs = df.shape[0]
        float_cols = [c for c, d in zip(df.columns, df.dtypes) if "float" in str(d)]
        str_cols = [c for c, d in zip(df.columns, df.dtypes) if "object" in str(d)]
        if str_cols and not df[str_cols].empty:
            str_len_quantiles = list(
                df[str_cols].applymap(safelen).quantile([0.25, 0.50, 0.75], axis=0).mean(axis=1)
            )
            str_missing_proportion = (~df[str_cols].notnull()).mean().mean()
        else:
            str_len_quantiles = [np.nan, np.nan, np.nan]
            str_missing_proportion = np.nan
        if float_cols and not df[float_cols].empty:
            float_equal_0 = (df[float_cols] == 0).mean().mean()
            float_missing_proportion = (~df[str_cols].notnull()).mean().mean()
        else:
            float_equal_0 = np.nan
            float_missing_proportion = np.nan
        cardinality = df.apply(pd.Series.nunique)
        cardinality_quantile_proportion = cardinality.quantile([0.25, 0.50, 0.75]) / num_obs
        data = {
            # standard
            "num_obs": num_obs,
            "num_cols": num_cols,
            "num_float_vars": len(float_cols),
            "num_str_vars": len(str_cols),
            "percent_float": len(float_cols) / num_cols,
            "percent_str": len(str_cols) / num_cols,
            "str_missing_proportion": str_missing_proportion,
            "float_missing_proportion": float_missing_proportion,
            "cardinality_quantile_proportion_25": cardinality_quantile_proportion.iloc[0],
            "cardinality_quantile_proportion_50": cardinality_quantile_proportion.iloc[1],
            "cardinality_quantile_proportion_75": cardinality_quantile_proportion.iloc[2],
            # extra cpu
            "float_equal_0_proportion": float_equal_0,
            "str_len_quantile_25": str_len_quantiles[0],
            "str_len_quantile_50": str_len_quantiles[1],
            "str_len_quantile_75": str_len_quantiles[2],
        }
        return data

    def is_valid(self, df):
        if df.shape[1] < 2:
            return None
        if df.empty:
            return None
        return df
