from command_registry import CommandRegistry

# exception for planned session end
class SessionEnd(KeyboardInterrupt):
    "Raised when bot is asked to be closed."
    pass

# base commands
def close_bot():
    raise SessionEnd

def hello():
    return "How can I help you?"




