class Character:
    def __init__(self,
                 name: str,
                 health: int,
                 ) -> None:
        self.name = name
        self.health = health
        self.health_max = health

if __name__ == "__main__":
    characters_dict = {}
    for i in range(2):
        character_name = input("\nWhat is your name? ")
        character_health = input("What is your health? ")
        characters_dict[character_name] = Character(character_name, character_health)
    
    current_character = input(f"\nWhat character do you want to see? Options: {', '.join(characters_dict)}: ")
    print(characters_dict[current_character].name, characters_dict[current_character].health)   
