import re
import random


def StringToListBytes(string:str) -> list:
    output_list_bytes = []

    for char in string:
        output_list_bytes.append(hex(ord(char)))
    
    return output_list_bytes

def StringBytesToListBytes(string_bytes:str) -> list:
    regex_pattern_find_hex_byte = "[a-fA-F0-9]{2}"
    output_list_bytes = []

    List_bytes = re.findall(regex_pattern_find_hex_byte, string_bytes)
    for byte in List_bytes:
        output_list_bytes.append("0x"+byte)
    
    return output_list_bytes

def ListBytesToStringBytesDefineCapl(list_bytes:list) -> str:
    tmp_string = "{"
    for byte in range(0, len(list_bytes)):
        # at end of list
        if byte == (len(list_bytes)-1):
            tmp_string += f"{list_bytes[byte]}" + "}"
        # not at end of list
        else:
            tmp_string += f"{list_bytes[byte]}, "

    output_string_bytes_define_capl = f"[{len(list_bytes)}] = {tmp_string};"
    
    return output_string_bytes_define_capl

def GenRandomValueWithRangeToListBytes(num_bytes, range_min:int, range_max:int) -> list:
    output_list = []

    for byte in range(0, int(num_bytes)):
        random_value = random.randint(range_min, range_max)
        output_list.append("0x%02X" % random_value)
    
    return output_list

def ListBytesToStringWithSeperator(list_bytes:list, seperator:str) -> str:
    tmp_string = ""

    for byte in range(0, len(list_bytes)):
        # at end of list
        if byte == (len(list_bytes)-1):
            tmp_string += f"{list_bytes[byte]}"
        # not at end of list
        else:
            tmp_string += f"{list_bytes[byte]}" + seperator
    
    return tmp_string

def SearchKeyWordInlistReturnMatch(key_word_list:list, list_to_search:list) -> list:
    matched_flag = False
    output_matches_list = []
    
    for item in list_to_search:
        matched_flag = True
        for key_word in key_word_list:
            if key_word not in item:
                matched_flag = False
                break
        if matched_flag == True:
            output_matches_list.append(item)

    return output_matches_list

def SearchKeyWordInString(key_word_list:list, string_to_search:str) -> bool:

    for key_word in key_word_list:
        if key_word == None:
            continue
        if key_word.lower() not in string_to_search.lower():
            return False
    else:
        return True

def SearchKeyWordNotInString(key_word_list:list, string_to_search:str) -> bool:

    for key_word in key_word_list:
        if key_word == None:
            continue
        if key_word.lower() in string_to_search.lower():
            return False
    else:
        return True

def ListStringToStringEndLine(input_list_string:list):
    output_string = ""

    for string in input_list_string:
        output_string += string + "\n"

    return output_string