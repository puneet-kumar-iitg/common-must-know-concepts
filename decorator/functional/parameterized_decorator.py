def parameterized_decorator(role: str):

    def decorator(func):
        def wrapper(*args, **kwargs):
            if role == 'admin':
                return func(f"{role.capitalize()} {args[0]}", args[1])
            return "Don't have work to do. You are lucky"
        return wrapper

    return decorator

@parameterized_decorator('admin')
def greetings(name: str, msg: str = ""):
    default = "Welcome to decorator world."
    greet = f"Hi {name}, {msg or default}"
    return greet



if __name__ == "__main__":
    name = "Tester"
    msg = "How is your AI concepts knowledge?"
    # after decorator : testing function
    print(greetings(name, msg))
