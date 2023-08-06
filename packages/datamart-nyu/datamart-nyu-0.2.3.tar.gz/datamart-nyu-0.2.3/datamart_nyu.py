"""Currently just redirects to datamart-rest.

Might be getting code later, running operations on the client-side.
"""

from datamart_rest import \
    RESTDatamart as NYUDatamart, \
    RESTSearchResult as NYUSearchResult, \
    RESTQueryCursor as NYUQueryCursor


__all__ = ['NYUDatamart', 'NYUSearchResult', 'NYUQueryCursor']
