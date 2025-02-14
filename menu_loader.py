import json

class MenuLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.menu = self.load_menu()

    def load_menu(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)["menu"]

    def get_categories(self):
        return [category["category"] for category in self.menu]

    def get_items(self, category_name):
        for category in self.menu:
            if category["category"] == category_name:
                return category["items"]
        return []

    def get_price(self, item_name):
        for category in self.menu:
            for item in category["items"]:
                if item["name"] == item_name:
                    return item["price_kzt"]
        return 0
