from colorama import Fore, Style


class TermCallback(object):
    """
    This class contains callbacks that should only be displayed when running runcible from the terminal, they are
    all run the instant they are called and aren't associated with any objects
    """

    @staticmethod
    def fatal(msg):
        print(f"{Fore.RED}{msg}{Style.RESET_ALL}")

    @staticmethod
    def info(msg):
        print(msg)

    @staticmethod
    def error(msg):
        print(f"{Fore.RED}{msg}{Style.RESET_ALL}")

    @staticmethod
    def success(msg):
        print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")
