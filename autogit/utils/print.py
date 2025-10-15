def print_failure(message: str) -> None:
    return print('\n\033[1;31m' + message.center(79, ' ') + '\033[0m')
