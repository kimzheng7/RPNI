import random
import string

def extend_string(curr_str, curr_chars):
    next_char = random.choice(curr_chars)
    # Wildcard instantiates to random character
    if next_char == ".":
        next_char = random.choice(string.ascii_letters)

    return curr_str + next_char

def generate(re):
    generated_string = ""
    special_chars = ["*", "+"]

    i = 0
    while i < len(re):
        curr_chars = []

        # If current character isn't of the form (|), then the current string is just the character
        if re[i] != "(":
            curr_chars.append(re[i])
        else:
            # If current character is of the form (|), then current strings is list of characters delimited by |
            i += 1
            while re[i] != ")":
                if re[i] != "|":
                    curr_chars.append(re[i])
                i += 1

        # If the next character is special
        if (i + 1) < len(re) and re[i + 1] in special_chars:
            i += 1
            if re[i] == "+":
                generated_string = extend_string(generated_string, curr_chars)
            
            # Apply Kleene star
            add_next = random.choice([True, False])
            while add_next:
                generated_string = extend_string(generated_string, curr_chars)
                add_next = random.choice([True, False])
        else:
            # Otherwise, just add character
            generated_string = extend_string(generated_string, curr_chars)

        i += 1

    return generated_string

if __name__ == "__main__":
    re = "hello!* are you okay?+ ye(p|a)+"

    samples = []
    for i in range(10):
        samples.append(generate(re))

    print(samples)
