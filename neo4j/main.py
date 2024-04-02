from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def import_data(tx):
    tx.run("LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row "
           "CREATE (:Person {name: row.name, age: toInteger(row.age)})")

with driver.session() as session:
    session.write_transaction(import_data)

driver.close()