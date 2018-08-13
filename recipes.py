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

for link in list_of_recipes:
	#Loop through url's to find ingredients and difficulty