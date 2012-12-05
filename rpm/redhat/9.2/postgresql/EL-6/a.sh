usage()
{
        echo "Usage: pg_createnewcluster PG_MAJOR_VERSION CLUSTER_NAME"
        exit 1
}

[ "$#" -lt 2 ] && usage

# parse commandline
while [ $# -gt 0 ]
do
        arg="$1"
        case "#arg" in
                -h|--help) usage ;;
                -*) usage ;;
                *) break ;;
        esac
        shift
done

