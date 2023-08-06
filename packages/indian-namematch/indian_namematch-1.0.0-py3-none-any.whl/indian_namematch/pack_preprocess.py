
"""
###################################################################################
# Pre-Processing of names
###################################################################################
"""
import re
import nltk

SAL_REM = ['smt', 'mrs', 'mr', 'ms', 'dr', 'col', 'lt', 'dr', 'dr(mrs)',
           'm.s.', 'm/s', 'messes', 'messesrs', 'messors', 'messres',
           'messrs', 'messsers', 'miss', 'misss', 'mistar', 'mr', 'mr.',
           'mrs', 'mrs,', 'ms', 'ms.', 'ms.shri', 'prof', 'prop.shri',
           'prop.smt', 'sh', 'sh.shri', 'shri', 'sm', 'smt', 'lt',
           'lt.', 'col ', 'col.', 'cl', 'cl.', 'cdr', 'cdr.',
           'captain', 'flight', 'lieutenant', 'colonel', 'commander',
           'lieutenant', 'brig', 'prop']

COMPANY_BIGRAMS_TO_REMOVE = {('priwate', 'limited'), ('priwate', 'ltd'),
                             ('pwt', 'limited'), ('pwt', 'ltd'), ('p', 'ltd'),
                             ('p', 'limited'), ('priwate', 'l'), ('pwt', 'l'),
                             ('corporation', 'limited'),
                             ('corporation', 'ltd'), ('corporation', 'l'),
                             ('corp', 'limited'), ('corp', 'ltd'),
                             ('corp', 'l'), ('cor', 'limited'), ('cor', 'ltd'),
                             ('cor', 'l'), ('co', 'limited'), ('p', 'l')}

REMOVE_ONLY_IN_CASE_OF_NAME = ['mazor']

COMPANY_SINGLE = {'pwt', 'priwate', 'limited', 'ltd', 'corporation', 'corp',
                  'cor', 'co', 'llp'}

REPLACE_BY_SPACE_RE = re.compile(r'[/(){}\.[\]\|@;]')

SINGLE_CHARACTER_PHONETICS = {'v': 'w', 'j': 'z', 'q': 'k'}

BIGRAM_CHARACTER_PHONETICS = {'ph': 'f', 'th': 't', 'dh': 'd', 'sh': 's',
                              'ck': 'k', 'gh': 'g', 'kh': 'k', 'ch': 'c'}



def soundex_modified(query):
    '''
    ----> Save the first letter. Map all occurrences of
          a, e, i, o, u, y, h, w. to zero(0)
    ----> Replace all consonants (include the first letter)
          with digits as in to_replace.
    ----> Replace all adjacent same digits with one digit, and then remove
          all the zero (0) digits
    ----> If the saved letter's digit is the same as the resulting first
          digit, remove the digit (keep the letter).
    ----> Append 3 zeros if result contains less than 3 digits.
          Remove all except first letter and 3 digits after it
          (This step same as [4.] in explanation above)

    ----> **** What we have handled.
          Soundex don't give output for single character,
          but name can be as A singh. Hence Soundex of
          A and singh both will be needed.

          Apart from that names like Joy
          after removal of a,e,i,o,u,h,w becomes only J
          Hence Joy soundex will become same as J,
          due to presence of o and y in name.

          So we don't create soundex of such names,
          to avoid extra matches and mismatches.
    '''
    query = query.lower()
    # handling single character case
    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = query[0]
    letters = query[1:]
    letters = [char for char in letters if char not in to_remove]
    # caring about cases where except 1 lettter all are vowels
    if not letters:
        return query

    to_replace = {('b', 'f', 'p', 'v'): 1,
                  ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}
    # creating code for each char using to_replace.
    first_letter = [value if first_letter else first_letter for group,
                    value in to_replace.items()
                    if first_letter in group]

    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]
    # Replace all adjacent same digits with one digit
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]
    # If the saved letter’s digit is the same the resulting first digit,
    # remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])
    # Append 3 zeros if result contains less than 3 digits.
    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string


