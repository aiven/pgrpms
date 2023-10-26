#!/bin/bash
VERSION="3.4.3"

rm -rf gdal-"${VERSION}"{,-fedora}
tar zxf v"${VERSION}".tar.gz

mv gdal-"${VERSION}"{,-fedora} && pushd gdal-"${VERSION}"-fedora/gdal/data

rm cubewerx_extra.wkt
rm esri_StatePlane_extra.wkt
rm ecw_cs.wkt

# Sanitize linebreaks and encoding
# /frmts/grib/degrib18/degrib/metaname.cpp
# and geoconcept.c are potentially dangerous to change

set +x
for f in `find . -type f` ; do
  if file $f | grep -q ISO-8859 ; then
    set -x
    iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
      mv -f ${f}.tmp $f
    set +x
  fi
  if file $f | grep -q CRLF ; then
    set -x
    sed -i -e 's|\r||g' $f
    set +x
  fi
done
set -x

# Do more cleanup:
for f in apps; do
pushd $f
  chmod 644 *.cpp
popd
done

popd

#TODO: Insert Provenance file

tar cvfJ gdal-"${VERSION}"-fedora.tar.xz gdal-"${VERSION}"-fedora
