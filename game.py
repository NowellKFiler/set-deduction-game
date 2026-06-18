import random
import asyncio

# Local fallback for async_input (not needed in Pyodide)
# Note, I've been trying to know what async is literally
# and on how Pyodide could work, but after all this time,
# I still don't know what I am doing.

# Forgive me for using AI on the cases of random, asyncio and pyodide.

if 'async_input' not in dir():
    async def async_input(prompt=""):
        return input(prompt)

def generate_hidden_sets():
    pool = list(range(1, 21))
    return set(random.sample(pool, random.randint(3, 8))), set(random.sample(pool, random.randint(3, 8)))

async def get_player_set(prompt):
    while True:
        user_input = (await async_input(prompt)).strip()
        if not user_input:
            return set()
        parts = [x.strip() for x in user_input.split(',')]
        if all(x.isdigit() for x in parts):
            return {int(x) for x in parts}
        print('Invalid input, only numbers and commas are accepted. Please try again.')


async def probe_single_set(target_set, guessed_set, hard_mode, current_energy):
    costs = {
        'len': 1, 'min': 4, 'max': 4, 'sum': 4,
        'disjoint': 2, 'subset': 3, 'superset': 3,
        'intersection': 6, 'union': 8, 'minus': 8, 'symmetric_difference': 7
    }
    print('Methods: [len], [min], [max], [sum], [subset], [superset], [disjoint], [intersection], [union], [minus], [symmetric_difference]')
    op = (await async_input('Choose a function: ')).strip().lower()
    if op not in costs:
        print('Unknown function.')
        return 0
    cost = costs[op] if hard_mode else 0
    if hard_mode and cost > current_energy:
        print(f'Insufficient energy. {op} costs {cost} energy, but you only have {current_energy}.')
        return 0
    no_input_ops = {
        'len': lambda: f'Length is {len(target_set)}',
        'min': lambda: f'Minimum value is {min(target_set)}' if target_set else 'Set is empty',
        'max': lambda: f'Maximum value is {max(target_set)}' if target_set else 'Set is empty',
        'sum': lambda: f'Sum of elements is {sum(target_set)}'
    }
    if op in no_input_ops:
        print(f'Result: {no_input_ops[op]()}')
        return cost
    test_set = await get_player_set(f'Enter your custom set for {guessed_set} (e.g, 1,2,3): ')
    operations = {
        'subset': lambda: test_set.issubset(target_set),
        'superset': lambda: test_set.issuperset(target_set),
        'disjoint': lambda: test_set.isdisjoint(target_set),
        'intersection': lambda: test_set.intersection(target_set),
        'union': lambda: test_set.union(target_set),
        'minus': lambda: target_set.difference(test_set),
        'symmetric_difference': lambda: test_set.symmetric_difference(target_set)
    }
    print(f'Result: {operations[op]()}')
    return cost


async def compare_hidden_sets(set_a, set_b, hard_mode, current_energy):
    costs = {'subset': 5, 'superset': 5, 'disjoint': 4, 'intersection': 8, 'union': 10, 'minus': 10, 'symmetric_difference': 9}
    print('Methods: [subset], [superset], [disjoint], [intersection], [union], [minus], [symmetric_difference]')
    op = (await async_input('Choose a function: ')).strip().lower()
    if op not in costs:
        print('Unknown function.')
        return 0
    cost = costs[op] if hard_mode else 0
    if hard_mode and cost > current_energy:
        print(f'Insufficient energy. {op} costs {cost} energy, but you only have {current_energy}.')
        return 0
    operations = {
        'subset': lambda: set_a.issubset(set_b),
        'superset': lambda: set_a.issuperset(set_b),
        'disjoint': lambda: set_a.isdisjoint(set_b),
        'intersection': lambda: set_a.intersection(set_b),
        'union': lambda: set_a.union(set_b),
        'minus': lambda: set_a.difference(set_b),
        'symmetric_difference': lambda: set_a.symmetric_difference(set_b)
    }
    print(f'Result: {operations[op]()}')
    return cost


async def check_final_guess(set_a, set_b):
    guess_a = await get_player_set("Final Guess on the elements in Set A: ")
    guess_b = await get_player_set("Final Guess on the elements in Set B: ")
    if guess_a == set_a and guess_b == set_b:
        print("\nCorrect. You figured out both sets.")
        return True
    else:
        print(f"\nWrong!\n Set A was {set_a},\n Set B was {set_b}.")
        return False


