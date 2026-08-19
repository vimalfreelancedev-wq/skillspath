"""
Database connection management for Django.
"""
import logging
from neo4j import GraphDatabase, exceptions
from django.conf import settings

logger = logging.getLogger(__name__)

_driver = None

def get_driver():
    """Return the Neo4j driver singleton."""
    global _driver
    if _driver is None:
        uri = settings.NEO4J_URI
        user = settings.NEO4J_USER
        password = settings.NEO4J_PASSWORD
        if not uri or not password:
            raise RuntimeError("Neo4j credentials not set in environment.")
        _driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            max_connection_pool_size=50,
            connection_timeout=30,
            max_connection_lifetime=3600
        )
    return _driver

def close_driver():
    """Close the driver if it exists."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
        logger.debug("Database driver closed.")

def run_query(query, parameters=None, database=None):
    """
    Execute a Cypher query and return a list of records.
    Uses parameterised queries – safe from injection.
    """
    parameters = parameters or {}
    database = database or settings.NEO4J_DATABASE
    try:
        driver = get_driver()
        with driver.session(database=database) as session:
            result = session.run(query, parameters)
            return [record for record in result]
    except exceptions.ServiceUnavailable:
        logger.error("Database service unavailable.")
        raise
    except exceptions.CypherSyntaxError as e:
        logger.error(f"Cypher syntax error: {e}")
        raise
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise