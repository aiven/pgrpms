for i in `ls -d *|grep -v renew`
do
rm -fr $i
es-noncommon.sh $i F
done
rm sslutils/F\* 

es-nonfree-noncommon.sh timescaledb-tsl E
es-nonfree-noncommon.sh oracle_fdw E
es-nonfree-noncommon.sh pg_strom E
es-nonfree-noncommon.sh db2_fdw E
