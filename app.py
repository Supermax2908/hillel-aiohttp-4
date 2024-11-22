import asyncio
import aiohttp
import random

pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "jigglypuff",
    "meowth", "psyduck", "machop", "geodude", "magikarp"
]


# дістаємо з url персонажів і перевіряємо url на справність
async def fetch_pokemon(session, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed to fetch data for {name}: {response.status}")
            return None

# Обрахування сили двох персонажів
def calculate_strength(pokemon_data):
    if not pokemon_data:
        return 0
    stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
    return stats.get('attack', 0) + stats.get('defense', 0) + stats.get('speed', 0)

# Батл між двома персонажами
def simulate_battle(pokemon1, pokemon2):
    strength1 = calculate_strength(pokemon1)
    strength2 = calculate_strength(pokemon2)
    winner = pokemon1['name'] if strength1 >= strength2 else pokemon2['name']
    return {
        'pokemon1': pokemon1['name'],
        'pokemon2': pokemon2['name'],
        'strength1': strength1,
        'strength2': strength2,
        'winner': winner
    }

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, name) for name in pokemon_names]
        pokemon_data = await asyncio.gather(*tasks)

    valid_pokemon = [data for data in pokemon_data if data]

    if len(valid_pokemon) < 2:
        print("Not enough Pokémon fetched successfully to simulate a battle.")
        return

    pokemon1, pokemon2 = random.sample(valid_pokemon, 2)
    battle_result = simulate_battle(pokemon1, pokemon2)

    print(f"Battle Result: {battle_result['pokemon1']} vs {battle_result['pokemon2']}")
    print(f"Strengths: {battle_result['strength1']} vs {battle_result['strength2']}")
    print(f"Winner: {battle_result['winner']}")


if __name__ == "__main__":
    asyncio.run(main())