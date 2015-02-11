#   Script Name :   string_management.py
#   Author      :   Logan McCamish
#   Created     :   Saturday, February 7th
#   Purpose     :   This script takes in a string or file of strings and
#       a) Reverses the string if its length is a multiple of 4.
#       b) Truncates the string to 5 characters if its length is a multiple of 5.
#       c) Converts the string to all uppercase if it contains at least 3 uppercase characters in the first 5 characters.
#       d) If the string ends with a hyphen, removes it, and appends the next string in the list to the current one.
#       e) Prints the string out.
#       f) Calculates the median length of strings.
#       g) Counts the number of letters in the input file.
#       h) Counts the number of letters in the output file.


#   Here we define the output file that we write to.
output_file = "output.txt"


#   This method reverses a string if it's length is a multiple of 4
def reverse_string(to_reverse):
    if len(to_reverse) % 4 == 0:
        # While we could use 'to_reverse[::-1]' (a usage of extended slicing) to reverse the string faster,
        # I chose this implementation for the sake of readability.
        return ''.join(reversed(to_reverse))
    return to_reverse


#   This method truncates a string to 5 characters if the string length is a multiple of 5.
#       Note:
#       this uses Python slice syntax: https://docs.python.org/2/library/functions.html#slice
def truncate(to_truncate):
    if len(to_truncate) % 5 == 0:
        return to_truncate[:5]  # Gets characters from index 0 (inclusive) to 6 (exclusive)
    return to_truncate


#   This method converts the string to upper case if 3 out of the 5 first characters are already uppercase.
#       Note:
#       this uses Python slice syntax: https://docs.python.org/2/library/functions.html#slice
def to_uppercase(uppercase):
    num_upper = 0
    for letter in uppercase[:5]:  # Gets characters from index 0 (inclusive) to 6 (exclusive)
        if letter.upper() == letter:
            num_upper += 1
    if num_upper >= 3:
        return uppercase.upper()
    return uppercase


#   Checks if the last character is a hyphen. If so, removes the hyphen and appends the next string hyphened one.
#       Note:
#       this uses Python slice syntax: https://docs.python.org/2/library/functions.html#slice
def hyphen_check(hyphened, next_str):
    if hyphened[-1] == '-':
        return hyphened[:-1] + next_str
    return hyphened


#   This strips punctuation before and after a word, and prints it.
def pretty_print(word_list):
    output = " ".join(word_list)
    print(output)
    return output


#   Parses the input file, storing the value in string_list,
#  and counts the number of characters, storing them in input_count.
def parse_file():
    string_list = []
    input_count = 0
    print("What list of strings would you like to print?")
    file_name = raw_input("=> ")
    try:
        with open(file_name.encode('string-escape'), 'r') as input_file:
            for line in input_file:
                input_count += len(line)
                for word in line.split():
                    string_list.append(word)
    except IOError as e:
        print("Could not parse file - ({0}): {1}".format(e.errno, e.strerror))

    return string_list, input_count


# This function collects and prints the output info
def print_output_info(output_list):
    output = pretty_print(output_list)

    # This sorts the list by length from smallest to largest.
    output_list.sort(key=len)
    median = output_list[len(output_list)/2]
    word_count = len(output_list)
    print("\n\nThe output has a median string length of {0}, a word count of {1}, and a character count of {2}. "
          .format(len(median), word_count, len(output)))
    print("It now reads: \n\"" + output + "\",\n and is printed to \"{0}\"").format(output_file)
    write_output(output)


# We write to our output file in this function
def write_output(output):
    try:
        with open(output_file, 'w') as o_file:
            o_file.write(output)
    except IOError as e:
        print("Could not write to file - ({0}): {1}".format(e.errno, e.strerror))


def main():
    word_list, count = parse_file()
    print_list = []
    sorted_input = sorted(word_list, key=len)
    median = len(sorted_input)/2
    print("the list of strings has {0} characters in it, composed of {1} words, with a median length of {2}."
          .format(count, len(word_list), len(sorted_input[median])))
    i = 1

    # We choose to join hyphens first, as we modify the list in the process.
    while i < len(word_list):
        word = hyphen_check(word_list[i-1], word_list[i])
        if word == word_list[i-1]:  # If our word doesn't change, we keep going.
            i += 1
        else:  # else we remove the word we joined, and change the old un-hyphenated one to the new, conjoined word
            word_list.pop(i)
            word_list[i-1] = word

    # Here we run our words through their various tests, then print the result.
    for word in word_list:
        word = reverse_string(word)
        word = truncate(word)
        word = to_uppercase(word)
        print_list.append(word)
        print(word)

    # Here we find the median value, and print the median, number of words, and number of characters, and write to file
    print_output_info(print_list)


if __name__ == '__main__':
    main()