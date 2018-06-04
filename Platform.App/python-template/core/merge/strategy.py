import log

class MergeStrategy:

    def __init__(self, session):
        self.session = session

    def run(self):
        """ Starts merge process

        Steps:
            1) Get all branch links from apicore
            2) For each entity query all data from branch to merge
            3) For each data row do:
                if data exist in master then just update
                else create a new data in branch master
            4) Mark this branch as merged in apicore
         """


        log.info('create fork')