def show_game_info():
    print(
    '''\nGAME MANUAL & METHOD DESCRIPTIONS
    Deduce the contents of two hidden sets (A and B) containing unique integers from 1-20.
    In Normal Mode, you have infinite energy. In Hard Mode, you start with 25 energy.
    If your energy hits 0, you are soft-locked from querying and must guess.

    What each method does:
    - len                  : Returns the total number of elements in the hidden set.
    - min / max            : Returns the lowest or highest integer contained in the set.
    - sum                  : Returns the added total value of all numbers inside the set.
    - disjoint             : Returns True if your set shares ZERO numbers with the hidden set.
    - subset               : Returns True if ALL numbers in your custom set exist in the hidden set.
    - superset             : Returns True if the hidden set contains ALL numbers you provided and more.
    - intersection         : Returns only the numbers shared between your set and the hidden set.
    - union                : Combines your custom set and the hidden set, showing all numbers combined.
    - minus                : Subtracts your custom numbers from the hidden set, revealing what is left over.
    - symmetric_difference : Returns elements in either your set or the hidden set, but NOT in both.

    Single Set Probes:
    - len / min / max / sum  : 1 / 4 / 4 / 4 energy
    - disjoint               : 2 energy
    - subset / superset      : 3 energy
    - intersection           : 6 energy
    - symmetric_difference   : 7 energy
    - union / minus          : 8 energy

    Cross-Set Comparisons (A vs B):
    - disjoint               : 4 energy
    - subset / superset      : 5 energy
    - intersection           : 8 energy
    - symmetric_difference   : 9 energy
    - union / minus          : 10 energy    
    
    COMMAND SYNTAX
    ---------------
    probe <a|b> <op> [set]   Query Set A or B
                             Examples:  probe a len
                                        probe b min
                                        probe a subset 1,2,3
                                        probe b disjoint 4,5,6

    compare <op>              Compare Set A vs Set B
                             Examples:  compare subset
                                        compare union
                                        compare intersection

    guess                     Make your final guess for both sets
    info                      Show this manual
    clear                     Clear the terminal screen
    quit                      Exit and reveal the hidden sets''')


async def execute_single_probe(target_set, target_name, op, test_set_str, hard_mode, energy):
    """Direct version of probe_single_set that already has the op and optional test set."""
    costs = {
        'len': 1, 'min': 4, 'max': 4, 'sum': 4,
        'disjoint': 2, 'subset': 3, 'superset': 3,
        'intersection': 6, 'union': 8, 'minus': 8, 'symmetric_difference': 7
    }
    if op not in costs:
        print('Unknown function.')
        return 0
    cost = costs[op] if hard_mode else 0
    if hard_mode and cost > energy:
        print(f'Insufficient energy. {op} costs {cost} energy, but you only have {energy}.')
        return 0

    no_input_ops = ['len', 'min', 'max', 'sum']
    if op in no_input_ops:
        if op == 'len':
            result = f'Length is {len(target_set)}'
        elif op == 'min':
            result = f'Minimum value is {min(target_set)}' if target_set else 'Set is empty'
        elif op == 'max':
            result = f'Maximum value is {max(target_set)}' if target_set else 'Set is empty'
        elif op == 'sum':
            result = f'Sum of elements is {sum(target_set)}'
        print(f'Result: {result}')
        return cost

    if test_set_str is None:
        print('This operation requires a custom set. Usage: probe <a|b> <op> <numbers>')
        return 0

    test_set = parse_set_from_string(test_set_str)
    if test_set is None:
        print('Invalid set format. Use comma-separated numbers, e.g., 1,2,3')
        return 0

    if op == 'subset':
        result = test_set.issubset(target_set)
    elif op == 'superset':
        result = test_set.issuperset(target_set)
    elif op == 'disjoint':
        result = test_set.isdisjoint(target_set)
    elif op == 'intersection':
        result = test_set.intersection(target_set)
    elif op == 'union':
        result = test_set.union(target_set)
    elif op == 'minus':
        result = target_set.difference(test_set)
    elif op == 'symmetric_difference':
        result = test_set.symmetric_difference(target_set)
    else:
        result = 'Unknown operation'

    print(f'Result: {result}')
    return cost


