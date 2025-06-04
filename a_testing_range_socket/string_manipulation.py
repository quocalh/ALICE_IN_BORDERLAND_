import numpy

def string_the_pos(array: tuple):
    assert len(array) == 2, "a given array must only have 2 elements"
    str = f"({array[0]}, {array[1]})"
    return str

def int_the_pos(string: str):
    array =  (string[1:-1].split(","))
    array = list(map(float, array))
    assert len(array) == 2, "a given array cannot have more than 2 elements"
    return array

if __name__ == "__main__":

    string_pos = string_the_pos((200, 300))

    print(string_pos, type(string_pos).__name__)

    print(int_the_pos(string_pos), type(int_the_pos(string_pos)).__name__)