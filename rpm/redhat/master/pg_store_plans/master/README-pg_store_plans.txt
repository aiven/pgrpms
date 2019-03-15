#  pg_store_plans

The `pg_store_plans` module provides a means for tracking execution plan
statistics of all SQL statements executed by a server.

The module must be loaded by adding `pg_store_plans` to
[shared_preload_libraries](http://www.postgresql.org/docs/current/static/runtime-
config-client.html#GUC-SHARED-PRELOAD-LIBRARIES) in `postgresql.conf`, because
it requires additional shared memory. This means that a server restart is
required to add or remove the module.

## 1\. The `pg_store_plans` View

The statistics gathered by the module are available via a system view named
`pg_store_plans`. This view contains one row for each distinct set of database
ID, user ID and query ID. The columns of the view are described in Table 1.

**Table 1. `pg_store_plans` Columns**

Name| Type| References | Description  
---|---|---|---  
`userid` | `oid` | [
`pg_authid``](http://www.postgresql.org/docs/current/static/catalog-pg-
authid.html).oid` | OID of user who executed the statement  
`dbid` | `oid` | [
`pg_database`](http://www.postgresql.org/docs/current/static/catalog-pg-
database.html)`.oid` | OID of database in which the statement was executed  
`queryid` | `bigint` |   | Internal hash code, computed from the statement's
query string.  
`planid` | `bigint` |   | Internal hash code, computed from the statement's
plan representation.  
`queryid_stat_statements` | `bigint` |   | A copy of pg_stat_statements' query
hash code. This is available only when pg_stat_statements is installed.  
`plan` | `text` |   | Text of a representative plan. The format is specified
by the configuration parameter `pg_store_plans.plan_format.`  
`calls` | `bigint` |   | Number of times executed  
`total_time` | `double precision` |   | Total time spent in the statement
using the plan, in milliseconds  
`rows` | `bigint` |   | Total number of rows retrieved or affected by the
statement using the plan  
`shared_blks_hit` | `bigint` |   | Total number of shared block cache hits by
the statement using the plan  
`shared_blks_read` | `bigint` |   | Total number of shared blocks read by the
statement using the plan  
`shared_blks_dirtied` | `bigint` |   | Total number of shared blocks dirtied
by the statement using the plan  
`shared_blks_written` | `bigint` |   | Total number of shared blocks written
by the statement using the plan  
`local_blks_hit` | `bigint` |   | Total number of local block cache hits by
the statement using the plan  
`local_blks_read` | `bigint` |   | Total number of local blocks read by the
statement using the plan  
`local_blks_dirtied` | `bigint`|   | Total number of local blocks dirtied by
the statement using the plan  
`local_blks_written` | `bigint` |   | Total number of local blocks written by
the statement using the plan  
`temp_blks_read` | `bigint` |   | Total number of temp blocks read by the
statement using the plan  
`temp_blks_written` | `bigint` |   | Total number of temp blocks written by
the statement using the plan  
`blk_read_time` | `double precision` |   | Total time the statement using the
plan spent reading blocks, in milliseconds (if
[track_io_timing](http://www.postgresql.org/docs/current/static/runtime-
config-statistics.html#GUC-TRACK-IO-TIMING) is enabled, otherwise zero)  
`blk_write_time` | `double precision` |   | Total time the statement using the
plan spent writing blocks, in milliseconds (if
[track_io_timing](http://www.postgresql.org/docs/current/static/runtime-
config-statistics.html#GUC-TRACK-IO-TIMING) is enabled, otherwise zero)  
`first_call` | `timestamp with time zone` |   | Timestamp for the least
recently call of the query using this plan.  
`last_call` | `timestamp with time zone` |   | Timestamp for the most recently
call of the query using this plan.  
  
This view, and the functions `pg_store_plans_reset ` and `pg_store_plans` and
other auxiliary functions, are available only in databases where the
`pg_store_plans` is installed by `CREATE EXTENSION`. However, statistics are
tracked across all databases of the server whenever the `pg_store_plans`
module is loaded onto the server, regardless of presence of the view.

For security reasons, non-superusers are not allowed to see the plan
representation, queryid or planid for the queries executed by other users.

`queryid` is calculated to identify the source query similary to
`pg_stat_statements` but in a different algorithm. `plan` is calculated in a
similar way. Two plans are considered the same if they are seemingly
equivalent except for the values of literal constants or fluctuating values
such like costs or measured time.

For PostgreSQL 9.4 or later, you can find the corresponding query for a
`pg_store_plans` entry in `pg_stat_statements` by joining using
`queryid_stat_statements`. Otherwise it is identified by using `queryid` and
`pg_store_plans_hash_query`, like following.

    
    
    SELECT s.query, p.plan FROM pg_store_plans p JOIN pg_stat_statements s ON (pg_store_plans_hash_query(s.query)) = p.queryid;

However plan id is calculated ignoring fluctuating values, the values for most
recent execution are still displayed in `pg_store_plans.plan`.

In some cases, `pg_stat_statements` merges semantically equivalent queries
which are considered different by `pg_stat_statements`. In the cases
correspondent in `pg_stat_statements` might not be found, but there is a small
chance that this happenes. In contrast, there also is a small chance that some
queries might be regarded as equivalent and merged into one entry in
`pg_store_plans` but differentiated in `pg_stat_statements` mainly for utility
statements.

`pg_store_plans` and `pg_stat_statements` maintain thier entries individually
so there is certain unavoidable chance especially for entries with low
execution frequency that no correspondent is found.

`queryid_stat_statements` has the same restriction to `pg_stat_statements` in
terms of stability. Although `queryid` and `planid` in `pg_store_plans`
doesn't have such a restriction, assuming long-term stability is also
discouraged.

##  2\. Functions

`pg_store_plans_reset() returns void`

    

`pg_store_plans_reset` discards all statistics gathered so far by
`pg_store_plans`. By default, only superusers can execute this function.

`pg_store_plans(showtext boolean) returns setof record`

    

The `pg_store_plans` view is defined in terms of a function also named
`pg_store_plans`.

`pg_store_hash_query(query text) returns oid`

    

This function calculates hash value of a query text. The same algorithm is
used to calculate `queryid` in `pg_store_plans` so this function is usable to
join with `pg_store_plans`.

`pg_store_plans_textplan(query text) returns text`

    

This function generates a ordinary text representation from raw representation
of `plan` in `pg_store_plans`, which is shown there when
`pg_store_plans.plan_formats` = 'raw'. Since the result plan text is generated
from json representation, it might be slightly different from what you will
get directly from 'EXPLAIN' commnand.

`pg_store_plans_jsonplan(query text) returns text`

    

This function infaltes a "short format json plan" or "raw format" into normal
json format. Short format json is internal format for `plan` in
`pg_store_plans`, which is shown there when `pg_store_plans.plan_formats` =
'raw'.

`pg_store_plans_xmlplan(query text) returns text`

    

This function generates a XML representation from raw representation of `plan`
in `pg_store_plans`, which is shown there when `pg_store_plans.plan_formats` =
'raw'.

`pg_store_plans_yamlplan(query text) returns text`

    

This function generates a YAML representation from raw representation of
`plan` in `pg_store_plans`, which is shown there when
`pg_store_plans.plan_formats` = 'raw'.

##  3\. Configuration Parameters

`pg_store_plans.max` (`integer`)

    

`pg_store_plans.max` is the maximum number of plans tracked by the module
(i.e., the maximum number of rows in the `pg_store_plans` view). If more
distinct plans than that are observed, information about the least-executed
plan is discarded. The default value is 1000. This parameter can only be set
at server start.

`pg_store_plans.track` (`enum`)

    

Similar to `pg_stat_statements`, `pg_store_plans.track` controls which
statements are counted by the module. Specify `top` to track top-level
statements (those issued directly by clients), `all` to also track nested
statements (such as statements invoked within functions), or `none` to disable
statement statistics collection. The default value is `top`. Only superusers
can change this setting.

`pg_store_plans.plan_format` (`enum`)

    

`pg_store_plans.plan_format` controls the format of `plans` in
`pg_store_plans`. `text` is the default value and to show in ordinary text
representation, `json`, `xml` and `yaml` to show in corresponding format.
`raw` to get internal representation which can be fed to
`pg_store_plans_*plan` functions.

`pg_store_plans.min_duration` (`integer`)

    

`pg_store_plans.min_duration` is the minumum statement execution time, in
milliseconds, that will cause the statement's plan to be logged. Setting this
to zero (the default) logs all plans. Only superuses can change this setting.

`pg_store_plans.log_analyze` (`boolean`)

    

`pg_store_plans.log_analyze` causes `EXPLAIN ANALYZE` output, rather than just
`EXPLAIN` output, to be included in `plan`. This parameter is off by default.

`pg_store_plans.log_buffers` (`boolean`)

    

`pg_store_plans.log_buffers` causes `EXPLAIN (ANALYZE, BUFFERS)` output,
rather than just `EXPLAIN` output, to be included in `plan`. This parameter is
off by default.

`pg_store_plans.log_timing` (`boolean`)

    

Setting `pg_store_plans.log_timing` to false disables to record actual
timings. The overhead of repeatedly reading the system clock can slow down the
query significantly on some systems, so it may be useful to set this parameter
to FALSE when only actual row counts, and not exact execution times for each
execution nodes, are needed. Run time of the entire statement is always
measured when `pg_store_plans.log_analyze` is TRUE. It defaults to TRUE.

`pg_store_plans.log_triggers` (`boolean`)

    

`pg_store_plans.log_triggers` causes trigger execution statistics to be
included in recoreded plans. This parameter has no effect unless
`pg_store_plans.log_analyze` is turned on.

`pg_store_plans.verbose` (`boolean`)

    

`pg_store_plans.verbose` causes `EXPLAIN VERBOSE` output, rather than just
`EXPLAIN` output, to be included in `plan`. This parameter is off by default.

`pg_store_plans.save` (`boolean`)

    

`pg_store_plans.save` specifies whether to save plan statistics across server
shutdowns. If it is `off` then statistics are not saved at shutdown nor
reloaded at server start. The default value is `on`. This parameter can only
be set in the `postgresql.conf` file or on the server command line.

The module requires additional shared memory proportional to
`pg_store_plans.max`. Note that this memory is consumed whenever the module is
loaded, even if `pg_store_plans.track` is set to `none`.

These parameters must be set in `postgresql.conf`. Typical usage might be:

    
    
    # postgresql.conf
    shared_preload_libraries = 'pg_store_plans, pg_stat_statements'
    pg_store_plans.max = 10000
    pg_store_plans.track = all

##  4\. Sample Output

    
    
    (postgresql.conf has following settings)
    shared_preload_libraries = 'pg_store_plans,pg_stat_statements'
    pg_store_plans.log_analyze = true
    pg_store_plans.log_timing = false
    
    bench=# SELECT pg_store_plans_reset();
    
    $ pgbench -i bench
    $ pgbench -c10 -t3000 bench
    
    bench=# \x
    bench=#  SELECT s.query, p.plan,
            p.calls as "plan calls", s.calls as "stmt calls",
            p.total_time / p.calls as "time/call", p.first_call, p.last_call
            FROM pg_stat_statements s
            JOIN pg_store_plans p ON
            (p.queryid = pg_store_plans_hash_query(s.query) and p.calls < s.calls)
            ORDER BY query ASC, "time/call" DESC;
    -[ RECORD 1 ]----------------------------------------------------------------------------------------------------------------------------
    query      | UPDATE pgbench_branches SET bbalance = bbalance + ? WHERE bid = ?;
    plan       | Update on pgbench_branches  (cost=0.00..8.01 rows=1 width=370) (actual rows=0 loops=1)
               |   ->  Seq Scan on pgbench_branches  (cost=0.00..8.01 rows=1 width=370) (actual rows=1 loops=1)
               |         Filter: (bid = 1)
    plan calls | 15583
    stmt calls | 30000
    time/call  | 40.096513957518
    first_call | 2014-04-25 14:29:17.163924+09
    last_call  | 2014-04-25 14:31:29.421635+09
    -[ RECORD 2 ]----------------------------------------------------------------------------------------------------------------------------
    query      | UPDATE pgbench_branches SET bbalance = bbalance + ? WHERE bid = ?;
    plan       | Update on pgbench_branches  (cost=0.12..8.14 rows=1 width=370) (actual rows=0 loops=1)
               |   ->  Index Scan using pgbench_branches_pkey on pgbench_branches  (cost=0.12..8.14 rows=1 width=370) (actual rows=1 loops=1)
               |         Index Cond: (bid = 1)
    plan calls | 14417
    stmt calls | 30000
    time/call  | 39.1920771311645
    first_call | 2014-04-25 14:31:29.288913+09
    last_call  | 2014-04-25 14:33:31.287061+09
    -[ RECORD 3 ]----------------------------------------------------------------------------------------------------------------------------
    query      | UPDATE pgbench_tellers SET tbalance = tbalance + ? WHERE tid = ?;
    plan       | Update on pgbench_tellers  (cost=0.14..8.16 rows=1 width=358) (actual rows=0 loops=1)
               |   ->  Index Scan using pgbench_tellers_pkey on pgbench_tellers  (cost=0.14..8.16 rows=1 width=358) (actual rows=1 loops=1)
               |         Index Cond: (tid = 7)
    plan calls | 4
    stmt calls | 30000
    time/call  | 87.0435
    first_call | 2014-04-25 14:30:37.850293+09
    last_call  | 2014-04-25 14:32:38.083977+09
    -[ RECORD 4 ]----------------------------------------------------------------------------------------------------------------------------
    query      | UPDATE pgbench_tellers SET tbalance = tbalance + ? WHERE tid = ?;
    plan       | Update on pgbench_tellers  (cost=4.14..8.16 rows=1 width=358) (actual rows=0 loops=1)
               |   ->  Bitmap Heap Scan on pgbench_tellers  (cost=4.14..8.16 rows=1 width=358) (actual rows=1 loops=1)
               |         Recheck Cond: (tid = 10)
               |         ->  Bitmap Index Scan using pgbench_tellers_pkey  (cost=0.00..4.14 rows=1 width=0) (actual rows=1 loops=1)
               |               Index Cond: (tid = 10)
    plan calls | 29996
    stmt calls | 30000
    time/call  | 33.6455953793834
    first_call | 2014-04-25 14:29:17.162871+09
    last_call  | 2014-04-25 14:33:31.28646+09

* * *

