from rdflib import Graph

# Creăm un graf RDF și îl populăm cu date din fișierul RDF
g = Graph()
g.parse("e.rdf", format="xml")  # Poate fi "turtle", "n3", "nt" în funcție de format

from rdflib import OWL, RDF, RDFS, Graph, Namespace

# Interogare SPARQL pentru a obține numele și descrierea semnelor
query = """
PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>

SELECT ?signName ?signImageURL ?maxSpeed ?maxSpeedOutsideUrbanAreas ?maxSpeedUrbanAreas ?minSpeed ?maxHeight ?maxWidth ?maxWeight ?colorBackgroundName ?colorContourName ?desc 
WHERE {
    ?sign signs:signName ?signName.
    ?sign signs:signImageURL ?signImageURL.
    OPTIONAL { ?sign signs:maxSpeed ?maxSpeed. }
    OPTIONAL { ?sign signs:maxSpeedUrbanAreas ?maxSpeedUrbanAreas. }
    OPTIONAL { ?sign signs:maxSpeedOutsideUrbanAreas ?maxSpeedOutsideUrbanAreas. }
    OPTIONAL { ?sign signs:minSpeed ?minSpeed. }
    OPTIONAL { ?sign signs:maxHeight ?maxHeight. }
    OPTIONAL { ?sign signs:maxWidth ?maxWidth. }
    OPTIONAL { ?sign signs:maxWeight ?maxWeight. }

    OPTIONAL { 
        ?sign signs:hasBackgroundColor ?colorBackground.
        ?colorBackground rdfs:label ?colorBackgroundName. }

    OPTIONAL { 
        ?sign signs:hasContourColor ?colorContour.
        ?colorContour rdfs:label ?colorContourName. }    

    ?sign signs:description ?desc.


}
"""

# Rulează interogarea
results = g.query(query)

# Afișează rezultatele cu numele și descrierea pe rânduri separate
for row in results:
    print(f"Sign Name: {row.signName}")
    print(f"Sign Image URL: {row.signImageURL}")
    if row.maxSpeed is not None:
        print(f"Max Speed From Sign: {row.maxSpeed}")
    if row.maxSpeedUrbanAreas is not None:
        print(f"Max Speed Urban Areas: {row.maxSpeedUrbanAreas}")
    if row.maxSpeedOutsideUrbanAreas is not None:
        print(f"Max Speed Outside Urban Areas: {row.maxSpeedOutsideUrbanAreas}")
    if row.minSpeed is not None:
        print(f"Min Speed: {row.minSpeed}")
    if row.colorContourName is not None:
        print(f"Contour Color: {row.colorContourName}")  # Afișăm culoarea fundalului   
    if row.colorBackgroundName is not None:
        print(f"Background Color: {row.colorBackgroundName}")  # Afișăm culoarea fundalului      
                                   
                            
    print(f"Description: {row.desc}\n")




