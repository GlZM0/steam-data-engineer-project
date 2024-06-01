from utils import extract_condition_and_clean_name
from item import Item

class ItemProcessor:
    @staticmethod
    def process_item_data(item_data):
        name, condition = extract_condition_and_clean_name(item_data["name"])
        return Item(
            name=name,
            type=item_data["asset_description"].get("type", ""),
            condition=condition,
            price=item_data['sell_price_text'].replace('$', '').replace(',', ''),
            imageURL=f"https://community.cloudflare.steamstatic.com/economy/image/{item_data['asset_description']['icon_url']}"
        )

    @staticmethod
    def categorize_item_type(item_type):
        if "Music Kit" in item_type:
            return "Blue"
        elif "Base Grade" in item_type:
            return "Lighter Blue"
        elif "High Grade" in item_type:
            return "Blue"
        elif "Remarkable" in item_type:
            return "Purple"
        elif "Exotic" in item_type:
            return "Pink"
        elif "Extraordinary" in item_type:
            return "Red"
        elif "Distinguished" in item_type:
            return "Blue"
        elif "Exceptional" in item_type:
            return "Purple"
        elif "Superior" in item_type:
            return "Pink"
        elif "Master" in item_type:
            return "Red"
        elif "Contraband" in item_type:
            return "Yellow"
        elif "Consumer" in item_type:
            return "Lighter Blue"
        elif "Industrial" in item_type:
            return "Light Blue"
        elif "Mil-Spec" in item_type:
            return "Blue"
        elif "Restricted" in item_type:
            return "Purple"
        elif "Classified" in item_type:
            return "Pink"
        elif "Covert" in item_type:
            return "Red"
        elif "★ Covert Knife" in item_type:
            return "Yellow"
        else:
            return "Unknown"

    @staticmethod
    def add_skin_hex_color(color):
        color_lower = color.lower()
        if color_lower == "lighter blue":
            return '#b0c3d9'
        elif color_lower == 'light blue':
            return '#5e98d9'
        elif color_lower == 'blue':
            return '#2563eb'
        elif color_lower == 'purple':
            return '#7c3aed'
        elif color_lower == 'pink':
            return '#d946ef'
        elif color_lower == 'red':
            return '#dc2626'
        elif color_lower == 'yellow':
            return '#eab308'
        else:
            return 'no color'

    @staticmethod
    def set_condition(item):
        if "Sticker" in item.name:
            return ''
        elif "Graffiti" in item.name:
            return ''
        else:
            return item.condition