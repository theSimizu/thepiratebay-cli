import libtorrent as lt
import time
import json
import os

downloads_data = './downloads.json'
torrents_path = os.path.expanduser('~/Downloads/torrents')

class TorrentDownloader:
    def __init__(self) -> None:
        self._update_download_info()
        self.ses = lt.session()
        self.ses.listen_on(56969, 56969)

        self.params = {
            'save_path': torrents_path,
            'storage_mode': lt.storage_mode_t(2)
        }

    def _human_readable_size(self, size):
        prefixes = ('B', 'kB', 'MB', 'GB', 'TB')
        count = 0
        while size > 1024:
            size /= 1024
            count+=1
        return f'{size:.2f} {prefixes[count]}'

    def _new_download_info(self, name, link, downloaded, size):
        with open(downloads_data, 'r+') as file:
            downloads_list = json.loads(file.read())

            for download in downloads_list: 
                if download['magnet_link'] == link: return

            json_data = {"name": name, "magnet_link": link, 'total_downloaded': downloaded, 'size': size}
            downloads_list.append(json_data)
            file.seek(0)
            json.dump(downloads_list, file)
            file.truncate()

    def _edit_download_info(self, link, info, value):
        with open(downloads_data, 'r+') as file:
            downloads_list = json.loads(file.read())
            index = tuple(index for index, x  in enumerate(downloads_list) if x['magnet_link'] == link)[0]
            downloads_list[index][info] = value
            file.seek(0)
            json.dump(downloads_list, file)
            file.truncate()

    def _downloading_status(self, s):
        state_str = ['queued', 'checking', 'downloading metadata', \
                         'downloading', 'finished', 'seeding', 'allocating']
        line_1 = f'\r{self._human_readable_size(s.total_done)} of {self._human_readable_size(s.total_wanted)} ({(s.progress*100):.2f}%)        '
        line_2 = (f'Downloading from {s.num_peers} peers - ('
                  f'{self._human_readable_size(s.download_rate)}/s▾ '
                  f'{self._human_readable_size(s.upload_rate)}/s▴) '
                  f'{state_str[s.state]}         ')
        print(line_1)
        print(line_2, end='')
        print('\033[1A', end='\x1b[2K')

    def _wait_torrent(self, handle, magnet_link):
        print('Downloading Metadata...')
        wait_time = 0
        while (not handle.has_metadata()): 
            print(f'\r{"."*wait_time}', end='')
            wait_time+=1
            if wait_time > 60: raise Exception('Timeout')
            time.sleep(1) 
        print ('Got Metadata, Starting Torrent Download...')
        print("Starting", handle.name())
        self._new_download_info(handle.name(), magnet_link, handle.status().total_done,\
                                handle.status().total_wanted)
        os.system('clear')

    def _get_dir_size(self, path):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self._get_dir_size(entry.path)
        return total

    def _get_item_total_size(self, dir_name):
        full_path = os.path.join(torrents_path, dir_name)
        if os.path.isfile(full_path):
            total = os.path.getsize(full_path)
        elif os.path.isdir(full_path):
            total = self._get_dir_size(full_path)
        return total

    def _update_download_info(self):
        downloaded_torrents = os.listdir(torrents_path)
        with open(downloads_data, 'r+') as file:
            downloads_list = json.loads(file.read())
            for dir_name in downloaded_torrents:
                total = self._get_item_total_size(dir_name)
                for index, item in enumerate(downloads_list):
                    if item['name'] not in downloaded_torrents: downloads_list[index]['total_downloaded'] = 0
                    if item['name'] == dir_name: downloads_list[index]['total_downloaded'] = total
                    
            file.seek(0)
            json.dump(downloads_list, file)
            file.truncate()
            
    def download(self, magnet_link):
        handle = lt.add_magnet_uri(self.ses, magnet_link, self.params)

        self._wait_torrent(handle, magnet_link)        
        print(f'Downloading {handle.name()}')
        while handle.status().state != lt.torrent_status.seeding:
            s = handle.status()
            self._edit_download_info(magnet_link, "total_downloaded", s.total_done)
            self._downloading_status(s)
            time.sleep(1.5)
        os.system('clear')
        
        self._edit_download_info(magnet_link, "total_downloaded", handle.status().total_done)
        print('\r', handle.name(), "COMPLETE")
        quit()

if __name__ == '__main__':
    tl = TorrentDownloader()
    tl._update_download_info()
