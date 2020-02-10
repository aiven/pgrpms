#!/usr/bin/env python3

import argparse
from configparser import ConfigParser
import psycopg2
import time

class ReconnectingPostgres(object):
    def __init__(self, name, dsn, slotname, verbose):
        self.name = name
        self.dsn = dsn
        self.slotname = slotname
        self.verbose = verbose

        self._conn = None
        self._slot_active = False
        self._slot_restart_lsn = None

    def get_conn(self):
        tries = 0
        while tries < 3:
            tries += 1
            if self._conn:
                # Connection exists, poll it
                try:
                    curs = self._conn.cursor()
                    curs.execute("SELECT 1")
                    curs.fetchall()
                except Exception as e:
                    print("%s: ping failed: %s. Closing." % (self.name, e))
                    try:
                        self._conn.close()
                    except:
                        pass
                    self._conn = None
                    # Retry immediately without sleep
                    continue
                # Connection OK, so return it
                return self._conn
            # Make a new connection
            try:
                self._conn = psycopg2.connect(self.dsn)
            except Exception as e:
                print("%s: connection failed: %s" % (self.name, e))
                time.sleep(5)
                continue
            if self.verbose:
                print("%s: connected" % self.name)
            self._conn.autocommit = True
            return self._conn

        print("%s: multiple attempts failed, giving up for now." % self.name)
        return None

    def update_slot(self, create_if_missing=True):
        # Reset state
        self._slot_active= False
        self._slot_restart_lsn = False

        conn = self.get_conn()
        if conn:
            curs = conn.cursor()
            curs.execute("SELECT active, restart_lsn FROM pg_replication_slots WHERE slot_name=%(name)s", {'name': self.slotname})
            if curs.rowcount == 0:
                if create_if_missing:
                    print("%s: creating replication slot" % self.name)
                    try:
                        curs.execute("SELECT pg_create_physical_replication_slot(%(name)s, 't')", {'name': self.slotname})
                    except Exception as e:
                        print("%s: failed to create slot: %s" % (self.name, e))
                        return
                else:
                    print("%s: slot not found" % self.name)
            else:
                self._slot_active, self._slot_restart_lsn = curs.fetchone()

    def has_active_slot(self):
        return self._slot_active

    def get_slot_lsn(self):
        return self._slot_restart_lsn

    def move_slot(self, new_lsn):
        if self.verbose:
            print("Moving slot on %s to %s" % (self.name, new_lsn))

        conn = self.get_conn()
        if not conn:
            return

        curs = conn.cursor()
        curs.execute("SELECT pg_slotmove(%(name)s, %(newpos)s)", {
            'name': self.slotname,
            'newpos': new_lsn,
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replication slot synchronizer")
    parser.add_argument('--config', default='pg_slotsync.ini', help='Name of configuration file')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    cfg = ConfigParser()
    cfg.read(args.config)

    slotname = cfg.get('global', 'slotname')

    # Set up a list of all servers
    servers = [ReconnectingPostgres(k, v, slotname, args.verbose) for k,v in cfg.items('servers')]
    if args.verbose:
        print("Loaded %s servers" % len(servers))

    while True:
        list(map(lambda x: x.update_slot(), servers))
        active = [s for s in servers if s.has_active_slot()]
        if len(active) == 0:
            print("No active slot found, nothing to do")
        elif len(active) > 1:
            print("More than one active slot found! Should never happen!")
            sys.exit(1)
        else:
            active = active[0]
            for s in servers:
                if s == active:
                    continue
                if s.get_slot_lsn() != active.get_slot_lsn():
                    s.move_slot(active.get_slot_lsn())

        time.sleep(cfg.getint('global', 'interval', fallback=60))
