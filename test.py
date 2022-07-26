from time import sleep
import asyncio

# def test1():
#     print(f'\r{1} of {2} ({3}%)', end='')


# def test2():
#     print(f'\n\rDownloading from {0} peers - ('
#             f'{1}/s▾ '
#             f'{2}/s▴) '
#             f'{3}', end='')

t = 0


while True:

    print(f'\r{t} of {2} ({3}%)')

    print(f'Downloading from {t} peers - ('
            f'{1}/s▾ '
            f'{2}/s▴) '
            f'{3}', end='')

    print('\033[1A', end='')
    # print('\033[1A')

    t+=1
    sleep(1)


