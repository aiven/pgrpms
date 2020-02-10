/*
 * pg_slotcontrol.c
 *
 * Simple wrapper functions to control the position of
 * a physical replication slot from SQL.
 */
#include "postgres.h"

#include "fmgr.h"
#include "access/xlog.h"
#include "utils/builtins.h"
#include "utils/pg_lsn.h"
#include "replication/slot.h"

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(pg_slotmove);

Datum
pg_slotmove(PG_FUNCTION_ARGS)
{
	text	   *slotname = PG_GETARG_TEXT_PP(0);
	XLogRecPtr	moveto = PG_GETARG_LSN(1);
	char	   *slotnamestr;
	bool		changed = false;
	bool 		backwards = false;

	slotnamestr = text_to_cstring(slotname);

	if (XLogRecPtrIsInvalid(moveto))
		ereport(ERROR,
				(errmsg("Invalid target xlog position")));

	/* Temporarily acquire the slot so we "own" it */
	ReplicationSlotAcquire(slotnamestr);

	if (MyReplicationSlot->data.database != InvalidOid)
	{
		ReplicationSlotRelease();
		ereport(ERROR,
				(errmsg("Only physical slots can be moved.")));
	}

	if (moveto > GetXLogWriteRecPtr())
		/* Can't move past current position, so truncate there */
		moveto = GetXLogWriteRecPtr();

	/* Now adjust it */
	SpinLockAcquire(&MyReplicationSlot->mutex);
	if (MyReplicationSlot->data.restart_lsn != moveto)
	{
		/* Never move backwards, because bad things can happen */
		if (MyReplicationSlot->data.restart_lsn > moveto)
			backwards = true;
		else
		{
			MyReplicationSlot->data.restart_lsn = moveto;
			changed = true;
		}
	}
	SpinLockRelease(&MyReplicationSlot->mutex);

	if (backwards)
		ereport(WARNING,
				(errmsg("Not moving replication slot backwards!")));


	if (changed)
	{
		ReplicationSlotMarkDirty();
		ReplicationSlotsComputeRequiredLSN();
		ReplicationSlotSave();
	}

	/* And release it again, so we're not holding it */
	ReplicationSlotRelease();

	PG_RETURN_BOOL(changed);
}
