class Item:
    def __init__(self, name="", type="", condition="", price="", imageURL=""):
        self.name = name
        self.type = type
        self.condition = condition
        self.price = price
        self.imageURL = imageURL

    def __str__(self):
        return f"Name: {self.name}, Condition: {self.condition} Price: {self.price}, Image URL: {self.imageURL}, Type: {self.type}"
