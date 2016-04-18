import os
from Tribler.Core.CacheDB.db_versions import LATEST_DB_VERSION, LOWEST_SUPPORTED_DB_VERSION
from Tribler.Core.Upgrade.upgrade import TriblerUpgrader
from Tribler.Test.Core.Upgrade.upgrade_base import AbstractUpgrader
from Tribler.dispersy.util import call_on_reactor_thread, blocking_call_on_reactor_thread


class TestUpgrader(AbstractUpgrader):

    def setUp(self):
        super(TestUpgrader, self).setUp()
        self.copy_and_initialize_upgrade_database('tribler_v17.sdb')
        self.upgrader = TriblerUpgrader(self.session, self.sqlitedb)

    @blocking_call_on_reactor_thread
    def test_stash_database(self):
        self.upgrader.stash_database()
        old_dir = os.path.dirname(self.sqlitedb.sqlite_db_path)
        self.assertTrue(os.path.exists(u'%s_backup_%d' % (old_dir, LATEST_DB_VERSION)))
        self.assertIsNotNone(self.sqlitedb._connection)
        self.assertTrue(self.upgrader.is_done)

    @blocking_call_on_reactor_thread
    def test_should_upgrade(self):
        self.sqlitedb._version = LATEST_DB_VERSION + 1
        self.assertTrue(self.upgrader.check_should_upgrade()[0])
        self.assertFalse(self.upgrader.check_should_upgrade()[1])

        self.sqlitedb._version = LOWEST_SUPPORTED_DB_VERSION - 1
        self.assertTrue(self.upgrader.check_should_upgrade()[0])
        self.assertFalse(self.upgrader.check_should_upgrade()[1])

        self.sqlitedb._version = LATEST_DB_VERSION
        self.assertFalse(self.upgrader.check_should_upgrade()[0])
        self.assertFalse(self.upgrader.check_should_upgrade()[1])

        self.sqlitedb._version = LATEST_DB_VERSION - 1
        self.assertFalse(self.upgrader.check_should_upgrade()[0])
        self.assertTrue(self.upgrader.check_should_upgrade()[1])

    @blocking_call_on_reactor_thread
    def test_upgrade_with_upgrader_enabled(self):
        self.upgrader.run()
        self.assertTrue(self.upgrader.is_done)
        self.assertFalse(self.upgrader.failed)


class TestUpgraderDisabled(AbstractUpgrader):

    def setUp(self):
        super(TestUpgraderDisabled, self).setUp()
        self.copy_and_initialize_upgrade_database('tribler_v17.sdb')
        self.upgrader = TriblerUpgrader(self.session, self.sqlitedb)

    @blocking_call_on_reactor_thread
    def test_upgrade_with_upgrader_disabled(self):
        self.upgrader.run()
        self.assertTrue(self.upgrader.is_done)
        self.assertFalse(self.upgrader.failed)