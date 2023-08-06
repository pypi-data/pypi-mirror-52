from pack_preprocess import (name_to_code, soundex_modified)
from pack_utils_namematching import (validate_name_1,check)


def single_compare(s1,s2):
    
    if not s1.strip() or not s2.strip() :
        print('Invalid Input')
        return
    if s1.strip() == s2.strip():
        print('Match')
        return
    answer = name_to_code(s1)
    answer_1 = name_to_code(s2)
    
    #comparing company -name case
    if answer[1] != answer_1[1]:
        print('Not Match')
        return
    
    else:
        name_combo = validate_name_1(answer[0])
        final_code_list = []
        
        # Creating final_code_list which contains soundex of each combo name.
        for name in name_combo:
            preprocessed_name = name.split()
            code_list = []
            for words in preprocessed_name:
                try:
                    code_list.append(soundex_modified(words))
                except:
                    code_list.append(words)

            final_code = ' '.join(code_list)
            final_code_list.append(final_code)

        if answer_1[2] in final_code_list:
            if (check(answer[0],answer_1[0])) == 'Match':
                print('Match')
                return
            else:
                print('Not Match')
                return    
        else:
            
            name_combo_x = validate_name_1(answer_1[0])
            
            final_code_list_x = []
           # Creating final_code_list which contains soundex of each combo name.
            for name_x in name_combo_x:
                preprocessed_name_x = name_x.split()
                code_list_x = []
                for words_x in preprocessed_name_x:
                    try:
                        code_list_x.append(soundex_modified(words_x))
                    except:
                        code_list_x.append(words_x)

                final_code_x = ' '.join(code_list_x)
                final_code_list_x.append(final_code_x)
 
            if answer[2] in final_code_list_x:
                
                if (check(answer_1[0],answer[0])) == 'Match':
                    print('Match')
                    return
                else:
                    print('Not Match')
                    return
            else:
                print('Not Match')
                return


single_compare('jaten','jatin')