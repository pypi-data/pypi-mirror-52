
import pandas as pd

from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource


class FooDataSource(ToucanDataSource):
    query: str


class FooConnector(ToucanConnector):
    type = "foo"
    data_source_model: FooDataSource

    username: str
    password: str

    def get_df(self, data_source: FooDataSource) -> pd.DataFrame:
        pass
