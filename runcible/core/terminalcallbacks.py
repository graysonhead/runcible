from colorama import Fore, Style


class TermCallback(object):
    """
    This class contains callbacks that should only be displayed when running runcible from the terminal, they are
    all run the instant they are called and aren't associated with any objects
    """

    @staticmethod
    def fatal(msg, indent=False):
        indent = ""
        if indent:
            indent="    "
        print(f"{indent}{Fore.RED}{msg}{Style.RESET_ALL}")

    @staticmethod
    def info(msg, indent=False):
        indent = ""
        if indent:
            indent = "    "
        print(f"{indent}{msg}")

    @staticmethod
    def error(msg, indent=False):
        indent = ""
        if indent:
            indent = "    "
        print(f"{indent}{Fore.RED}{msg}{Style.RESET_ALL}")

    @staticmethod
    def success(msg, indent=False):
        indent = ""
        if indent:
            indent = "    "
        print(f"{indent}{Fore.GREEN}{msg}{Style.RESET_ALL}")

    @staticmethod
    def changed(msg, indent=False):
        indent = ""
        if indent:
            indent = "   "
        print(f"{indent}{Fore.YELLOW}{msg}{Style.RESET_ALL}")
