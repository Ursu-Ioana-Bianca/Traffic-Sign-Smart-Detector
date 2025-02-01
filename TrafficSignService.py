from rdflib import Graph

# Creăm un graf RDF și îl populăm cu date din fișierul RDF
g = Graph()
g.parse("TrafficSignOntology.rdf", format="xml")  # Poate fi "turtle", "n3", "nt" în funcție de format

from rdflib import OWL, RDF, RDFS, Graph, Namespace

# # Interogare SPARQL pentru a obține numele și descrierea semnelor
# query = """
# PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>

# SELECT ?signName ?signImageURL ?maxSpeed ?maxSpeedOutsideUrbanAreas ?maxSpeedUrbanAreas ?minSpeed ?maxHeight 
#      ?maxWidth ?maxWeight ?colorBackgroundName ?colorContourName ?signCategoryName ?desc 
# WHERE {
#     ?sign signs:signName ?signName.
#     ?sign signs:signImageURL ?signImageURL.
#     OPTIONAL { ?sign signs:maxSpeed ?maxSpeed. }
#     OPTIONAL { ?sign signs:maxSpeedUrbanAreas ?maxSpeedUrbanAreas. }
#     OPTIONAL { ?sign signs:maxSpeedOutsideUrbanAreas ?maxSpeedOutsideUrbanAreas. }
#     OPTIONAL { ?sign signs:minSpeed ?minSpeed. }
#     OPTIONAL { ?sign signs:maxHeight ?maxHeight. }
#     OPTIONAL { ?sign signs:maxWidth ?maxWidth. }
#     OPTIONAL { ?sign signs:maxWeight ?maxWeight. }

#     OPTIONAL { 
#         ?sign signs:hasBackgroundColor ?colorBackground.
#         ?colorBackground rdfs:label ?colorBackgroundName. }

#     OPTIONAL { 
#         ?sign signs:hasContourColor ?colorContour.
#         ?colorContour rdfs:label ?colorContourName. }

#     OPTIONAL { 
#         ?sign signs:category ?signCategory.
#         ?signCategory rdfs:label ?signCategoryName 
#     }        

#     ?sign signs:description ?desc.


# }
# """

# # Rulează interogarea
# results = g.query(query)

# # Afișează rezultatele cu numele și descrierea pe rânduri separate
# for row in results:
#     print(f"Sign Category: {row.signCategoryName}")  # Afișăm culoarea fundalului 
#     print(f"Sign Name: {row.signName}")
#     print(f"Sign Image URL: {row.signImageURL}")
#     if row.maxSpeed is not None:
#         print(f"Max Speed From Sign: {row.maxSpeed}")
#     if row.maxSpeedUrbanAreas is not None:
#         print(f"Max Speed Urban Areas: {row.maxSpeedUrbanAreas}")
#     if row.maxSpeedOutsideUrbanAreas is not None:
#         print(f"Max Speed Outside Urban Areas: {row.maxSpeedOutsideUrbanAreas}")
#     if row.minSpeed is not None:
#         print(f"Min Speed: {row.minSpeed}")
#     if row.colorContourName is not None:
#         print(f"Contour Color: {row.colorContourName}")  # Afișăm culoarea fundalului   
#     if row.colorBackgroundName is not None:
#         print(f"Background Color: {row.colorBackgroundName}")  # Afișăm culoarea fundalului      
                                   
                            
#     print(f"Description: {row.desc}\n")



# Execută interogarea pentru a obține toate categoriile
category_query = """
PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?signCategoryName
WHERE {
    ?sign signs:category ?signCategory.
    ?signCategory rdfs:label ?signCategoryName.
}
ORDER BY ?signCategoryName
"""

category_results = g.query(category_query)

# Creează un dicționar pentru a stoca semnele pe categorii
categories = {}

# Rulează interogarea pentru fiecare categorie și adaugă rezultatele în dicționar
for category_row in category_results:
    category_name = str(category_row.signCategoryName)  # Convertim în string
    
    categories[category_name] = []  # Inițializăm o listă goală pentru această categorie
    
    # Interogare pentru semnele din categoria curentă
    sign_query = f"""
    PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?signName ?signImageURL ?signDescription ?associatedSignName ?associatedSignImageUrl
    WHERE {{
        ?sign signs:signName ?signName.
        ?sign signs:signImageURL ?signImageURL.
        ?sign signs:description ?signDescription.
        ?sign signs:category ?signCategory.
        ?signCategory rdfs:label ?signCategoryName.

        OPTIONAL {{
        ?sign signs:hasAssociatedSign ?associatedSign.
        ?associatedSign rdfs:label ?associatedSignName.
        ?associatedSign signs:signImageURL ?associatedSignImageUrl.
    }}
        FILTER (STR(?signCategoryName) = "{category_name}")
    }}
    ORDER BY ?signName
    """
    
    sign_results = g.query(sign_query)
    
    for sign_row in sign_results:
        categories[category_name].append(str(sign_row.signName))  # Convertim în string
        categories[category_name].append(str(sign_row.signImageURL))
        categories[category_name].append(str(sign_row.signDescription))
        if sign_row.associatedSignName is not None:
            categories[category_name].append(str(sign_row.associatedSignName))
        if sign_row.associatedSignImageUrl is not None:    
            categories[category_name].append(str(sign_row.associatedSignImageUrl))

# Afișează rezultatele
for category, signs in categories.items():
    print(f"Category: {category}")
    if signs:
        for sign in signs:
            print(f"  - {sign}")
    else:
        print("  No signs found for this category.")
    print()



