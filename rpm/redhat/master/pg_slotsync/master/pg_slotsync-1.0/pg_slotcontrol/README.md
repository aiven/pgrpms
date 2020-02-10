## pg_slotcontrol

`pg_slotcontrol` provides a simple extension for controlling the
position of a replication slot. It allows moving the position that the
replication slot reserves, to make sure it doesn't block WAL
unnecessarily. Note that actually using this on a logical replication
slot is likely to break the replication apply, but for a physical slot
it is safe as long as the WAL is archived elsewhere.

### Installation

```
$ make install
```

Activation:

```
postgres=# CREATE EXTENSION pg_slotcontrol;
CREATE EXTENSION
```

### Usage

```
postgres=# SELECT slot_name, restart_lsn FROM pg_replication_slots;
 slot_name | restart_lsn 
-----------+-------------
 testslot  | 1/86000000
(1 row)
                                       ^
postgres=# SELECT pg_slotmove('testslot', '1/86000100');
 pg_slotmove 
-------------
 t
(1 row)

postgres=# SELECT slot_name, restart_lsn FROM pg_replication_slots;
 slot_name | restart_lsn 
-----------+-------------
 testslot  | 1/86000100
(1 row)
```
