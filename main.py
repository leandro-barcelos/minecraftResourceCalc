import json
import math


class Recipe:
    def __init__(self):
        self.input_items = []
        self.output_items = []


class ResourceCalculator:
    def __init__(self):
        self.recipes = {}

    def add_recipe(self):
        recipe = Recipe()

        print("- Required items")
        self._get_items_input(recipe.input_items)

        print("- Output items")
        self._get_items_input(recipe.output_items)

        for _, item_name in recipe.output_items:
            self.recipes[item_name] = recipe

    def view_recipes(self):
        print("Recipes:")
        for item_name, recipe in self.recipes.items():
            print(f"\nCrafting {item_name}:")
            print("Input items:")
            self._display_items(recipe.input_items)
            print("Output items:")
            self._display_items(recipe.output_items)

    def calculate_resources(self):
        item_name = input("Enter the name of the item to calculate resources for: ")
        quant = int(input("Enter the quantity: "))
        resources = {}
        leftovers = {}
        queue = []
        self.calculate_resources_impl(item_name, quant, resources, leftovers, queue)

        # Print calculated resources
        print("\nTotal raw resources needed:")
        resources_list = [(q, n) for n, q in resources.items()]
        self._display_items(resources_list)

        # Print leftovers
        print("\nLeftovers:")
        leftovers_list = [(q, n) for n, q in leftovers.items()]
        self._display_items(leftovers_list)

        # Print queue
        print("\n Queue:")
        for q, item in queue:
            print(f"\t Craft {q} {item}")

    def calculate_resources_impl(self, item_name, quant, resources, leftovers, queue):
        if item_name in leftovers:
            tmp = quant
            quant = max(0, quant - leftovers[item_name])
            leftovers[item_name] = max(0, leftovers[item_name] - tmp)
            if leftovers[item_name] == 0:
                del leftovers[item_name]

        if quant == 0:
            return

        if item_name in self.recipes:
            recipe = self.recipes[item_name]
            q_craft = [
                q
                for q, name in self.recipes[item_name].output_items
                if name == item_name
            ][0]

            n = math.ceil(quant / q_craft)
            q_craft *= n

            q_left = quant % q_craft if quant >= q_craft else q_craft - quant

            if q_left != 0:
                if item_name in leftovers:
                    leftovers[item_name] += q_left
                else:
                    leftovers[item_name] = q_left

            for q, name in recipe.input_items:
                self.calculate_resources_impl(name, q * n, resources, leftovers, queue)

            if item_name in [x[1] for x in queue]:
                for x in queue:
                    if x[1] == item_name:
                        x[0] += quant + q_left
            else:
                queue.append([quant + q_left, item_name])
        else:
            if item_name in resources:
                resources[item_name] += quant
            else:
                resources[item_name] = quant

    def save_to_json(self, filename):
        with open(filename, "w") as file:
            recipes_json = {}
            for key, recipe in self.recipes.items():
                recipes_json[key] = {
                    "input_items": recipe.input_items,
                    "output_items": recipe.output_items,
                }
            json.dump(recipes_json, file, indent=2)
        print(f"Recipes saved to {filename}.")

    def load_from_json(self, filename):
        with open(filename, "r") as file:
            recipes_json = json.load(file)
            for key, recipe_data in recipes_json.items():
                recipe = Recipe()
                recipe.input_items = recipe_data["input_items"]
                recipe.output_items = recipe_data["output_items"]
                self.recipes[key] = recipe
        print(f"Recipes loaded from {filename}.")

    def _get_items_input(self, items_list):
        while True:
            quant = input("\tQuantity (press Enter to finish): ")
            if quant == "":
                break
            else:
                quant = int(quant)
            item_name = input("\tItem Name: ")
            items_list.append((quant, item_name))

    def _display_items(self, items_list):
        for quant, item_name in items_list:
            print(f"\t{quant} x {item_name}")

    def _display_items_line(self, items_list, mult):
        out = ""
        for quant, item_name in items_list:
            out += f"{quant * mult} {item_name}, "

        return out[:-2]


def main():
    calculator = ResourceCalculator()
    try:
        calculator.load_from_json("recipes.json")
    except:
        pass

    while True:
        print("\nMenu:")
        print("1. Add Recipe")
        print("2. View Recipes")
        print("3. Calculate Resources")
        print("4. Save Recipes to JSON")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            calculator.add_recipe()
        elif choice == "2":
            calculator.view_recipes()
        elif choice == "3":
            calculator.calculate_resources()
        elif choice == "4":
            calculator.save_to_json("recipes.json")
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
