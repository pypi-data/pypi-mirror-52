Ascii = {
    "special_chars1": [chr(i) for i in range(32, 48)],
    "numbers": [chr(i) for i in range(48, 58)],
    "special_chars2": [chr(i) for i in range(58, 65)],
    "big_letters": [chr(i) for i in range(65, 91)],
    "special_chars3": [chr(i) for i in range(91, 97)],
    "little_letters": [chr(i) for i in range(97, 123)],
    "special_chars4": [chr(i) for i in range(123, 127)],
}


class Revertable(object):
    @staticmethod
    def convert(string=None):
        result = ""
        for char in string:
            if (
                char not in Ascii["numbers"]
                and char not in Ascii["big_letters"]
                and char not in Ascii["little_letters"]
            ):
                result = result + "_"
                for nums in char.encode():
                    result = result + str(nums) + "x"
                result = result[0:-1] + "_"
            else:
                result = result + char
        return result

    @staticmethod
    def revert(string=None):
        result = ""
        special = False
        digits = ""
        digitlist = bytearray()
        for char in string.encode():
            if chr(char) == "x" and special:
                digitlist.append(int(digits))
                digits = ""
                continue
            if chr(char) == "_" and special:
                special = False
                digitlist.append(int(digits))
                result = result + digitlist.decode("utf8")
                digitlist = bytearray()
                digits = ""
                continue
            elif chr(char) == "_" and not special:
                special = True
                continue
            if not special:
                result = result + chr(char)
            else:
                digits = digits + chr(char)
        return result


if __name__ == "__main__":
    print("It works!")
