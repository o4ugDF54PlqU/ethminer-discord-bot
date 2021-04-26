import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

install('discord')
install('asyncpg')
install('requests')
install('imgkit')
install('GPUtil')
install('tabulate')
install('numpy')
install('pyautogui')