from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# Checks if input is empty
	if not recipeName:
		return None
	
	# Replcaes hyphens and underscores
	recipeName = recipeName.replace("-", " ").replace("_", " ")

	# Removes any characters which arent letters or spaces
	recipeName = re.sub(r"[^a-zA-Z ]", "", recipeName)
	
	# Split words and capitalize the first letter
	words = recipeName.split()
	capitalizedWords = [word.capitalize() for word in words]

	# Join words back together
	cleanedRecipe = " ".join(capitalizedWords)
	
	# Returns if string is not empty
	if cleanedRecipe:
		return cleanedRecipe
	else:
		return None



# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	data = request.get_json()

	name = data.get('name')
	entryType = data.get('type')

	# Check if name already exists in cookbook
	if cookbook and name in cookbook:
		return jsonify({"error": "Entry name must be unique"}), 400
	
	# Process ingredient entries
	if entryType == "ingredient":
		if 'cookTime' not in data or not isinstance(data['cookTime'], int) or data['cookTime'] < 0:
			return jsonify({"error": "Invalid cookTime, must be an integer >= 0"}), 400
		
		# Add to cookbook
		cookbook[name] = Ingredient(name=name, cook_time=data['cookTime'])
		
	# Process recipe entries
	elif entryType == "recipe":
		if 'requiredItems' not in data or not isinstance(data['requiredItems'], list):
			return jsonify({"error": "Invalid requireItems, must be a list"}), 400
		
		seenItems = set()
		requiredItems = []

		for item in data['requiredItems']:
			if 'name' not in item or 'quantity' not in item or not isinstance(item['quantity'], int) or item['quantity'] <= 0:
				return jsonify({"error": "Each requiredItem must have a valid name and quantity > 0"}), 400
			
			# Ensure no duplicate names in requiredItems
			if item['name'] in seenItems:
				return jsonify({"error": "Duplicate requiredItem names are not allowed"}), 400
			seenItems.add(item['name'])

			requiredItems.append(RequiredItem(name=item['name'], quantity=item['quantity']))

		cookbook[name] = Recipe(name=name, required_items = requiredItems)

	else:
		return jsonify({"error": "Invalid type, must be 'recipe' or 'ingredients'"}), 400
	
	return "success", 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
