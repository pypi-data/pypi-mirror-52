from mobikit.config import config
from mobikit.feeds.exceptions import SourceTypeException
from mobikit.utils import token_required
from mobikit.feeds.base import FeedRef, Queryable


@token_required
def load(
    feed_id, source_name=None, query=None, source_names=None, queries=None, as_dict=True
):
    """
    Allows user to load/query any number of sources from a feed.

    If the request is very large, the result will be downsized and a warning will be issued to the user

    Parameters
    ----------
    feed_id : int
        Id of the feed whose sources you with to load. A feed consists of multiple sources.
    source_names : list of str
        List of source names to load data from.
    queries : dict
        Dict mapping source names (str) to queries (mobikit.feeds.Query).
    as_dict : boolean
        Whether the loaded dfs should be returned as dict or list.
    source_name : str
        String containing the name of a single source to query.
    query : mobikit.feeds.Query
        A query to be run on the single source specified with `source_name`.

    Returns
    -------
    dataframe(s) : pandas.DataFrame or dict or list
        If source_name is used to specify a single source to load, will return a single pandas.DataFrame.
        Otherwise, will return either a dict of the form {source_name: pandas.DataFrame}
        or a list of pandas.DataFrame, depending on the value of `as_dict`.
    """
    source_names = source_names or set()
    queries = queries or dict()
    if source_name:
        source_names.add(source_name)
        queries[source_name] = queries.get(source_name, None) or query

    feed = FeedRef.create(feed_id)
    feed.load()
    if not len(source_names):
        source_names = set(feed.sources.keys())

    source_dfs = {}
    for s in source_names:
        source_query = queries.get(s, None)
        if source_query and isinstance(feed.get_source(s), Queryable):
            feed.sources[s].query(source_query)
        elif source_query:
            raise SourceTypeException(f"{s} is not queryable.")
        else:
            feed.get_source(s).load()
        source_dfs[s] = feed.get_source(s).to_df()
    config.logger.info(f"returned {len(list(source_dfs.keys()))} dataframes")
    if source_name:
        return source_dfs[source_name]
    return source_dfs if as_dict else list(source_dfs.values())
