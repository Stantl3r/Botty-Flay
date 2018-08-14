import requests
from bs4 import BeautifulSoup

print('Which ingredients are you using?')
ingredients = input()

list_of_ingredients = ingredients.split(" ")
url = 'https://www.foodnetwork.com/search/'
for item in list_of_ingredients:
	url = url + item + '-'
url = url + '/CUSTOM_FACET:RECIPE_FACET'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
results = soup.findAll('a',href=True)
html_recipes = list()
list_of_recipes = list()

for recipes in results:
	if 'recipes/' in recipes['href']:
		html_recipes.insert(len(html_recipes), recipes['href'])

for counter, recipe in enumerate(html_recipes):
	if counter != 0 and counter % 3 == 2:
		list_of_recipes.insert(len(list_of_recipes), recipe)

difficulty_easy = dict()
difficulty_intermediate = dict()
difficulty_hard = dict()

for link in list_of_recipes:
	url = 'http:' + link
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	difficulty_level = soup.findAll('dd', {"class": "o-RecipeInfo__a-Description"})
	for counter, level in enumerate(difficulty_level):
		if counter == (len(difficulty_level) / 2) - 1:
			print('Fetching...')
			if level.text.strip() == 'Easy':
				recipe_name = soup.findAll('h1', {"class": "o-AssetTitle__a-Headline"})
				for i, h in enumerate(recipe_name):
					if i == 0:
						name = h.text.strip()
						difficulty_easy[name] = url
			elif level.text.strip() == 'Intermediate':
				recipe_name = soup.findAll('h1', {"class": "o-AssetTitle__a-Headline"})
				for i, h in enumerate(recipe_name):
					if i == 0:
						name = h.text.strip()
						difficulty_intermediate[name] = url
			else:
				recipe_name = soup.findAll('h1', {"class": "o-AssetTitle__a-Headline"})
				for i, h in enumerate(recipe_name):
					if i == 0:
						name = h.text.strip()
						difficulty_hard[name] = url
for i in difficulty_easy:
	print(i + ': ' + difficulty_easy[i])
