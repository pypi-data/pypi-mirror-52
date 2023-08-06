import os
from kck.lib.kck_database import KCKDatabase
from kck.lib.kck_updater import KCKUpdater
from kck.lib.yaml_updater import KCKYamlUpdater
from kck.test.test_case import BaseKCKTestCase

SCRIPT_DIRPATH = os.path.dirname(os.path.realpath(__file__))
KCK_SOURCES_DIRPATH = os.path.join(SCRIPT_DIRPATH, "..")


class MockData(object):
    updaters = None

    def __init__(self):
        self.updaters = {}

    def register_updater(self, name, cls):
        print("registering updater: {}".format(name))
        self.updaters[name] = cls

    def updater(self, name):
        return self.updaters[name]

    def no_updaters_defined(self):
        return not bool(self.updaters)


class TestKCKUpdater(BaseKCKTestCase):

    def test_register_updater_yamls(self):
        data_obj = MockData()
        assert(data_obj.no_updaters_defined())
        KCKYamlUpdater.register_updaters(data_obj)
        assert(not data_obj.no_updaters_defined())
        assert(data_obj.updater("simple_updater1").parameters[0]["name"] == "id")

    def test_register_updater_modules(self):
        data_obj = MockData()
        assert(data_obj.no_updaters_defined())
        KCKUpdater.register_updaters(data_obj)
        assert(not data_obj.no_updaters_defined())
        assert(data_obj.updater("simpleclassbasedupdater1").parameters[0]["name"] == "id")

    def test_update_module_updates(self):
        data_obj = MockData()
        assert(data_obj.no_updaters_defined())
        KCKUpdater.register_updaters(data_obj)

        self._delete_postgres_tables()
        KCKDatabase.query(
            "test",
            """
                create table testtbl2 (
                    id serial PRIMARY KEY,
                    testcol2 varchar(256)
                )
            """
        )

        u = data_obj.updater("simpleclassbasedupdater1")
        res_homer = u.update({"testcol2": "homer"})
        res_barney = u.update({"testcol2": "barney"})
        res = KCKDatabase.query("test", "select id, testcol2 from testtbl2").fetchall()
        row_count = 0
        for row in res:
            row_count += 1
            assert(row[1] in ["homer", "barney"])
            if row[1] == "homer":
                assert(res_homer.fetchone()[0] == row[0])
            if row[1] == "barney":
                assert (res_barney.fetchone()[0] == row[0])

        assert(row_count == 2)

    def test_update_yaml_updates(self):
        data_obj = MockData()
        KCKYamlUpdater.register_updaters(data_obj)

        self._delete_postgres_tables()
        KCKDatabase.query(
            "test",
            """
                create table testtbl1 (
                    id serial PRIMARY KEY,
                    testcol1 float
                )
            """
        )

        u = data_obj.updater("simple_updater1")
        u.update({"testcol1":"1.234"})
        res = KCKDatabase.query("test", "select testcol1 from testtbl1").fetchall()
        assert(res[0][0] == 1.234)

    def _delete_postgres_tables(self):
        KCKDatabase.query("test", "drop table if exists testtbl1")
        KCKDatabase.query("test", "drop table if exists testtbl2")
