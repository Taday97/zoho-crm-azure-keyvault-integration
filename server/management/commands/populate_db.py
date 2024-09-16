import json
from django.core.management.base import BaseCommand
from server.models import Product  
from server.models import SubCategory  
from server.models import SubProduct  

# Method to populate the database with JSON files.
class Command(BaseCommand):
    help = 'Populate the database from a JSON file'

    def handle(self, *args, **options):
        with open('server/populate_json/products.json', 'r') as file:
            data = json.load(file)
            for item in data['products']:
                person = Product(productId=item['productId'], productName=item['productName'])
                person.save()

        with open('server/populate_json/subcategories.json', 'r') as file:
            data = json.load(file)
            for item in data['subcatergories']:
                try:
                 product_instance = Product.objects.get(productId=item['productId'])
                except Product.DoesNotExist:
                 # Handle the case where the product does not exist, for example, by continuing to the next item
                 continue
                subcategories = SubCategory(product=product_instance,subCategoryId=item['subCategoryId'], subCategoryName=item['subCategoryName'])
                subcategories.save()

        with open('server/populate_json/subproducts.json', 'r') as file:
            data = json.load(file)
            for item in data['subproducts']:
                try:
                 subcategory_instance = SubCategory.objects.get(subCategoryId=item['subCategoryId'])
                except SubCategory.DoesNotExist:
                 continue 
                subproducts = SubProduct(subProductId=item['subProductId'],subProductName=item['subProductName'],subCategory=subcategory_instance)
                subproducts.save()
        self.stdout.write(self.style.SUCCESS('Database successfully populated'))