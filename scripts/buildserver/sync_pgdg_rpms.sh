#!/usr/bin/bash

set -euo pipefail

sync_had_errors=0

# Defaults
OS=""
ARCH=""
VER=""
DRY_RUN=false
DEBUG=false
BASE_DIR_redhat="/srv/yum/yum"
BASE_DIR_fedora="/srv/yum/yum"
BASE_DIR_sles="/srv/zypp/zypp"
PG_ALL_VERSIONS=(18 17 16 15 14)		# All supported stable versions
PG_TEST_VERSIONS=(18 17 16 15 14)		# Versions available in testing repos
EXTRASREPOSENABLED=0
SYNCTESTINGREPOS=0
SYNCNONFREEREPOS=0
SYNC_ITEMS=()					# New: items to sync (common, extras, testing, non-free, or PG versions)
SYNC_PG_VERSIONS=()				# PG versions to sync based on --sync option

# Valid values
VALID_OS=("redhat" "fedora" "sles")
VALID_ARCH_redhat=("aarch64" "ppc64le" "x86_64")
VALID_ARCH_fedora=("x86_64")
VALID_ARCH_sles=("x86_64")
VALID_VER_redhat=("10.1" "10.0" "9.7" "9.6" "8.10")
VALID_VER_fedora=("43" "42")
VALID_VER_sles=("15.6" "15.7" "16.0")

# Help
usage() {
	cat <<EOF
Usage: $0 --os <os> --arch <arch> --ver <version> [options]

Required:
  --os           Operating system: redhat, fedora or sles
  --arch         Architecture: aarch64, ppc64le, x86_64
  --ver          OS version: redhat (10.1, 10.0, 9.7, 9.6, 8.10), fedora (43,42), sles (15.6, 15.7, 16.0)

Optional:
  --sync         Sync specific items: common, extras, testing, non-free, or PG version (e.g. 18)
                 Can specify multiple items (e.g. --sync common 18 17)
                 If not specified, syncs all available repos
  --dry-run      Simulate the sync without transferring files
  --debug        Show detailed debug output

Examples:
  $0 --os redhat --arch x86_64 --ver 9.7 --sync common
  $0 --os fedora --arch x86_64 --ver 43 --sync 18 17
  $0 --os redhat --arch x86_64 --ver 9.7 --sync common extras testing

EOF
	exit 1
}

# Contains helper
contains() {
	local val="$1"
	shift
	for item in "$@"; do [[ "$item" == "$val" ]] && return 0; done
	return 1
}

# Parse arguments
# Parse args
while [[ $# -gt 0 ]]; do
	case "$1" in
	--os)
		OS="$2"
		shift 2
		;;
	--arch)
		ARCH="$2"
		shift 2
		;;
	--ver)
		VER="$2"
		shift 2
		;;
	--sync)
		shift
		while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
			SYNC_ITEMS+=("$1")
			shift
		done
		;;
	--dry-run)
		DRY_RUN=true
		shift
		;;
	--debug)
		DEBUG=true
		shift
		;;
	*)
		echo "Unknown option: $1"
		usage
		;;
	esac
done

# Determine OS-specific prefix and extras repo availability
case "$OS" in
redhat)
	VALID_ARCH=("${VALID_ARCH_redhat[@]}")
	VALID_VER=("${VALID_VER_redhat[@]}")
	osname="rhel"
	osdistro="redhat"
	EXTRASREPOSENABLED=1
	SYNCTESTINGREPOS=1
	;;
fedora)
	VALID_ARCH=("${VALID_ARCH_fedora[@]}")
	VALID_VER=("${VALID_VER_fedora[@]}")
	osname="fedora"
	osdistro="fedora"
	EXTRASREPOSENABLED=0
	SYNCTESTINGREPOS=1
	;;
sles)
	VALID_ARCH=("${VALID_ARCH_sles[@]}")
	VALID_VER=("${VALID_VER_sles[@]}")
	osname="sles"
	osdistro="suse"
	EXTRASREPOSENABLED=0
	SYNCTESTINGREPOS=0
	;;
*)
	echo "Unsupported OS: $OS"
	usage
	;;
