import json
from torrent import TorrentDownloader
from pirate_search import ThePirateBayCrawler

name = '''

                                            _____ _   _ _____ ____ ___ ____      _  _____ _____ ____    _ __   __ 
                                           |_   _| | | | ____|  _ \_ _|  _ \    / \|_   _| ____| __ )  / \\ \ / /    
                                             | | | |_| |  _| | |_) | || |_) |  / _ \ | | |  _| |  _ \ / _ \\ V / 
                                             | | |  _  | |___|  __/| ||  _ <  / ___ \| | | |___| |_) / ___ \| |  
                                             |_| |_| |_|_____|_|  |___|_| \_\/_/   \_\_| |_____|____/_/   \_\_|  
                                                                                                                 
                                                                     ____ _     ___ 
                                                                    / ___| |   |_ _|
                                                                   | |   | |    | | 
                                                                   | |___| |___ | | 
                                                                    \____|_____|___|
                                           
'''

piratesearcher = ThePirateBayCrawler()
downloader = TorrentDownloader()


def _choice(args):
    choice = int(input('> '))
    if choice < 1 or choice > len(args): raise Exception
    return choice
        
def _table(args):
    hash_size = 152
    hashes = '#'*hash_size
    print('\n')
    for index, arg in enumerate(args[::-1]):
        print(hashes)
        print('#{}#'.format( f'{len(args)-index} - {arg.capitalize()}'.center(hash_size-2)))
    print(f'{hashes}\n\n')
    return _choice(arg)

def _get_categories():
    categories = {
        'All': 0,
        # Audio
        'Music (Audio)': 101,
        'Audio books (Audio)': 102,
        'Sound clips (Audio)': 103,
        'FLAC (Audio)': 104,
        'Other (Audio)': 199,

        # Videos
        'Movies (Videos)': 201,
        'Movies DVDR (Videos)': 202,
        'Music videos (Videos)': 203,
        'Movie clips (Videos)': 204,
        'TV shows (Videos)': 205,
        'Handheld (Videos)': 206,
        'HD - Movies (Videos)': 207,
        'HD - TV shows (Videos)': 208,
        '3D (Videos)': 209,
        'Other (Videos)': 299,

        # Programs
        'Windows (Programs)': 301,
        'Mac (Programs)': 302,
        'UNIX (Programs)': 303,
        'Handheld (Programs)': 304,
        'IOS (iPad/iPhone) (Programs)': 305,
        'Android (Programs)': 306,
        'Other OS (Programs)': 399,

        # Games
        'PC (Games)': 401,
        'Mac (Games)': 402,
        'PSx (Games)': 403,
        'XBOX360 (Games)': 404,
        'Wii (Games)': 405,
        'Handheld (Games)': 406,
        'IOS (iPad/iPhone) (Games)': 407,
        'Android (Games)': 408,
        'Other (Games)': 499,

        # Porn
        'Movies (Porn)': 501,
        'Movies DVDR (Porn)': 502,
        'Pictures (Porn)': 503,
        'Games (Porn)': 504,
        'HD - Movies (Porn)': 505,
        'Movie clips (Porn)': 506,
        'Other (Porn)': 599,

        # Other
        'E-books (Other)': 601,
        'Comics (Other)': 602,
        'Pictures (Other)': 603,
        'Covers (Other)': 604,
        'Physibles (Other)': 605,
        'Other (Other)': 699
    }

    return categories

def _category_code(cat):
    return list(_get_categories().keys())[cat-1]

def search():
    cat = input('\nFilter by category?[y/N]\n\n>')

    if cat.upper() in ('Y', 'YES'):
        cat = _table(list(_get_categories().keys()))
        cat = _category_code(cat)
    else:
        cat = 'All'

    search = input('Pirate search: ')
    piratesearcher.search(search, _get_categories()[cat])
    magnet = piratesearcher.get_magnet(int(input('\n> ')))
    downloader.download(magnet)

def continue_download():
    file = open('downloads.json', 'r')
    downloads = json.loads(file.read())
    file.close()
    d = []
    for download in downloads:
        name = download["name"]
        total_downloaded = download['total_downloaded']
        total_size = download['size']
        complete = total_downloaded / total_size * 100
        if complete == 100: continue
        d.append(f'{name} | ({complete:.2f}%) completo')
    choice = _table(d)

def run():
    print(name)
    try:
        while True:
            start = _table(('Buscar', 'Continuar Download', 'Baixar por Link'))
            if start == 1:
                search()
            elif start == 2:
                continue_download()
            elif start == 3:
                pass
    except:
        quit()



        
        

if __name__ == '__main__':
    run()
