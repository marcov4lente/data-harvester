from web_adapter import WebAdapter
from db_adapter import DBAdapter

class TopApps(WebAdapter):

    data_src = 'https://play.google.com/store/apps/collection/topselling_free'
    status = 0
    data = None

    def __init__(self):
        fields = [
            'id INTEGER PRIMARY KEY',
            'name TEXT',
            'developer TEXT',
            'rank INTEGER',
            'url TEXT',
            'created TEXT DEFAULT current_timestamp',
            ]

        db = DBAdapter()
        db.create_table_if_not_exists('top_apps', fields)


    def harvest(self):
        if not self.load_data():
            print('Error loading data')
            return False

        apps = self.data.select('.square-cover .details')

        for app in apps:

            appLink = app.find('a', class_='title')
            appLinkHref = appLink.attrs['href']
            appLinkContent = appLink.contents[0].split('.')

            developerLink = app.find('a', class_='subtitle')
            # developerLinkHref = developerLink.attrs['href']
            developerLinkContent = developerLink.contents

            data = {
                'name':appLinkContent[1].strip(),
                'developer':developerLinkContent[0],
                'rank':appLinkContent[0].strip(),
                'url':appLinkHref,
            }

            db = DBAdapter()
            db.insert('top_apps', data)

        return True