esac

# Validation
[[ -z "$OS" || -z "$ARCH" || -z "$VER" ]] && usage

if ! contains "$OS" "${VALID_OS[@]}"; then
	echo "Invalid OS: $OS"
	usage
fi

if ! contains "$ARCH" "${VALID_ARCH[@]}"; then
	echo "Invalid arch: $ARCH"
	usage
fi

if ! contains "$VER" "${VALID_VER[@]}"; then
	echo "Invalid version '$VER' for OS '$OS'"
	echo "Valid versions: ${VALID_VER[*]}"
	exit 1
fi

if [[ "$OS" == "redhat" && ! " ${VALID_VER[*]} " =~ " $VER " ]]; then
	echo "Invalid version: $VER for redhat"
	usage
elif [[ "$OS" == "fedora" && ! " ${VALID_VER[*]} " =~ " $VER " ]]; then
	echo "Invalid version: $VER for fedora"
	usage
fi

# Validate arch and ver
if ! contains "$ARCH" "${VALID_ARCH[@]}"; then
	echo "Invalid architecture '$ARCH' for OS '$OS'"
	echo "Valid: ${VALID_ARCH[*]}"
	exit 1
fi

if ! contains "$VER" "${VALID_VER[@]}"; then
	echo "Invalid version '$VER' for OS '$OS'"
	echo "Valid: ${VALID_VER[*]}"
	exit 1
fi

# Process SYNC_ITEMS to determine what to sync
SYNC_COMMON=0
SYNC_EXTRAS=0
SYNC_TESTING=0
SYNC_NONFREE=0

if [[ ${#SYNC_ITEMS[@]} -eq 0 ]]; then
	# If no --sync specified, sync everything available
	SYNC_COMMON=1
	SYNC_EXTRAS=$EXTRASREPOSENABLED
	SYNC_TESTING=$SYNCTESTINGREPOS
	SYNC_NONFREE=$SYNCNONFREEREPOS
	SYNC_PG_VERSIONS=("${PG_ALL_VERSIONS[@]}")
else
	# Parse SYNC_ITEMS
	for item in "${SYNC_ITEMS[@]}"; do
		case "$item" in
		common)
			SYNC_COMMON=1
			;;
		extras)
			SYNC_EXTRAS=1
			;;
		testing)
			SYNC_TESTING=1
			;;
		non-free)
			SYNC_NONFREE=1
			;;
		18|17|16|15|14|13|12|11|10)
			SYNC_PG_VERSIONS+=("$item")
			;;
		*)
			echo "Invalid sync item: $item"
			echo "Valid items: common, extras, testing, non-free, or PG version (18, 17, 16, 15, 14, etc.)"
			exit 1
			;;
		esac
	done
fi

# Debug output
if $DEBUG; then
	echo "[DEBUG] OS:   $OS"
	echo "[DEBUG] ARCH: $ARCH"
	echo "[DEBUG] VER:  $VER"
	echo "[DEBUG] osname: $osname"
	echo "[DEBUG] osdistro: $osdistro"
	echo "[DEBUG] EXTRASREPOSENABLED: $EXTRASREPOSENABLED"
	echo "[DEBUG] SYNCTESTINGREPOS: $SYNCTESTINGREPOS"
	echo "[DEBUG] SYNC_COMMON: $SYNC_COMMON"
	echo "[DEBUG] SYNC_EXTRAS: $SYNC_EXTRAS"
	echo "[DEBUG] SYNC_TESTING: $SYNC_TESTING"
	echo "[DEBUG] SYNC_NONFREE: $SYNC_NONFREE"
	echo "[DEBUG] SYNC_PG_VERSIONS: ${SYNC_PG_VERSIONS[*]}"
	echo "[DEBUG] Dry run:    $DRY_RUN"
fi

# Determine source host based on OS
if [[ "$OS" == "redhat" ]]; then
	SOURCE_HOST="pgrpms-el${VER}-${ARCH}.postgresql.org"
elif [[ "$OS" == "fedora" ]]; then
	SOURCE_HOST="pgrpms-fedora${VER}-${ARCH}.postgresql.org"
