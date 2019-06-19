#PASSED
# ATM machines allow 4 or 6 digit PIN codes and PIN codes cannot contain anything but exactly 4 digits or exactly 6 digits.
#
# If the function is passed a valid PIN string, return true, else return false.
#


def validate_pin(pin):
    #make sure it's a string:
    if not type(pin) is str:
        return False
    #make sure it's an acceptable length:
    if (len(pin) != 4) and (len(pin) != 6):
        return False
    #make sure it only contains integers:
    for c in pin:
        n = ord(c) #ord() gets us the ascii code for this character
        if n<48 or n>57:
            return False

    #if we haven't returned False by this point, it must be a valid pin
    return True

# eg:
#
# validate_pin("1234") == True
# ans = validate_pin("1234")
# ans = validate_pin("12345")# == False
ans = validate_pin("a234") # == False

print(ans)
