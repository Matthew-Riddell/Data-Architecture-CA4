// Matthew Riddell D00245674
// Neo4j Queries

// clear existing graph
MATCH (n)
DETACH DELETE n

// Create store nodes
CREATE (:Store {name: 'Blunt Umbrellas'})
CREATE (:Store {name: 'Meow Meow Tweet'})

// Create product nodes
CREATE (:Product {
    title: 'Metro Umbrella',
    price: 159.00,
    type: 'Umbrella'
})

CREATE (:Product {
    title: 'Deodorant Cream',
    price: 18.00,
    type: 'Body Care'
})

// Create vendor nodes
CREATE (:Vendor {name: 'BLUNT'})
CREATE (:Vendor {name: 'Meow Meow Tweet'})

// Relationships
// Store to Product
MATCH (s:Store {name:'Blunt Umbrellas'})
MATCH (p:Product {title:'Metro Umbrella'})
CREATE (s)-[:SELLS]->(p)

MATCH (s:Store {name:'Meow Meow Tweet'})
MATCH (p:Product {title:'Deodorant Cream'})
CREATE (s)-[:SELLS]->(p)

// Product to Vendor
MATCH (p:Product {title:'Metro Umbrella'})
MATCH (v:Vendor {name:'BLUNT'})
CREATE (p)-[:MADE_BY]->(v)

MATCH (p:Product {title:'Deodorant Cream'})
MATCH (v:Vendor {name:'Meow Meow Tweet'})
CREATE (p)-[:MADE_BY]->(v)

// View graph
MATCH (n)-[r]-(m)
RETURN n,r,m

// Queries
// 1. products sold by each store

MATCH (s:Store)-[:SELLS]->(p:Product)
RETURN s.name AS store, p.title AS product

// 2. vendors connected to products
MATCH (p:Product)-[:MADE_BY]->(v:Vendor)
RETURN p.title AS product, v.name AS vendor
