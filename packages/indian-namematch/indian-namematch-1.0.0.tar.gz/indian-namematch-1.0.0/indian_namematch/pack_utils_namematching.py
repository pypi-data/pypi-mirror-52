''' Deals with creating name combinations and validating it.'''
from itertools import permutations
from pack_preprocess import soundex_modified


def validate_name_1(ORIGINAL_NAME, PROVIDED_NAME=None):
    ORIGINAL_NAME = ORIGINAL_NAME.lower()
    PROVIDED_NAME = PROVIDED_NAME.lower() if PROVIDED_NAME else None

    # Check if both the names are equal
    if ORIGINAL_NAME == PROVIDED_NAME:
        return True

    ORIGINAL_NAME = [x.strip() for x in ORIGINAL_NAME.split(' ') if x]
    FAMILY_NAME = ORIGINAL_NAME[-1]
    OTHER_NAME = ORIGINAL_NAME[:-1]
    NAME_COMBINATIONS = []

    # Validating name based of permutations
    for i in range(1, len(ORIGINAL_NAME) + 1):
        combi = list(permutations(ORIGINAL_NAME, i))
        for _ in combi:
            if not PROVIDED_NAME:
                NAME_COMBINATIONS.append(' '.join(_))
            else:
                if PROVIDED_NAME == ' '.join(_):
                    return True

    # Validating based on initials
    for i in range(1, len(OTHER_NAME) + 1):
        combi = list(permutations(OTHER_NAME, i))
        for _ in combi:
            initials = [x[0] for x in _]
            _w = ''.join(initials) + ' ' + FAMILY_NAME
            _x = ' '.join(initials) + ' ' + FAMILY_NAME

            _p = FAMILY_NAME + ' ' + ''.join(initials)
            _q = FAMILY_NAME + ' ' + ' '.join(initials)

            if not PROVIDED_NAME:
                for _ in (_w, _x, _p, _q):
                    NAME_COMBINATIONS.append(_)
            else:
                if PROVIDED_NAME in (_w, _x, _p, _q):
                    return True

        for texts in combi:
            if len(texts) > 1:
                first_pos = texts[0][0]
                remainings = list(texts[1:])
                remainings.append(first_pos)
                _w = ' '.join(remainings) + ' ' + FAMILY_NAME
                _x = FAMILY_NAME + ' ' + ' '.join(remainings)

                if not PROVIDED_NAME:
                    for _ in (_w, _x):
                        NAME_COMBINATIONS.append(_)
                else:
                    if PROVIDED_NAME in (_w, _x):
                        return True

    return list(set(NAME_COMBINATIONS)) if not PROVIDED_NAME else False


def vowels_between_consonants(name1):
    '''Vowels between consonants find the vowels mapping between consonant
       example: pradeeip-----> {a,eei}
    '''
    list_consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                       'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                       'y', 'z']
    # index list contains index where vowels are in name.
    # ans_list contains consonants between those vowels.

    index_list = []
    ans_list = []
    for index, item in enumerate(name1):
        if item in list_consonants:
            index_list.append(index)
    # checking if first character need to be appended
    if index_list[0] not in list_consonants:
        ans_list.append(name1[:index_list[0]])
    # obtaining values based on slicing of indexes
    for i in range(len(index_list)-1):
        ans_list.append(name1[index_list[i]+1:index_list[i+1]])
    # cheking for last sliced result
    if index_list[-1] < len(name1)-1:
        ans_list.append(name1[index_list[-1]+1:])
    # if any empty names in list, remove them.
    ans_list = list(filter(None, ans_list))
    return ans_list