def name_to_code(text):
    """
    This code can be devided into two parts.
    1st---> converts the name into preprocessed name
    2nd---> Takes that preprocess name and create
            columns required for search.

    All those columns are 'name_preprocessed','is_company' and 'soundex_code'

    Conversion to preprocess name:
    --->    special handling of {'m.s.','m/s','m/a','m/s.'}
    --->    used regex to remove all type of slashes and brackets
            ('[/(){}\\.[\\]\\|@;]')
    --->    removing every element of remove list
    --->    used regex to remove all numeric and special characters ('[^a-z]+')
    --->    used mapping1 of similar sounding words to replace
            {'v': 'w', 'j': 'z', 'q': 'k'}.
    --->    used mapping2 of similar words to remove of two alphabets
            {'ph': 'f', 'th': 't', 'dh': 'd', 'sh': 's',
            'ck':'k', 'gh': 'g', 'kh': 'k'}
    --->   using this preprocessed name columns are created such as
            soundex,is_company.
    """

    text = text.lower()

    # special cases
    text = text.replace('m/s', ' ')
    text = text.replace('m/a', ' ')
    text = text.replace('m/s.', ' ')
    text = text.replace('m.s.', ' ')

    # removing slashes and brackets
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    if not text.strip():
        return text.lower()

    # removing numeric words and special characters
    text = re.sub('[^a-z/ ]+', ' ', text)
    if not text.strip():
        return text.lower()

    # removing list of [dr,mr,ms....]
    text = text.replace('group captain', '')
    text = text.split()
    text = [x for x in text if x not in SAL_REM]
    if not text:
        return text.lower()

    # applying mapping 1 with consideration of special case,
    # consideration of special case  e to i

    new_text = []
    for word in text:
        word = 'i' + word[1:] if word[0] == 'e' else word
        for char in word[1:]:
            word = word.replace(char, SINGLE_CHARACTER_PHONETICS[char]) if char in SINGLE_CHARACTER_PHONETICS.keys() else word
        new_text.append(word)

    # applying mapping 2, for applying mapping 2 ,
    # we need to create character bi-character-grams:

    text = []
    for word in new_text:
        word_bigrams = [word[j:j+2] for j in range(len(word)-1)]
        for bigram in word_bigrams:
            word = word.replace(bigram, BIGRAM_CHARACTER_PHONETICS[bigram]) if bigram in BIGRAM_CHARACTER_PHONETICS.keys() else word
        text.append(word)

    name_preprocessed = ' '.join(text).strip()
    
    # value for new column company now
    
    text1 = set(text)
    single_common = COMPANY_SINGLE & text1
    is_company = 0
    if single_common:
        is_company = 1

    bigrams_words = set(nltk.bigrams(text))
    double_common = COMPANY_BIGRAMS_TO_REMOVE & bigrams_words
    if double_common:
        is_company = 1
    if 'industries' in text:
        is_company = 1

    # Special handling of word major
    if is_company == 0:
        text = [x for x in text if x not in REMOVE_ONLY_IN_CASE_OF_NAME]
        name_preprocessed = ' '.join(text).strip()

    # removing pwt..limite...etc from preprocessed_name
    if is_company == 1:
        # Taking Care of L case
        if text[-1] == 'l':
            text = text[:len(text)-1]
        if double_common:
            for ele in double_common:
                try:
                    text.remove(ele[0])
                    text.remove(ele[1])
                except:
                    pass

        if single_common:
            for ele in single_common:
                try:
                    text.remove(ele)
                except:
                    pass
        name_preprocessed = ' '.join(text)
    # value for new column soundex code
    soundex_code = []
    for word in text:
        try:
            soundex_code.append(soundex_modified(word))
        except:
            soundex_code.append(word)
    soundex_code = ' '.join(soundex_code)
    return name_preprocessed, is_company, soundex_code



def company_preprocess(answer):
    '''
    This function removes compant private and all those terms from it.
    '''
    ans = answer.split()
    ans_s = set(ans)
    single_common = COMPANY_SINGLE & ans_s

    bigrams_words = set(nltk.bigrams(ans))
    double_common = COMPANY_BIGRAMS_TO_REMOVE & bigrams_words

    if double_common:
        for ele in double_common:
            ans.remove(ele[0])
            ans.remove(ele[1])

    if single_common:
        for ele in single_common:
            try:
                ans.remove(ele)
            except:
                pass

    answer = ' '.join(ans)
    return answer