elif [[ "$OS" == "sles" ]]; then
	SOURCE_HOST="pgrpms-sles${VER}-${ARCH}.postgresql.org"
else
	echo "Unsupported OS: $OS"
	exit 1
fi

# Dry-run mode
if $DRY_RUN; then
	echo "[DRY-RUN] Would sync $OS $VER $ARCH"
	echo "[DRY-RUN] SYNC_COMMON: $SYNC_COMMON"
	echo "[DRY-RUN] SYNC_EXTRAS: $SYNC_EXTRAS"
	echo "[DRY-RUN] SYNC_TESTING: $SYNC_TESTING"
	echo "[DRY-RUN] SYNC_NONFREE: $SYNC_NONFREE"
	echo "[DRY-RUN] SYNC_PG_VERSIONS: ${SYNC_PG_VERSIONS[*]}"
	exit 0
fi

# Run the sync command. This is the main loop.
echo "Starting sync operation for $OS $VER $ARCH"

osdistro=$OS
osarch=$ARCH
distrover=$VER
tmp_var="BASE_DIR_${OS}"
BASE_DIR_OS="${!tmp_var}"
sleep 1

echo "Syncing : $osname-$distrover"

# Sync non-common repo (specific PG versions)
if [[ ${#SYNC_PG_VERSIONS[@]} -gt 0 ]]; then
	for pgrelease in "${SYNC_PG_VERSIONS[@]}"; do
		echo "Syncing : $osname-$distrover-PG$pgrelease"

		RPM_DIR=/var/lib/pgsql/rpm$pgrelease/ALLRPMS

		if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$RPM_DIR/ $BASE_DIR_OS/$pgrelease/$osdistro/$osname-$distrover-$osarch; then
			echo "[ERROR] Rsync failed for PG $pgrelease ($osname-$distrover-$osarch)" >&2
			sync_had_errors=1
		fi
	done
fi

# Sync common repo
if [[ "$SYNC_COMMON" -eq 1 ]]; then
	echo "Syncing : $osname-$distrover-common repo"
	COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMON_RPM_DIR/ $BASE_DIR_OS/common/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for common repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi
fi

# Sync extras repo
if [[ "$SYNC_EXTRAS" -eq 1 ]]; then
	echo "Syncing : $osname-$distrover-extras repo"
	EXTRAS_RPM_DIR=/var/lib/pgsql/pgdg.extras/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$EXTRAS_RPM_DIR/ $BASE_DIR_OS/extras/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for Extras repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi
fi

# Sync testing repos
if [[ "$SYNC_TESTING" -eq 1 ]]; then
	echo "Syncing : $osname-$distrover-common testing repo"
	COMMONTESTING_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMONTESTING_RPM_DIR/ $BASE_DIR_OS/testing/common/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for commontesting repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi

	# Sync testing repos for specific PG versions
	for pgtestrelease in "${PG_TEST_VERSIONS[@]}"; do
		echo "Syncing : $osname-$distrover-PG$pgtestrelease testing repo"
		testdir="rpm${pgtestrelease}testing"
		TESTING_RPM_DIR=/var/lib/pgsql/$testdir/ALLRPMS

		if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$TESTING_RPM_DIR/ $BASE_DIR_OS/testing/$pgtestrelease/$osdistro/$osname-$distrover-$osarch; then
			echo "[ERROR] Rsync failed for PG $pgtestrelease testing repo ($osname-$distrover-$osarch)" >&2
			sync_had_errors=1
		fi
	done
fi

# Sync non-free repos
if [[ "$SYNC_NONFREE" -eq 1 ]]; then
	echo "Syncing : $osname-$distrover-non-free repo"
	NONFREE_RPM_DIR=/var/lib/pgsql/nonfree/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$NONFREE_RPM_DIR/ $BASE_DIR_OS/nonfree/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for non-free repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi
fi

# Finally tell us if there is an error in at least one of the steps above:

if [[ "$sync_had_errors" -eq 1 ]]; then
	echo "[WARN] One or more sync operations failed."
	exit 1
else
	echo "All syncs completed successfully."
	exit 0
fi
