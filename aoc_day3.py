import re

def load_engine_schematic(file):
    with open(file) as f:
        engine_schematic = f.readlines()
        engine_schematic = [x.strip() for x in engine_schematic]
    return engine_schematic

def get_surrounding(row_span,line_nr, engine_schematic):
    surrounding = ''

    j_start = max(row_span[0]-1, 0)
    j_end = min(row_span[1]+1, len(engine_schematic[line_nr])-1)

    i_prev = max(line_nr-1, 0)
    i_next = min(line_nr+1, len(engine_schematic)-1)

    for x in range(i_prev, i_next+1):
        surrounding += engine_schematic[x][j_start:j_end]
    
    return surrounding

def is_part_number(surrounding, symbols):
    if set(surrounding) & set(symbols):
        return True
    return False

def calc_part_sum(engine_schematic):
    
    symbols = re.findall(r'[^0-9.]+', ''.join(engine_schematic))

    part_sum=0
    for i in range(len(engine_schematic)):
        find_numbers = re.finditer(r'\d+', engine_schematic[i])
        line_numbers = [(n.group(), n.span()) for n in find_numbers]

        for number, row_span in line_numbers:
            surrounding = get_surrounding(row_span, i, engine_schematic)

            if is_part_number(surrounding, symbols):
                part_sum+=int(number)
    
    return part_sum

def get_gear_numbers(gear_span, line_nr, engine_schematic):
    gear_numbers = []

    i_start = max(line_nr-1, 0)
    i_end = min(line_nr+1, len(engine_schematic)-1)

    for i in range(i_start, i_end+1):
        find_numbers = re.finditer(r'\d+', engine_schematic[i])
        line_numbers = [(n.group(), n.span()) for n in find_numbers]

        for number, number_span in line_numbers:
            if abs(number_span[0]- gear_span[0]) <= 1 or abs(number_span[1] - gear_span[1]) <= 1:
                gear_numbers.append(int(number))

    return gear_numbers

def calc_gear_ratio(engine_schematic):
    gear_ratio = 0

    for i in range(len(engine_schematic)):
        if '*' in engine_schematic[i]:
            find_gear = re.finditer('\*', engine_schematic[i])
            gears = [(n.group(), n.span()) for n in find_gear]
            for gear in gears:
                get_numbers = get_gear_numbers(gear[1], i, engine_schematic)
                if len(get_numbers) == 2:
                    gear_ratio += get_numbers[0] * get_numbers[1]
    
    return gear_ratio

if __name__ == '__main__':
    # Part 1 (I created test cases to debug my code)
    engine_schematic_testcase0 = load_engine_schematic('aoc_day3_example.txt')
    assert calc_part_sum(engine_schematic_testcase0) == 4361

    engine_schematic_testcase1 = load_engine_schematic('aoc_day3_testcase1.txt')
    assert calc_part_sum(engine_schematic_testcase1) == 5862

    engine_schematic_testcase2 = load_engine_schematic('aoc_day3_testcase2.txt')
    assert calc_part_sum(engine_schematic_testcase2) == 5725

    engine_schematic = load_engine_schematic('aoc_day3_input.txt')
    print('Part 1 result:', calc_part_sum(engine_schematic))

    # Part 2
    assert calc_gear_ratio(engine_schematic_testcase0) == 467835

    assert calc_gear_ratio(engine_schematic_testcase1) == 7792

    assert calc_gear_ratio(engine_schematic_testcase2) == 0

    print('Part 2 result:', calc_gear_ratio(engine_schematic))
