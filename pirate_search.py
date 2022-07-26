from requests_html import HTMLSession

class ThePirateBayCrawler:

    def __init__(self) -> None:
        self.session = HTMLSession()

    
    
    # Print formated line
    def _line_format(self, index, name, uploaded, size, se, le):
        print(' =========================================================================================================================================================')
        print('|{}|{}|{}|{}|{}|{}|'.format(str(index+1).center(6), str(name).center(101), 
                                                str(uploaded).center(12), str(size).center(15), str(se).center(7), str(le).center(7)))

    # Print the whole table
    def _links_table(self, links):
        print('\n')
        print(' =========================================================================================================================================================')
        print('|{}|{}|{}|{}|{}|{}|'.format(str('N').center(6), str('Name').center(101), 
                                                str('Uploaded').center(12), str('Size').center(15), str('SE').center(7), str('LE').center(7)))
        for index, link in enumerate(links):
            name = link.find('.item-title', first=True).find('a', first=True).text
            uploaded = link.find('.item-uploaded', first=True).find('label', first=True).text
            size = link.find('.item-size', first=True).text
            se = link.find('.item-seed', first=True).text
            le = link.find('.item-leech', first=True).text
            self._line_format(index, name, uploaded, size, se, le)
        print(' =========================================================================================================================================================\n')

    # Save the queries's magnet links in a list and return it
    def _magnets(self, query):
        magnet_links = ['']
        for link in query:
            item = link.find('.item-icons', first=True)
            magnet = item.find('a', first=True).absolute_links
            magnet_links.append(magnet.pop())
        return magnet_links

    # Search 
    def search(self, name, category=0):
        r = self.session.get(f'https://thepiratebay.org/search.php?q={name}&cat={category}')
        while True:
            try:
                r.html.render(retries=2, timeout=10, sleep=3, keep_page=True, scrolldown=1)
                break
            except:
                pass
        queries = r.html.find('.list-entry')
        self._links_table(queries)
        self.magnet_links = self._magnets(queries)
    
    def get_magnet(self, choice):
        magnet = self.magnet_links[choice]
        self.magnet_links.clear()
        return magnet




if __name__ == '__main__':


    tpb = ThePirateBayCrawler()

    tpb.search('red dead redemption')

    tpb.get_magnet(int(input('\n> ')))


# query = input('Search: ')

# session = HTMLSession()
# r = session.get(f'https://thepiratebay.org/search.php?q={query}&cat=0')
# r.html.render(retries=2, timeout=10, sleep=3, keep_page=True, scrolldown=1)#sleep=1, keep_page=True, scrolldown=1)

# links = r.html.find('.list-entry')

# links_table(links)

# magnets = _magnets(links)

# get_magnet(magnets)
