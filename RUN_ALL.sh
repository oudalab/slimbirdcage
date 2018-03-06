#! /usr/bin/bash

dbfiles=(
/vol_c/data/processed_data/DISK1_CORENLP_RUN1.db_petrarch_done.db
/vol_c/data/processed_data/DISK1_CORENLP_RUN2.db_petrarch_done.db
/vol_c/data/processed_data/DISK2_CORENLP_V1_RUN1.db_petrarch_done.db
/vol_c/data/processed_data/DISK2_CORENLP_V2_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_CORENLP_V3_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_CORENLP_V4_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_KINGSTON_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_KINGSTON_RUN2.db_petrarch.db
/vol_c/data/processed_data/DISK2_PORTLAND_RUN3.db_petrarch.db
/vol_c/data/processed_data/DISK2_PORTLAND_VM_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_PORTLAND_VM_RUN2.db_petrarch.db
/vol_c/data/processed_data/DISK2_VM5_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_VM6_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_VM7_RUN1.db_petrarch.db
/vol_c/data/processed_data/DISK2_VM8_RUN1.db_petrarch.db
/vol_c/data/processed_data/gpel12_run1.db_petrarch.db
/vol_c/data/processed_data/gpel12_run2.db_petrarch.db
/vol_c/data/processed_data/gpel13_run1.db_petrarch.db
/vol_c/data/processed_data/gpel13_run2.db_petrarch.db
/vol_c/data/processed_data/gpel8_run1.db_petrarch.db
/vol_c/data/processed_data/gpel8_run2.db_petrarch.db
/vol_c/data/processed_data/gpel8_run3.db_petrarch.db
/vol_c/data/processed_data/gpel9_run2.db_petrarch.db
/vol_c/data/processed_data/KINGSTON_DISK2_CORENLP_FINAL1.db_petrarch.db
/vol_c/data/processed_data/KINGSTON_DISK2_CORENLP_FINAL_2.db_petrarch.db
/vol_c/data/processed_data/KINGSTON_DISK2_CORENLP_FINAL.db_petrarch.db
)


myrun () {
	local item=$1
	local fname=`basename $item`
	local outfile="outfiles/"$fname".json"
	#echo $fname
	#echo $outfile
	#ls -l $item
	nice -n19 sqlite3 $item "select json_object('doc_id', doc_id, 'phrases', phrases, 'mongo_id', mongo_id, 'date', date) from petrarch_table" | parallel --no-notice --jobs +0 --pipe "python3 birdcage.py --data '-' >> $outfile"
}

for item in ${dbfiles[@]};
do
	myrun $item &
done

# nice -n10 sqlite3 ~solaimani/data/DISK1_CORENLP_RUN1.db_petrarch_done.db "select json_object('doc_id', doc_id, 'phrases', phrases, 'mongo_id', mongo_id, 'date', date) from petrarch_table limit 5" | parallel --no-notice --sshloginfile myservers --workdir ...  --pipe python3 birdcage.py --data '-'
