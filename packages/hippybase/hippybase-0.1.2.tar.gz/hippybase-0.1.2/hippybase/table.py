"""
HippyBase table module.
"""

from collections import deque


class Table:
    """
    HBase table abstraction class.

    This class cannot be instantiated directly; use `Connection.table` instead.
    """

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection

    def __repr__(self):
        return '<%s.%s name=%r>' % (
            __name__,
            self.__class__.__name__,
            self.name,
        )

    def families(self):
        """
        Retrieve the column families for this table.

        Returns
        -------
        list[str]
            List of column families.
        None
            The table does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        schema = self.connection.client.get_table_schema(self.name)
        if not schema:
            return None
        return [col['name'] for col in schema['columns']]

    def row(self, row_key, columns=None, timestamp=None, include_timestamp=False):
        """
        Retrieve a single row of data.

        Parameters
        ----------
        row_key : str
            The row key.
        columns : list, optional
            List of columns to fetch, by default None
        timestamp : int, optional
            Timestamp, by default None
        include_timestamp : bool, optional
            Whether timestamps are returned, by default False

        Returns
        -------
        dict[str, str]
            Mapping of columns to values.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        return self.connection.client.get_row(self.name, row_key, columns, timestamp, include_timestamp)

    def put(self, row_key, row_data, timestamp=None):
        """
        Store data in the table.

        This method stores the data in the `row_data` argument for the row
        specified by `row`. The `row_data` argument is dictionary that maps columns
        to values. Column names must include a family and qualifier part, e.g.
        ``b'cf:col'``, though the qualifier part may be the empty string, e.g.
        ``b'cf:'``.

        Parameters
        ----------
        row_key : str
            The row key.
        row_data : dict[str, str]
            The data to store.
        timestamp : int, optional
            Timestamp, by default None

        Returns
        -------
        True
            The data is stored.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        return self.connection.client.put_row(self.name, row_key, row_data, timestamp)

    def delete(self, row_key):
        """
        Delete data from the table.

        This method deletes all columns for the row specified by `row_key`.

        Parameters
        ----------
        row_key : str
            The row key.

        Returns
        -------
        True
            The data is deleted.
        False
            The data does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        return self.connection.client.delete_row(self.name, row_key)

    def scan(self,
             start_row=None,
             end_row=None,
             columns=None,
             cell_batch=None,
             start_time=None,
             end_time=None,
             filter_string=None,
             caching=None,
             row_batch=None,
             include_timestamp=False):
        """
        Scan the table.

        This method returns an iterable that can be used for looping over the matching rows.

        Parameters
        ----------
        table_name : str
            Name of the table.
        start_row : str, optional
            Start row key, by default None
        end_row : str, optional
            End row key, by default None
        columns : list, optional
            List of columns to fetch, by default None
        cell_batch : int, optional
            The maximum number of cells to return for each iteration, by default None
        start_time : int, optional
            Start timestamp, by default None
        end_time : int, optional
            End_timestamp, by default None
        filter_string : str, optional
            A filter string, by default None
        caching : int, optional
            Scanner caching, by default None
        row_batch : int
            The maximum number of rows to return in each REST request, by default None
        include_timestamp : bool, optional
            Whether timestamps are returned, by default False

        Returns
        -------
        _TableScanner
            _TableScanner object.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        RuntimeError
            The table does not exist.
        """
        scanner_loc = self.connection.client.create_scanner(
            table_name=self.name,
            start_row=start_row,
            end_row=end_row,
            columns=columns,
            cell_batch=cell_batch,
            start_time=start_time,
            end_time=end_time,
            filter_string=filter_string,
            caching=caching
        )
        if scanner_loc:
            return _TableScanner(self, scanner_loc, row_batch, include_timestamp)
        raise RuntimeError("The table '%s' does not exist." % self.name)


class _TableScanner:
    def __init__(self, table, scanner_loc, row_batch=None, include_timestamp=False):
        self._client = table.connection.client
        self._scanner_loc = scanner_loc
        self._row_batch = row_batch
        self._include_timestamp = include_timestamp
        self._buffer = deque()

    def __del__(self):
        self._close()

    def _close(self):
        if self._scanner_loc:
            self._client.delete_scanner(self._scanner_loc)
            self._scanner_loc = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self._buffer:
            batch = self._client.iter_scanner(self._scanner_loc, self._row_batch, self._include_timestamp)
            if not batch:
                self._close()
                raise StopIteration()
            self._buffer.extend(batch)
        return self._buffer.popleft()
