from flask import Blueprint, request, jsonify
import requests
import folium
from utils.haversine import haversine
from ontology_exemple import load_ontology, signs_name, signs_properties
from rapidfuzz import process

map_blueprint = Blueprint('map', __name__)

@map_blueprint.route('/get_nearby_signs', methods=['GET'])
def get_nearby_signs():
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    nearby_signs = []
    for element in data.get("elements", []):
        if "tags" in element:
            sign_name = element["tags"].get("traffic_sign", "Unknown Sign")
            sign_lat = element["lat"]
            sign_lon = element["lon"]
            distance = haversine(float(lat), float(lon), sign_lat, sign_lon)

            load_ontology()
            # Găsim cel mai apropiat nume din 'signs_name' folosind rapidfuzz
            best_match = process.extractOne(sign_name, signs_name)
            if best_match:
                sign_name = best_match[0]
                print(signs_properties[sign_name][0].get('image')
                      )
                sign_image = signs_properties[sign_name][0].get('image')
                sign_description = signs_properties[sign_name][0].get('description')
                sign_category = signs_properties[sign_name][0].get('category')

            nearby_signs.append({
                "name": sign_name,
                "latitude": sign_lat,
                "longitude": sign_lon,
                "distance": round(distance, 2),
                "image": sign_image,
                "description": f"Description: {sign_description}",
                "category": f"Category: {sign_category}"
            })

    return jsonify(nearby_signs)


@map_blueprint.route('/map', methods=['GET'])
def generate_map():
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))

    # Create map centered on user location
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], popup="You are here", icon=folium.Icon(color='blue')).add_to(m)

    # Fetch nearby signs
    signs = get_nearby_signs(lat, lon)

    for sign in signs:
        folium.Marker(
            [sign["latitude"], sign["longitude"]],
            popup=sign["name"],
            icon=folium.Icon(color='red')
        ).add_to(m)

    # Return JSON response with nearby signs instead of rendering HTML
    return jsonify({"latitude": lat, "longitude": lon, "signs": signs})
