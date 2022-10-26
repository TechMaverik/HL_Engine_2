"""HL_Engine_SQLite_Processing.py"""
# author:Akhil P Jacob
# HLDynamic-Integrations
import sqlite3


class SQLiteProcessingEngine:
    """SQLite Processing Class"""

    def dmlLite_create(self, dbname, query):
        """Create Database"""
        try:
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            c.execute(query)
        except:
            return False

    def dmlLite_insert(self, dbname, query):
        """Insert Database"""
        try:
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            c.close()
            return True
        except:
            return False

    def dmLite_delete(self, dbname, query):
        """Delete Database"""
        try:
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            return "HLEngine:Cleared all Data"
        except:
            return False

    def dmLite_findData(self, dbname, query):
        """Find Data"""
        try:
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            c.execute(query)
            data = c.fetchall()
            if len(data) == 0:
                return "null"
            else:
                d = data[0]
                return d[0]
        except:
            return False

    def dmLite_findAll(self, dbname, query):
        """Find All data"""
        try:
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            c.execute(query)
            data = c.fetchall()
            for row in data:
                return row
        except:
            return False
