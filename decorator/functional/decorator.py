
# Write a decorator that tells you about it's working

def decorator(func):
    def wrapper(*args, **kwargs):
        updated_name = f"Mr/Mrs. {args[0]}"
        updated_msg = f"{args[1]} Probably, You are enjoying."
        print(f"Before : {args[0]} || {args[1]}")
        result = func(updated_name, updated_msg)
        print(f"After : {args[0]} -> {updated_name} || {args[1]} -> {updated_msg}")
        return result
    return wrapper

@decorator
def greetings(name: str, msg: str = ""):
    default = "Welcome to decorator world."
    greet = f"Hi {name}, {msg or default}"
    return greet


if __name__ == "__main__":
    # before decorator : testing function
    name = "Tester"
    msg = "How is your AI concepts knowledge?"
    '''If the decorator does not use @wraps, extract the original function from the closure first, then pass your parameters to it'''
    print(greetings.__closure__[0].cell_contents(name, msg))
    '''If your decorator uses @functools.wraps, pass the arguments straight into greetings.__wrapped__()'''
    # print(greetings.__wrapped__(name, msg))

    # after decorator : testing function
    print(greetings(name, msg))
