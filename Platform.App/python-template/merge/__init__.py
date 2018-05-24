import log

class MergeBranch:
    def __init__(self, session):
        self.session = session
        pass
    def run(self, instance_id, solution_id, event):
        log.info("Running merge branch")
        log.info(instance_id)
        log.info(solution_id)
        log.info(event)