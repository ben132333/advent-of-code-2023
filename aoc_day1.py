import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')
logging.disable(logging.DEBUG)

digit_dict = {
    'nine': '9',
    'eight': '8',
    'seven': '7',
    'six': '6',
    'five': '5',
    'four': '4',
    'three': '3',
    'two': '2',
    'one': '1'
}

def aoc_day1(doc):
    doc_list = doc.split('\n')
    solution = 0
    
    for line in doc_list:
        line = line.strip()
        logging.debug('Input  line: %s', line)

        matches = []

        for word, digit in digit_dict.items():
            finditer_matches = re.finditer(word, line)
            matches.extend([(match.start(), match.end(), word, digit) for match in finditer_matches])
        
        matches.sort(key=lambda x: x[0])
        for i in range(len(matches) - 1):
            if matches[i][1] > matches[i+1][0]:
                matches[i] = (matches[i][0], matches[i+1][1], line[matches[i][0]:matches[i+1][1]], matches[i][3]+matches[i+1][3])
                matches[i+1] = (0, 0, '', '')
        
        matches = [match for match in matches if match != (0, 0, '', '')]
        
        for match in matches:
            line = re.sub(match[2], match[3], line, count=1)
        
        digits = re.findall(r'\d', line)

        if len(digits) > 0:
            solution += int(digits[0] + digits[-1])

            logging.debug('Output line: %s', line)
            logging.debug('Extracted int: %s', int(digits[0] + digits[-1]))
            logging.debug('Solution: %s', solution)
            logging.debug(10*'- -')
    
    return solution
        

if __name__ == '__main__':
    with open('aoc_day1_input.txt', 'r') as file:
        example_doc = file.read()

    print(aoc_day1(example_doc))
