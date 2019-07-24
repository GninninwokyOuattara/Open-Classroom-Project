def encoded_then_sent(object , element, type_target):
    """Method for changing type of variables
    mostly integer to str, encode them and send them
    thru send method of object"""
    try:
        element = str(element)
        object.send(element.encode())
    except TypeError:
        print("Conversion impossible")
