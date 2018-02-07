class PostgresMigration:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, migration_object):
        name = "teste"
        f"""
        CREATE TABLE public.{name}
        (
            nome character varying COLLATE pg_catalog."default",
            idade integer,
            sobrenome character varying COLLATE pg_catalog."default",
            id uuid NOT NULL,
            CONSTRAINT pessoa_pkey PRIMARY KEY (id)
        )
        """

        pass

    def add_column(self, migration_object):
        pass