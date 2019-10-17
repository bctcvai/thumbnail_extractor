#!/bin/bash

code=0
rm -fr test_out/*
python3 extractor/extractor.py --mode localization_thumbnail -i test/big_buck_bunny.mp4 -m test/big_buck_bunny.json -o test_out
vid_count=`ls test_out | wc -l`

if [ ${vid_count} -ne 15 ]; then
    echo "Failed video check"
    code=255
fi

python3 extractor/extractor.py --mode localization_thumbnail -i test/image.jpg -m test/image.json -o test_out
# Do checks

total_count=`ls test_out | wc -l`
img_count=$((${total_count} - ${vid_count}))
if [ ${img_count} -ne 4 ]; then
    echo "Failed image check"
    code=255
fi

exit ${code}
