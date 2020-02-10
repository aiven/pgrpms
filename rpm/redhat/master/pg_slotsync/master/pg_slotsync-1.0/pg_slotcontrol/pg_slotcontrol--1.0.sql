-- complain if script is sourced in psql, rather than via CREATE EXTENSION
\echo Use "CREATE EXTENSION pg_slotcontrol" to load this file. \quit

CREATE FUNCTION pg_slotmove(text, pg_lsn)
       RETURNS boolean
       AS 'MODULE_PATHNAME', 'pg_slotmove'
       LANGUAGE C VOLATILE STRICT;

REVOKE ALL ON FUNCTION pg_slotmove(text, pg_lsn) FROM PUBLIC;
