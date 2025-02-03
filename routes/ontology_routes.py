from flask import Blueprint, jsonify
from rdflib import Graph

ontology_blueprint = Blueprint('ontology', __name__)

categories = {}
signs_name = []
signs_properties = {}


def load_ontology():
    global categories, signs_name, signs_properties  # Asigură-te că folosești variabilele globale

    # Curățăm datele pentru a preveni dublarea informațiilor
    categories.clear()
    signs_name.clear()
    signs_properties.clear()

    g = Graph()
    g.parse("TrafficSignOntology.rdf", format="xml")  # Poate fi "turtle", "n3", "nt" în funcție de format
    # Execută interogarea pentru a obține toate categoriile
    category_query = """
    PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
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

    for category_row in category_results:
        category_name = str(category_row.signCategoryName)
        categories[category_name] = []

        sign_query = f"""
        PREFIX signs: <http://www.semanticweb.org/bianca/ontologies/2025/0/signs#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?signName ?signImageURL ?signDescription ?associatedSignName ?associatedSignImageUrl 
                ?shapeName ?contourColor ?backgroundColor ?symbolDescription
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

            OPTIONAL {{
                ?sign signs:hasShape ?shape.
                ?shape rdfs:label ?shapeName.

                ?sign signs:hasContourColor ?contour.
                ?contour rdfs:label ?contourColor.

                ?sign signs:hasBackgroundColor ?background.
                ?background rdfs:label ?backgroundColor.

                ?sign signs:hasSymbol ?symbol.
                ?symbol rdfs:label ?symbolDescription.

            }}

            FILTER (STR(?signCategoryName) = "{category_name}")
        }}
        ORDER BY ?signName
        """

        sign_results = g.query(sign_query)

        for sign_row in sign_results:
            signs_name.append(str(sign_row.signName))

            signs_properties[str(sign_row.signName)] = []
            signs_properties[str(sign_row.signName)].append({
                "image": str(sign_row.signImageURL),
                "description": str(sign_row.signDescription),
                "category": category_name,
            })

            # Verificăm dacă semnul există deja în listă
            existing_sign = next((s for s in categories[category_name] if s["name"] == str(sign_row.signName)), None)

            if existing_sign:
                # Dacă semnul există deja, verificăm dacă semnul asociat nu este deja adăugat
                if sign_row.associatedSignName is not None:
                    # Verificăm dacă semnul asociat nu există deja în lista de semne asociate
                    associated_sign = next(
                        (s for s in existing_sign["associatedSigns"] if s["name"] == str(sign_row.associatedSignName)),
                        None)

                    if associated_sign is None:
                        # Dacă semnul asociat nu este în lista, îl adăugăm
                        existing_sign["associatedSigns"].append({
                            "name": str(sign_row.associatedSignName),
                            "image": str(
                                sign_row.associatedSignImageUrl) if sign_row.associatedSignImageUrl is not None else None
                        })
            else:
                # Dacă semnul NU există, îl creăm și îl adăugăm în listă
                sign_data = {
                    "name": str(sign_row.signName),
                    "image": str(sign_row.signImageURL),
                    "description": str(sign_row.signDescription),
                    "shape": str(sign_row.shapeName) if sign_row.shapeName is not None else "",
                    "background": str(sign_row.backgroundColor) if sign_row.backgroundColor is not None else "",
                    "contour": str(sign_row.contourColor) if sign_row.contourColor is not None else "",
                    "symbol": str(sign_row.symbolDescription) if sign_row.symbolDescription is not None else "",
                    "associatedSigns": []
                }

                if sign_row.associatedSignName is not None:
                    # Verificăm dacă semnul asociat nu există deja
                    associated_sign = {
                        "name": str(sign_row.associatedSignName),
                        "image": str(
                            sign_row.associatedSignImageUrl) if sign_row.associatedSignImageUrl is not None else None
                    }
                    # Verificăm dacă semnul asociat este deja în lista
                    if associated_sign not in sign_data["associatedSigns"]:
                        sign_data["associatedSigns"].append(associated_sign)

                categories[category_name].append(sign_data)  # Adăugăm semnul principal în listă

@ontology_blueprint.route('/load_ontology', methods=['GET'])
def get_ontology():
    load_ontology()
    return jsonify(categories)
