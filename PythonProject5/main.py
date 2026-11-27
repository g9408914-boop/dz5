import random
from utils import count_calls

# Таблиця предметів (вже містить 3 нових збалансованих предмети)
LOOT_TABLE = [
    {"name": "Звичайне зілля", "type": "heal", "value": 20, "chance": 0.5},
    {"name": "Іржавий меч", "type": "damage", "value": 3, "chance": 0.3},
    # 3 нових предмети за завданням:
    {
        "name": "Мале зілля здоров'я",
        "type": "heal",
        "value": 30,
        "chance": 0.4,
    },
    {
        "name": "Точильний камінь",
        "type": "damage",
        "value": 5,
        "chance": 0.25,
    },
    {
        "name": "Амулет Дракона",
        "type": "max_hp",
        "value": 40,
        "chance": 0.15,
    },
]


# Генератор ворогів: кожен 3-й ворог — Boss із більшим HP
def enemy_generator():
    room = 0
    while True:
        room += 1
        if room % 3 == 0:
            yield {
                "name": f"BOSS Підземелля (Кімната {room})",
                "hp": 140,
                "damage": 18,
                "is_boss": True,
            }
        else:
            yield {
                "name": f"Гоблін (Кімната {room})",
                "hp": 45,
                "damage": 10,
                "is_boss": False,
            }


# Функція бою з декоратором підрахунку викликів
@count_calls
def fight(player, enemy):
    print(f"\n--- Бій! {player['name']} проти {enemy['name']} (HP: {enemy['hp']}) ---")
    while player["hp"] > 0 and enemy["hp"] > 0:
        enemy["hp"] -= player["damage"]
        print(f"Ви вдарили на {player['damage']} шкоди. HP ворога: {max(0, enemy['hp'])}")
        if enemy["hp"] <= 0:
            print(f"Перемога! {enemy['name']} переможений!")
            return True

        player["hp"] -= enemy["damage"]
        print(f"{enemy['name']} вдарив на {enemy['damage']} шкоди. Ваше HP: {max(0, player['hp'])}")
        if player["hp"] <= 0:
            print("Ви загинули у підземеллі...")
            return False


def drop_loot(player):
    for item in LOOT_TABLE:
        if random.random() <= item["chance"]:
            print(f"Ви знайшли предмет: {item['name']}!")
            if item["type"] == "heal":
                player["hp"] = min(player["max_hp"], player["hp"] + item["value"])
                print(f"Здоров'я відновлено до {player['hp']}/{player['max_hp']}.")
            elif item["type"] == "damage":
                player["damage"] += item["value"]
                print(f"Ваша атака зросла до {player['damage']}!")
            elif item["type"] == "max_hp":
                player["max_hp"] += item["value"]
                player["hp"] += item["value"]
                print(f"Максимальне HP збільшено до {player['max_hp']}!")
            break


def main():
    player = {"name": "Герой", "hp": 100, "max_hp": 100, "damage": 20}
    enemies = enemy_generator()
    total_rooms = 6  # Проходимо 6 кімнат, щоб зустріти 2 босів (у 3-й та 6-й кімнатах)

    print("Ласкаво просимо до підземелля!")
    for _ in range(total_rooms):
        enemy = next(enemies)
        survived = fight(player, enemy)
        if not survived:
            break
        drop_loot(player)

    print("\n==============================")
    print(f"Гру завершено! Кількість проведених боїв: {fight.calls}")
    print("==============================")


if __name__ == "__main__":
    main()
