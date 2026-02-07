# Bash completion for sync_pgdg_rpms.sh

_sync_pgdg_rpms() {
	local cur prev opts os_choice sync_mode
	local i

	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD - 1]}"

	opts="--os --arch --ver --sync --dry-run --debug --help"

	# Extract --os value if provided
	for i in "${!COMP_WORDS[@]}"; do
		if [[ "${COMP_WORDS[i]}" == "--os" && -n "${COMP_WORDS[i + 1]}" ]]; then
			os_choice="${COMP_WORDS[i + 1]}"
		fi
		if [[ "${COMP_WORDS[i]}" == "--sync" ]]; then
			sync_mode=1
		fi
	done

	case "$prev" in
	--os)
		COMPREPLY=($(compgen -W "redhat fedora sles" -- "$cur"))
		return 0
		;;
	--arch)
		# Provide architecture options based on OS if known
		if [[ "$os_choice" == "redhat" ]]; then
			COMPREPLY=($(compgen -W "aarch64 ppc64le x86_64" -- "$cur"))
		elif [[ "$os_choice" == "fedora" ]]; then
			COMPREPLY=($(compgen -W "x86_64" -- "$cur"))
		elif [[ "$os_choice" == "sles" ]]; then
			COMPREPLY=($(compgen -W "x86_64" -- "$cur"))
		else
			# If OS not specified yet, show all possible architectures
			COMPREPLY=($(compgen -W "aarch64 ppc64le x86_64" -- "$cur"))
		fi
		return 0
		;;
	--ver)
		if [[ "$os_choice" == "redhat" ]]; then
			COMPREPLY=($(compgen -W "10.1 10.0 9.7 9.6 8.10" -- "$cur"))
		elif [[ "$os_choice" == "fedora" ]]; then
			COMPREPLY=($(compgen -W "43 42" -- "$cur"))
		elif [[ "$os_choice" == "sles" ]]; then
			COMPREPLY=($(compgen -W "15.6 15.7 16.0" -- "$cur"))
		else
			# If OS not specified, show common versions
			COMPREPLY=($(compgen -W "10.1 10.0 9.7 9.6 8.10 43 42 15.6 15.7 16.0" -- "$cur"))
		fi
		return 0
		;;
	--sync)
		# Offer sync options: common, extras, testing, non-free, or PG versions
		COMPREPLY=($(compgen -W "common extras testing non-free 18 17 16 15 14" -- "$cur"))
		return 0
		;;
	*)
		# If we're in --sync mode (following --sync values), continue offering sync options
		if [[ -n "$sync_mode" && "$cur" != --* ]]; then
			COMPREPLY=($(compgen -W "common extras testing non-free 18 17 16 15 14" -- "$cur"))
			return 0
		fi
		;;
	esac

	# Default: offer main options
	if [[ "$cur" == --* ]]; then
		COMPREPLY=($(compgen -W "$opts" -- "$cur"))
	fi
}

# Register the function for your script name
complete -F _sync_pgdg_rpms sync_pgdg_rpms.sh