def consonants_between_vowels(name1):
    '''Vowels between consonants find the vowels mapping between consonant
       example: pradeeip-----> {pr,d,p}
    '''
    list_vowels = ['a', 'e', 'i', 'o', 'u']
    # index list contains index where vowels are in name.
    # ans_list contains consonants between those vowels.
    index_list = []
    ans_list = []
    for index, item in enumerate(name1):
        if item in list_vowels:
            index_list.append(index)
    # checking if first character need to be appended
    if index_list[0] not in list_vowels:
        ans_list.append(name1[:index_list[0]])
    # obtaining values based on slicing of indexes
    for i in range(len(index_list)-1):
        ans_list.append(name1[index_list[i]+1:index_list[i+1]])
    # checking for last sliced result
    if index_list[-1] < len(name1)-1:
        ans_list.append(name1[index_list[-1]+1:])
    # if any empty names in list, remove them.
    ans_list = list(filter(None, ans_list))
    return ans_list


def final_check(part1, part2):
    ''' Final check basically checks where names don't have a mapping of never ever
        in it. example amit and amat ----{a matches with a} but
        { i dont matchws with a} , Hence it's not a match. '''
    
    never_ever = [('e', 'u'), ('u', 'e'), ('a', 'e'), ('a', 'i'), ('a', 'o'),
                  ('e', 'a'), ('i', 'a'), ('o', 'a'), ('e', 'o'), ('o', 'e'),
                  ('e', 'i'), ('i', 'e'), ('u', 'a'), ('a', 'u'), ('i', 'u'),
                  ('u', 'i'), ('ee', 'a'), ('a', 'ee'), ('ei', 'a'),
                  ('a', 'ei'), ('a', 'ea'), ('ea', 'a'), ('i', 'o'),
                  ('o', 'i'), ('nh', 'm'), ('m', 'nh'), ('m', 'n'),
                  ('n', 'm'), ('a', 'au'), ('nh', 'my'),
                  ('my', 'nh')]
    # checking name start and name end with same alphabet
    if (part1[0] != part2[0]) or (part1[-1] != part2[-1]):
        return 'Not Match'
    # getting list of vowel combo for name 1 and name 2 and zip them
    vowels_name1 = vowels_between_consonants(part1)
    vowels_name2 = vowels_between_consonants(part2)
    final_list = list(zip(vowels_name1, vowels_name2))
    # getting list of consonant combo for name 1 and name 2 and zip them
    con_name1 = consonants_between_vowels(part1)
    con_name2 = consonants_between_vowels(part2)
    final_list_con = list(zip(con_name1, con_name2))

    final_list = final_list + final_list_con
    
    flag = 'Match'
    for i in final_list:
        if i in never_ever:
            flag = 'Not Match'
            break
    return 'Match' if flag == 'Match' else 'Not Match'


def check(input_name, to_check_name):
    ''' Check function comapres the two name to give optimized
        Output from soundex name matches,
        selects similar words between two names and send it to final_check
    '''
    # contains output of no of matches and not matches
    out = []
    # create a dictionary of input name {input_name:code}
    splitted_input_name = input_name.split()
    code_input_code = [soundex_modified(i) for i in splitted_input_name]
    dic_input_dictionary = dict(zip(code_input_code, splitted_input_name))
    # create a dictionary of single characters instead of surname
    single_splitted_input_list = splitted_input_name[:-1]
    single_splitted_input_list = [i[0] for i in single_splitted_input_list]
    # create a dictionary of output name {output_name:code}
    splitted_check_name = to_check_name.split()
    code_check_name = [soundex_modified(i) for i in splitted_check_name]
    dic_output_dictionary = dict(zip(code_check_name, splitted_check_name))
    # Creating count and common_single to know common macthes of words,
    #  between two names.
    count = 0
    common_single = 0
    # Count contains names with >=3 characters.
    for i in splitted_check_name:
        if len(i) >= 3:
            count = count + 1
        if i in single_splitted_input_list:
            common_single = common_single + 1

    common_elements_list = list(set(code_input_code) & set(code_check_name))
    common = len(common_elements_list) + common_single
    # if all the words of to_check_name matches with input name
    # Then only we do final_check
    if (not common_elements_list) or (common < count):
        return 'Not Match'
    
    for i in common_elements_list:
        out.append(final_check(dic_input_dictionary[i], dic_output_dictionary[i]))
    
    return 'Not Match' if 'Not Match' in out else 'Match'

