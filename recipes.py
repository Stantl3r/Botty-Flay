import requests
from bs4 import BeautifulSoup

print('Which ingredients are you using?')
ingredients = input()
print('Which difficulty did you want the recipe to be? (Easy, Intermediate, Advanced, or None)')
user_difficulty = input()
if len(user_difficulty) > 0:
	user_difficulty = user_difficulty[0].lower() + user_difficulty[1:]

#Creates url to scrape
list_of_ingredients = ingredients.split(",")
url = 'https://www.foodnetwork.com/search/'
for item in list_of_ingredients:
	item = item.strip()
	url = url + item + '-'

#Load first page of recipes
html_recipes = list()
list_of_recipes = list()
r = requests.get(url + '/CUSTOM_FACET:RECIPE_FACET')
soup = BeautifulSoup(r.content, 'html.parser')
results = soup.findAll('a',href=True)
for recipes in results:
	if 'recipes/' in recipes['href']:
		html_recipes.insert(len(html_recipes), recipes['href'])

#Load second page of recipes
r = requests.get(url + '/p/2' + '/CUSTOM_FACET:RECIPE_FACET')
soup = BeautifulSoup(r.content, 'html.parser')
results = soup.findAll('a',href=True)
for recipes in results:
	if 'recipes/' in recipes['href']:
		html_recipes.insert(len(html_recipes), recipes['href'])

for counter, recipe in enumerate(html_recipes):
	if counter != 0 and counter % 3 == 2:
		list_of_recipes.insert(len(list_of_recipes), recipe)

difficulty_easy = dict()
difficulty_intermediate = dict()
difficulty_advanced = dict()

#Iterate through recipe links
for link in list_of_recipes:
	url = 'https:' + link
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	#Get difficulty
	difficulty_level = soup.findAll('dd', {"class": "o-RecipeInfo__a-Description"})
	for counter, diff in enumerate(difficulty_level):
		if counter == (len(difficulty_level)- 1):
			difficulty_recipe = diff.text.split()
			difficulty_recipe = difficulty_recipe[0]
	if len(difficulty_level) == 0:
		list_to_filter = soup.findAll('span', {"class": "o-RecipeInfo__a-Description"})
		for counter, diff in enumerate(list_to_filter):
			if counter == 0:
				difficulty_recipe = diff.text.strip()

	#Get ingredients
	ingredients_of_recipe = soup.findAll('label', {"class": "o-Ingredients__a-ListItemText"})
	if len(ingredients_of_recipe) == 0:
		ingredients_of_recipe = soup.findAll('p', {"class": "o-Ingredients__a-Ingredient"})

	#Check if all ingredients are in recipe
	check = 0
	for ingredient in list_of_ingredients:
		for element in ingredients_of_recipe:
			if ingredient in element.text:
				check += 1
				break
	has_ingredients = (check == len(list_of_ingredients))

	#Print if the ingredients are in the recipe
	if has_ingredients:
		print('Fetching...')
		print(difficulty_recipe)
		if difficulty_recipe == 'Easy':
			recipe_name = soup.findAll('h1', {"class": "o-AssetTitle__a-Headline"})
			for i, h in enumerate(recipe_name):
				if i == 0:
					name = h.text.strip()
					difficulty_easy[name] = url
		elif difficulty_recipe == 'Intermediate':
			recipe_name = soup.findAll('h1', {"class": "o-AssetTitle__a-Headline"})
			for i, h in enumerate(recipe_name):
				if i == 0:
					name = h.text.strip()
					difficulty_intermediate[name] = url
		elif difficulty_recipe == 'Advanced':
			recipe_name = soup.findAll('h1', {"class": "o-AssetTitle__a-Headline"})
			for i, h in enumerate(recipe_name):
				if i == 0:
					name = h.text.strip()
					difficulty_advanced[name] = url
	check = 0
	has_ingredients = False

#Print results
if user_difficulty == 'easy':
	for i in difficulty_easy:
		print(i + ': ' + difficulty_easy[i])
elif user_difficulty == 'intermediate':
	for i in difficulty_intermediate:
		print(i + ': ' + difficulty_intermediate[i])
elif user_difficulty == 'advanced':
	for i in difficulty_advanced:
		print(i + ': ' + difficulty_advanced[i])
else:
	print('Easy:')
	for i in difficulty_easy:
		print(i + ': ' + difficulty_easy[i])
	print('Intermediate:')
	for i in difficulty_intermediate:
		print(i + ': ' + difficulty_intermediate[i])
	print('Advanced:')
	for i in difficulty_advanced:
		print(i + ': ' + difficulty_advanced[i])