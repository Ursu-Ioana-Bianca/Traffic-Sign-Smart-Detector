from flask import Blueprint, jsonify
from ontology_exemple import load_ontology, categories

signs_blueprint = Blueprint('signs', __name__)

@signs_blueprint.route('/get_signs', methods=['GET'])
def get_signs():
    """
    Returnează semnele de circulație din ontologie.
    """
    load_ontology()
    return jsonify(categories)
