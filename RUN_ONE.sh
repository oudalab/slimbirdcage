#! /usr/bin/bash

dbfiles=(
/vol_c/data/processed_data/DISK1_CORENLP_RUN1.db_petrarch_done.db
)


myrun () {
	local item=$1
	local fname=`basename $item`
	local outfile="outfiles/"$fname".json"
	#echo $fname
	#echo $outfile
	#ls -l $item
	sqlite3 $item "select json_object('doc_id', doc_id, 'phrases', phrases, 'mongo_id', mongo_id, 'date', date) from petrarch_table" | parallel --no-notice --jobs +0 --pipe --block 256M "python3 birdcage.py --data '-' >> $outfile"
}

for item in ${dbfiles[@]};
do
	myrun $item &
done

# nice -n10 sqlite3 ~solaimani/data/DISK1_CORENLP_RUN1.db_petrarch_done.db "select json_object('doc_id', doc_id, 'phrases', phrases, 'mongo_id', mongo_id, 'date', date) from petrarch_table limit 5" | parallel --no-notice --sshloginfile myservers --workdir ...  --pipe python3 birdcage.py --data '-'
