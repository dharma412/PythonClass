import polling

import mysql.connector as mysql
from robot.api import logger

from Logger import exec_log
from AtlasTestConstants import ATLAS_CONSTANTS

class AtlasDbUtils:
    """ Library for interacting with atlas mysql database"""
    host = ATLAS_CONSTANTS['django_db_host']
    database = ATLAS_CONSTANTS['django_db_name']
    user = ATLAS_CONSTANTS['django_db_user']
    password = ATLAS_CONSTANTS['django_db_passwd']

    @exec_log
    def __init__(self):
        self.atlasdb_con = None
        self.atlasdb_cursor = None
  
    @exec_log
    def connectdb(self):
        """
         Purpose: connects to the database

        Args:
           None

        Returns:
           None
        """

        try:
            self.atlasdb_con = mysql.connect(host = AtlasDbUtils.host,
                                             user = AtlasDbUtils.user,
                                             password = AtlasDbUtils.password,
                                             database= AtlasDbUtils.database,
                                            )
            self.atlasdb_cursor = self.atlasdb_con.cursor()
        except mysql.connector.Error as err:
             logger.error("Connecting to database {} failed {}".format(self.database,err))
             raise AtlasDbConnectionFailedException("Connecting to database {} failed {}".format(self.database,err))

    @exec_log
    def closedb_con(self):
        """
         Purpose: closes the db connection

        Args:
          None

        Returns:
          None
        """
        if self.atlasdb_con:
            self.atlasdb_con.close()
    
    @exec_log    
    def get_all_db_entiries(self,table_name):
        """
         Purpose: gets the table entries in the form of list of namedtuple

        Args:
          table_name       : table name whose data has to be pulled

        Returns:
            list of namedtuple having all the data for the table
        """
        self.connectdb()
        self.atlasdb_cursor.execute(''' SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND \
                                        table_name='{0}' ORDER BY ordinal_position;'''.format(table_name))
        columns = self.atlasdb_cursor.fetchall()
        columns = [ col[0]  for col in columns ]
        self.atlasdb_cursor.execute('SELECT * from {}'.format(table_name))
        rows = self.atlasdb_cursor.fetchall()
        self.closedb_con()
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))
        return result

    @exec_log
    def execute_db_select_query(self,query): 
        """
         Purpose: executes the select query on the datbase

        Args:
          query       : select query to be executed

        Returns:
            list of rows
        """

        self.connectdb()
        self.atlasdb_cursor.execute(query)
        rows = self.atlasdb_cursor.fetchall()
        self.closedb_con()
        return rows

    @exec_log
    def execute_db_update_query(self,query):
        """
         Purpose: executes the update query on the datbase

        Args:
          query       : update query to be executed

        Returns:
            None
        """

        try:
            self.connectdb()
            self.atlasdb_cursor.execute(query)
            self.atlasdb_con.commit()    
            self.closedb_con()
        except:
            raise AtlasDbUpdateFailedException('Update failed while executing query - {}'.format(query))


