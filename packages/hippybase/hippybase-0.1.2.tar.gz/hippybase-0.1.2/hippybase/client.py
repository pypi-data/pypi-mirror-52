"""
HippyBase client module.
"""

import requests
from . import schema_pb2

OK = 200
CREATED = 201
NO_CONTENT = 204
FORBIDDEN = 403
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500


def _make_row(cell_list, include_timestamp):
    """
    Make a row dict for a cell mapping
    """
    return {
        cell.column.decode(): (cell.data.decode(), cell.timestamp) if include_timestamp else cell.data.decode()
        for cell in cell_list
    }


class HbaseServerError(RuntimeError):
    """
    Hbase Server returns errors.
    """

    def __init__(self, code=None, msg=None):
        text = ''
        if code:
            text += 'Return Code: %d' % code
        if msg:
            text += '\n%s' % msg
        super().__init__(text)


class Client:
    """
    REST Client object.

    Parameters
    ----------
    host : str
        Hostname or IP address.
    port : int
        Port number.
    """

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._base_url = 'http://%s:%d' % (host, port)
        self._session = requests.Session()

    def ping(self):
        response = self._session.head(self._base_url)
        status_code = response.status_code
        return status_code == OK

    def get_version(self):
        """
        Retrieve the Hbase software version.

        Returns
        -------
        dict[str]
            Hbase software version

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.get(
            url='/'.join((self._base_url, 'version')),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            version = schema_pb2.Version()
            version.ParseFromString(response.content)
            return {
                'rest_version': version.restVersion,
                'jvm_version': version.jvmVersion,
                'os_version': version.osVersion,
                'server_version': version.serverVersion,
                'jersey_version': version.jerseyVersion
            }
        raise HbaseServerError(code, response.text)

    def get_namespaces(self):
        """
        List all namespaces.

        Returns
        -------
        list[str]
            List of all namespace names.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.get(
            url='/'.join((self._base_url, 'namespaces')),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            namespaces = schema_pb2.Namespaces()
            namespaces.ParseFromString(response.content)
            return namespaces.namespace
        raise HbaseServerError(code, response.text)

    def get_namespace(self, namespace):
        """
        Retrieve a specific namespace.

        Parameters
        ----------
        namespace : str
            Name of the namespace.

        Returns
        -------
        dict
            Descriptions of the namespace.
        None
            The namespace does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.get(
            url='/'.join((self._base_url, 'namespaces', namespace)),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            namespace_properties = schema_pb2.NamespaceProperties()
            namespace_properties.ParseFromString(response.content)
            return {
                prop.key: prop.value
                for prop in namespace_properties.props
            }
        if code in (NOT_FOUND, INTERNAL_SERVER_ERROR):
            return None
        raise HbaseServerError(code, response.text)

    def create_namespace(self, namespace, props=None):
        """
        Create a new namespace.

        Parameters
        ----------
        namespace : str
            Name of the namespace.
        props : dict, optional
            Properties of the namespace, by default None

        Returns
        -------
        True
            The Namespace is created.
        False
            The Namespace already exists.

        Raises
        ------
        TypeError
            The type of props is not 'dict'.
        HbaseServerError
            Server returns other errors.
        """
        namespace_properties = schema_pb2.NamespaceProperties()
        if props:
            if not isinstance(props, dict):
                raise TypeError("props: expect 'dict', get '%s'." % type(props).__name__)
            for key, value in props.items():
                prop = namespace_properties.props.add()
                prop.key = key
                prop.value = value
        response = self._session.post(
            url='/'.join((self._base_url, 'namespaces', namespace)),
            headers={
                'Accept': 'application/x-protobuf',
                'Content-Type': 'application/x-protobuf'
            },
            data=namespace_properties.SerializeToString()
        )
        code = response.status_code
        if code == CREATED:
            return True
        if code == FORBIDDEN:
            # namespace already exists
            return False
        raise HbaseServerError(code, response.text)

    def delete_namespace(self, namespace):
        """
        Delete a namespace.

        Parameters
        ----------
        namespace : str
            Name of the namespace.

        Returns
        -------
        True
            The namespace is deleted.
        False
            The namespace does not exists.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.delete(
            url='/'.join((self._base_url, 'namespaces', namespace)),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            return True
        if code == NOT_FOUND:
            # namespace does not exists
            return False
        raise HbaseServerError(code, response.text)

    def get_tables(self, namespace=None):
        """
        List all nonsystem tables if namespace is None.
        Otherwise, list all tables in a specific namespace.

        Parameters
        ----------
        namespace : str, optional
            Name of the namespace, by default None

        Returns
        -------
        list[str]
            List of all table names.
        None
            The namespace does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        if namespace is None:
            response = self._session.get(
                url=self._base_url,
                headers={
                    'Accept': 'application/x-protobuf'
                }
            )
            code = response.status_code
            if code == OK:
                table_list = schema_pb2.TableList()
                table_list.ParseFromString(response.content)
                return table_list.name
            raise HbaseServerError(code, response.text)

        response = self._session.get(
            url='/'.join((self._base_url, 'namespaces', namespace, 'tables')),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            table_list = schema_pb2.TableList()
            table_list.ParseFromString(response.content)
            return table_list.name
        if code in (NOT_FOUND, INTERNAL_SERVER_ERROR):
            return None
        raise HbaseServerError(code, response.text)

    def get_table_schema(self, table_name):
        """
        Retrieve the schema of the specified table.

        Parameters
        ----------
        table_name : str
            Name of the table.

        Returns
        -------
        dict
            Schema of the table.
        None
            The table does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.get(
            url='/'.join((self._base_url, table_name, 'schema')),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            table_schema = schema_pb2.TableSchema()
            table_schema.ParseFromString(response.content)
            return {
                'name': table_schema.name,
                'columns': [
                    {
                        'name': column.name,
                        'ttl': column.ttl,
                        'max_versions': column.maxVersions,
                        'compression': column.compression,
                        'attrs': {
                            attr.name: attr.value
                            for attr in column.attrs
                        }
                    }
                    for column in table_schema.columns
                ],
                'in_memory': table_schema.inMemory,
                'read_only': table_schema.readOnly,
                'attrs': {
                    attr.name: attr.value
                    for attr in table_schema.attrs
                }
            }
        if code in (NOT_FOUND, INTERNAL_SERVER_ERROR):
            return None
        raise HbaseServerError(code, response.text)

    def create_table(self, table_name, families):
        """
        Create a new table, or replace an existing table's schema with the provided schema.

        The `families` argument is a dictionary mapping column family
        names to a dictionary containing the options for this column
        family, e.g.
        ::
            families = {
                'cf1': dict(max_versions=10),
                'cf2': dict(max_versions=1, compression=False),
                'cf3': dict(),  # use defaults
            }
            connection.create_table('mytable', families)

        The following options are supported:
        * ``ttl`` (`int`)
        * ``max_versions`` (`int`)
        * ``compression`` (`str`)

        Parameters
        ----------
        table_name : str
            Name of the table.
        families : dict[str, dict]
            The name and options for each column family.

        Returns
        -------
        True
            Table is created.
        False
            Table already exists and is updated.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        table_schema = schema_pb2.TableSchema()
        table_schema.name = table_name
        for cf_name, options in families.items():
            column = table_schema.columns.add()
            column.name = cf_name
            if 'ttl' in options:
                column.ttl = options.pop('ttl')
            if 'max_versions' in options:
                column.maxVersions = options.pop('max_versions')
            if 'compression' in options:
                column.compression = options.pop('compression')
            for name, value in options.items():
                attr = column.attrs.add()
                attr.name = str(name).upper()
                attr.value = str(value).upper()

        response = self._session.post(
            url='/'.join((self._base_url, table_name, 'schema')),
            headers={
                'Accept': 'application/x-protobuf',
                'Content-Type': 'application/x-protobuf',
            },
            data=table_schema.SerializeToString()
        )
        code = response.status_code
        if code == CREATED:
            return True
        if code == OK:
            # table already exists
            return False
        raise HbaseServerError(code, response.text)

    def delete_table(self, table_name):
        """
        Delete the table.

        Parameters
        ----------
        table_name : str
            Name of the table.

        Returns
        -------
        True
            The table is deleted.
        False
            The table does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.delete(
            url='/'.join((self._base_url, table_name, 'schema')),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            return True
        if code == NOT_FOUND:
            # table does not exists
            return False
        raise HbaseServerError(code, response.text)

    def get_row(self, table_name, row_key, columns=None, timestamp=None, include_timestamp=False):
        """
        Retrieve a single row of data.

        Parameters
        ----------
        table_name : str
            Name of the table.
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
        url = '/'.join((self._base_url, table_name, row_key))
        if columns:
            url += '/' + ','.join(columns)
        if timestamp:
            url += '/' + timestamp + ',' + (timestamp + 1)
        response = self._session.get(
            url=url,
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            cell_set = schema_pb2.CellSet()
            cell_set.ParseFromString(response.content)
            rows = cell_set.rows
            if not rows:
                return {}
            return _make_row(rows[0].values, include_timestamp)
        if code == NOT_FOUND:
            return {}
        raise HbaseServerError(code, response.text)

    def put_row(self, table_name, row_key, row_data, timestamp=None):
        """
        Store data in the table.

        This method stores the data in the `row_data` argument for the row
        specified by `row`. The `row_data` argument is dictionary that maps columns
        to values. Column names must include a family and qualifier part, e.g.
        ``b'cf:col'``, though the qualifier part may be the empty string, e.g.
        ``b'cf:'``.

        Parameters
        ----------
        table_name : str
            Name of the table.
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
        cell_set = schema_pb2.CellSet()
        row = cell_set.rows.add()
        row.key = row_key.encode()
        for column, data in row_data.items():
            cell = row.values.add()
            cell.column = column.encode()
            cell.data = data.encode()
            if timestamp:
                cell.timestamp = timestamp

        response = self._session.put(
            url='/'.join((self._base_url, table_name, 'false_row')),
            headers={
                'Accept': 'application/x-protobuf',
                'Content-Type': 'application/x-protobuf',
            },
            data=cell_set.SerializeToString()
        )
        code = response.status_code
        if code == OK:
            return True
        raise HbaseServerError(code, response.text)

    def delete_row(self, table_name, row_key):
        """
        Delete data from the table.

        This method deletes all columns for the row specified by `row_key`.

        Parameters
        ----------
        table_name : str
            Name of the table.
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
        response = self._session.delete(
            url='/'.join((self._base_url, table_name, row_key)),
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            return True
        if code == NOT_FOUND:
            return False
        raise HbaseServerError(code, response.text)

    def create_scanner(self,
                       table_name,
                       start_row=None,
                       end_row=None,
                       columns=None,
                       cell_batch=None,
                       start_time=None,
                       end_time=None,
                       filter_string=None,
                       caching=None):
        """
        Allocate a new table scanner.

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

        Returns
        -------
        str
            The URI which should be used to address the scanner.
        None
            The table does not exist.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        scanner = schema_pb2.Scanner()
        if start_row:
            scanner.startRow = start_row.encode()
        if end_row:
            scanner.endRow = end_row.encode()
        if columns:
            for col in columns:
                scanner.columns.append(col.encode())
        if cell_batch:
            scanner.batch = cell_batch
        if start_time:
            scanner.startTime = start_time
        if end_time:
            scanner.endTime = end_time
        if filter_string:
            scanner.filter = str(filter_string)
        if caching:
            scanner.caching = caching

        response = self._session.post(
            url='/'.join((self._base_url, table_name, 'scanner')),
            headers={
                'Accept': 'application/x-protobuf',
                'Content-Type': 'application/x-protobuf',
            },
            data=scanner.SerializeToString()
        )
        code = response.status_code
        if code == CREATED:
            return response.headers['Location']
        if code == NOT_FOUND:
            return None
        raise HbaseServerError(code, response.text)

    def delete_scanner(self, scanner_loc):
        """
        Delete resources associated with the scanner.

        Parameters
        ----------
        scanner_loc : str
            The URI which should be used to address the scanner.

        Returns
        -------
        True
            The scanner is deleted.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """
        response = self._session.delete(
            url=scanner_loc,
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            return True
        raise HbaseServerError(code, response.text)

    def iter_scanner(self, scanner_loc, row_batch=None, include_timestamp=False):
        """
        Iterate a scanner.

        Parameters
        ----------
        scanner_loc : str
            The URI which should be used to address the scanner.
        row_batch : int
            The maximum number of rows to return in each REST request, by default None
        include_timestamp : bool, optional
            Whether timestamps are returned, by default False

        Returns
        -------
        list[tuple]
            List of `(row_key, row_data)` tuples.

        Raises
        ------
        HbaseServerError
            Server returns other errors.
        """

        if row_batch:
            scanner_loc += '?n=' + str(row_batch)

        response = self._session.get(
            url=scanner_loc,
            headers={
                'Accept': 'application/x-protobuf'
            }
        )
        code = response.status_code
        if code == OK:
            cell_set = schema_pb2.CellSet()
            cell_set.ParseFromString(response.content)
            return [
                (row.key.decode(), _make_row(row.values, include_timestamp))
                for row in cell_set.rows
            ]
        if code == NO_CONTENT:
            return None
        raise HbaseServerError(code, response.text)
