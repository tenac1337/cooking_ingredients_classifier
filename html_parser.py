#!/usr/bin/env python

import sys
from lxml import html
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen #py36
import re 
import requests
import io
from io import StringIO
import csv

num_webpages = 12
keyword = "salad"
recipestree = []
base_url = "https://cookpad.com/"
search_term_url = ""
recipes_url_str = []
recipes = []
data_path = "/Users/kevinhchon/Documents/_CMU/Research/Cooking/dataset/"

class Recipe:
	def __init__(self):
		self.name = ""
		self.url = ""
		self.ingredients = []
		self.ingredients_quantity = []
		self.main_image = ""

countries_english = ['us', 'uk', 'in', 'za', 'ng', 'ke']
country = countries_english[0]
#get all the child recipe elements
for webpage_num in range(1,num_webpages+1):
    search_term_url = base_url + country + "/search/" + keyword + "?page=" + str(webpage_num)
    print("search_term_url: ", search_term_url)
    try:
    	page = requests.get(search_term_url)
    except:
    	print("Could not parse: ", search_term_url)
    	continue
    tree = html.fromstring(page.content)
    #recipes_result_page = tree.xpath('//*[contains(@class, "wide-card ranked-list__item")]')
    recipes_result_elem = tree.xpath('//*[contains(@class, "media")]')
    #print("recipes_result_elem: ", recipes_result_elem)
    #print("len of recipestree: ", recipestree)
    recipestree += recipes_result_elem

#get child recipe Url strings
for child in recipestree:
	child_link = child.get('href')
	country_url = base_url + country
	if child_link == country_url:
		continue
	if child_link is not None:
		full_recipe_url = base_url + child_link
		print("full_recipe_url: ", full_recipe_url)
		recipes_url_str.append(full_recipe_url)

ids_to_ingredients = []
ingredients_save_path = data_path + "/ingredients/ingredients_" + country+ ".csv"
#parse each individual child recipe
recipe_count = 0 

print("recipes_url_str: ", recipes_url_str)

for recipe_url_str in recipes_url_str:
	print("recipe_url_str:", recipe_url_str)
	child_url_lst = recipe_url_str.split('/')
	child_url_str = child_url_lst[-1]
	child_id_lst = child_url_str.split('-')
	child_id = child_id_lst[0]
	print("child_url_str: ", child_url_str)
	print("child_id: ", child_id)
	'''
	try:
		page = requests.get(recipe_url_str)
	except:
		print("Could not parse: ", recipe_url_str)
		continue
	tree = html.fromstring(page.content)
	image_elem = tree.xpath('//meta[@property="og:image"]/@content')
	print("image_elem: ", image_elem)
	'''
	image_url = image_elem[0]
	img_data = requests.get(image_url).content
	image_save_path = data_path + "/images/" + child_url_str + ".jpg"
	
	with open(image_save_path, 'wb') as handler:
		handler.write(img_data)
		print("saving image: ", child_url_str)

	recipe_name_elems = tree.xpath('//*[contains(@class, "recipe-show__title recipe-title strong field-group--no-container-xs")]/text()')
	recipe_name_lst = recipe_name_elems[0].split('\n')
	recipe_name = recipe_name_lst[1]
	recipe_name = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', recipe_name, flags=re.M)
	print("recipe_name:", recipe_name)
	ingredients_name_elems = tree.xpath('//*[contains(@class, "ingredient__details")]/text()')
	ingredients_name = list(filter(lambda x: x != "\n          ", ingredients_name_elems))
	ingredients_name = list(map(lambda ing: re.sub(r'(^[ \t]+|[ \t]+[ \n]+(?=:))', '', ing, flags=re.M), ingredients_name))
	ingredients_name = list(map(lambda ing: re.sub(r'\n', '', ing, flags=re.M), ingredients_name))
	ingredients_name = list(map(lambda ing: ing.lower(),ingredients_name))

	print("ingredients: ", ingredients_name)
	ingredients_quantity_elems = tree.xpath('//*[contains(@class, "ingredient__quantity")]')
	ingredient_quantity = list(map(lambda x: x.text, ingredients_quantity_elems))
	id_to_ingredient = child_id
	id_to_ingredient += ":"
	id_to_ingredient += str(ingredients_name)
	ids_to_ingredients.append(id_to_ingredient)
	print("ids_to_ingredients: ", ids_to_ingredients)
	print("ingredients quantities: ", ingredient_quantity)
	if (len(ingredients_name) != len(ingredient_quantity)):
		print("Mismatch between ingredients and respective quantities")
	#parse all the ingredient names
	'''
	for ingredient_elem in ingredients_result_elem:
		#print(repr(ingredient_elem.text_content()))
		ingredient_children = ingredient_elem.getchildren()
		print(ingredient_elem)
		print("ingredient_children: ", ingredient_children)
		#print(ingredient_elem.get('ingredient__quantity'))
		ingredient_quantity = ingredient_elem[0].text_content() #span class = ingredient__quantity
	'''
	recipe_count += 1

print("recipe_count: ", recipe_count)
ids_to_ingredients_str = ''.join(ids_to_ingredients)
print("ids_to_ingredients_str", ids_to_ingredients_str)
ids_to_ingredient_byte = io.StringIO(ids_to_ingredients_str)

'''
writer = csv.writer(open(ingredients_save_path, 'wb'))
with open(ingredients_save_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in ids_to_ingredients:
        writer.writerows([[i]])
'''








