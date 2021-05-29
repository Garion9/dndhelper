from Character_Module import *
from Dice_Module import *
def main():
    test_character = Character("Garion", "Druid", "Dragonborn", "CG", "Sage", 12, 12, 12, 12, 12, 12, 16, 30, 10, 10,
                               "", "", "", "")
    test_character.add_skill_proficiency("perception")
    print(test_character.death_saving_throw_failures)
    print(test_character.name)
    print(test_character.spells_list)

    print(roll_dice(1, 4))

    print(roll_d4(1))
    print(roll_d6())
    print(roll_d8(1))
    print(roll_d12())
    print(roll_d20(1))
    print(roll_d100())

    another_test_character = Character("Dewkong", "Barbarian", "Dwarf", "LG", "Miner", 14, 10, 15, 8, 14, 10, 18, 30, 10, 10,
                               "", "", "", "", level=20)

    print(test_character.get_proficiency_bonus())
    print(another_test_character.get_proficiency_bonus())
    print("========")
    print(test_character.get_passive_perception())
    print(another_test_character.get_passive_perception())
    print(test_character.skill_proficiency)
    print(another_test_character.skill_proficiency)

    print("========")
    print(test_character.get_skill_check_modifier("wisdom", "perception"))
    print(another_test_character.get_skill_check_modifier("wisdom", "perception"))
    another_test_character.add_saving_throw_proficiency("strength")
    print(another_test_character.get_saving_throw_modifier("strength"))


if __name__ == '__main__':
    main()
