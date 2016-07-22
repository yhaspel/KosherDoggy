# KosherDoggy

KosherDoggy – Django Web Application designed to assist dog owners with obtaining dog food information, dog food comparison and other dog related information

To view project screenshots, go to screenshots/ directory within project.
Initial setup for this project:
* Install Python 3.x
* Make your own virtual environment: mkvirualenv <environment name>
* Initiate environment: workon <environment name>
* Clone the project into the folder you’re working on
* Install  requirements: pip install –r “requirements.txt”
* To populate database with some data, open python console on your project:
  * from doggyfood.dbpopulator import populate_all
  * populate_all()


Guide:
* Home screen shows card display of dog foods and a search and filter section on the top of the page, below the title
* Search and filter section allows user to search dog food
* Each card contains:
 * Compare checkbox, arrow up/down icon to reveal or hide more care info, eye icon to preview dog food
 * A picture or a placeholder of the dog food
 * Title and description of the dog food
 * Ingredients and nutritional composition of dog food
 * Dog food rating
* To preview a dog food product, click on the relevant eye icon on the dog food card
* To compare dog foods, click the compare checkbox in 2 or more checkboxes and then click the ‘Compare <x> Products’ to go to the compare page
* Compare page will display the common ingredients per dog food and allow user to access preview on each product, as well as view ingredients and nutritional composition information