def parse_set_from_string(s):
    """Convert a string like '1,2,3' to a set of ints. Returns None if invalid."""
    if not s.strip():
        return set()
    parts = s.split(',')
    cleaned = [p.strip() for p in parts if p.strip()]
    if all(p.isdigit() for p in cleaned):
        return {int(p) for p in cleaned}
    return None


async def execute_compare(set_a, set_b, op, hard_mode, energy):
    """Direct compare without sub‑prompt."""
    costs = {'subset': 5, 'superset': 5, 'disjoint': 4, 'intersection': 8, 'union': 10, 'minus': 10, 'symmetric_difference': 9}
    if op not in costs:
        print('Unknown function.')
        return 0
    cost = costs[op] if hard_mode else 0
    if hard_mode and cost > energy:
        print(f'Insufficient energy. {op} costs {cost} energy, but you only have {energy}.')
        return 0

    if op == 'subset':
        result = set_a.issubset(set_b)
    elif op == 'superset':
        result = set_a.issuperset(set_b)
    elif op == 'disjoint':
        result = set_a.isdisjoint(set_b)
    elif op == 'intersection':
        result = set_a.intersection(set_b)
    elif op == 'union':
        result = set_a.union(set_b)
    elif op == 'minus':
        result = set_a.difference(set_b)
    elif op == 'symmetric_difference':
        result = set_a.symmetric_difference(set_b)
    else:
        result = 'Unknown operation'

    print(f'Result: {result}')
    return cost


async def play_game():
    set_a, set_b = generate_hidden_sets()
    print('The computer has generated two hidden sets: Set A and Set B.')
    print('Values are integers between 1 and 20.')
    print('Query them using set operations to deduce their exact values.\n')
    print('Modes: [1] Normal Mode (Infinite Energy) | [2] Hard Mode (25 Energy)')
    while True:
        mode_choice = (await async_input('Select game mode (1 or 2): ')).strip()
        if mode_choice in ('1', '2'):
            break
        print("Invalid choice. Please type '1' or '2'.")

    hard_mode = (mode_choice == '2')
    energy = 25 if hard_mode else float('inf')
    skip_energy = False
    active = True

    print("\nYou are now in the terminal. Type commands like: probe a len, compare subset, guess, info, clear, or quit")
    print("For custom set probes: probe a subset 1,2,3\n")
    print('To look up command syntaxes, type: [info].')

    while active:
        if hard_mode:
            print(f'Energy: {energy}')
        skip_energy = False    
        user_input = (await async_input('> ')).strip()
        if not user_input:
            continue

        parts = user_input.split()
        if not parts:
            continue

        cmd = parts[0].lower()

        if cmd == 'quit':
            print('Exiting game. The sets were:')
            print(f'Set A: {set_a}')
            print(f'Set B: {set_b}')
            break

        elif cmd == 'info':
            show_game_info()
            continue

        elif cmd == 'guess':
            if await check_final_guess(set_a, set_b):
                active = False
            continue

        elif cmd == 'probe':
            if len(parts) < 3:
                print('Usage: probe <a|b> <op> [set]')
                continue
            target = parts[1].lower()
            op = parts[2].lower()
            test_set_str = None if len(parts) < 4 else parts[3]

            if target not in ('a', 'b'):
                print("Target must be 'a' or 'b'.")
                continue

            target_set = set_a if target == 'a' else set_b
            target_name = 'Presumed Set A' if target == 'a' else 'Presumed Set B'

            cost = await execute_single_probe(target_set, target_name, op, test_set_str, hard_mode, energy)
            energy = max(0, energy - cost)
            continue

        elif cmd == 'compare':
            if len(parts) < 2:
                print('Usage: compare <op>')
                continue
            op = parts[1].lower()
            cost = await execute_compare(set_a, set_b, op, hard_mode, energy)
            energy = max(0, energy - cost)
            continue

        elif cmd == 'clear':
            skip_energy = True
            if 'IN_PYODIDE' in globals():
                clear_output()
            else:
                # Since os.system is deprecated.
                print('\033[2J\033[H', end='')
            continue
        
        else:
            print(f"Unknown command '{cmd}'. Available: probe, compare, guess, info, quit")
            continue


if __name__ == '__main__':
    if 'IN_PYODIDE' not in dir():
        asyncio.run(play_game())