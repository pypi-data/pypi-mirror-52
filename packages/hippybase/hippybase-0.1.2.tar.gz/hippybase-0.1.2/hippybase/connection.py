"""
HippyBase connection module.
"""

from .table import Table
from .client import Client

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8080


class Connection:
    """
    Connection to an HBase REST server.

    Parameters
    ----------
    host : str, optional
        The host to connect to, by default DEFAULT_HOST
    port : int, optional
        The port to connect to, by default DEFAULT_PORT
    """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.client = Client(self.host, self.port)

    def table(self, name):
        """
        Return a table object.

        Parameters
        ----------
        name : str
            Name of the table.

        Returns
        -------
        Table
            A table object.
        """
        return Table(name, self)

    def tables(self, namespace=None):
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
        return self.client.get_tables(namespace)

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
        return self.client.create_table(table_name, families)

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
        return self.client.delete_table(table_name)
