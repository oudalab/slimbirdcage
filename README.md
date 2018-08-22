# slimbirdcage
A slimer reimplementation of the https://github.com/openeventdata/birdcage code

# Dependencies

GNU Parallel
sqlite3 # (with Json support)
python3.6 # or greater
pip3 # apt install python3-pip


Be sure to add a `myservers` file in the same directory. This file should list `:` and the ipaddress of every other remote server. [More information here](https://www.gnu.org/software/parallel/man.html#EXAMPLE:-Using-remote-computers).

    ```echo ":" > myservers```

pip3 install --upgrade pip3
pip3 instal --user -r requirements.txt

# Additional

sudo apt install speedtest-cli iperf
sudo apt install jq

# Execution

slimbirdcage has example scripts to run the pipeline.
The `RUN_ALL.sh` file runs the pipeline overall database input using bash.

The first variable is `dbfiles`, this is a list of the location of all the petrarch encoded database files. In this example all the files are local to the filesystem.

Next, a bash function called `myrun` is created. The `myrun` function takes one parameter (the file to be processed).
the function creates an output file the in the `outfile/` directory. You should ensure that this file exists. This function then runs the main processing line.

```bash

nice -n19 \
    sqlite3 $item "select json_object('doc_id', doc_id, 'phrases', phrases, 'mongo_id', mongo_id, 'date', date) from petrarch_table" |\
    parallel --no-notice --jobs +0 --pipe "python3 birdcage.py --data '-' \
    >> $outfile"
```

The first line, `nice -n19` gives this script low priority in the list of running tasks. This is an io bound tasks so it is best to not also dominate the cores. Next, sqlite3 extracts the data from the petrarch tables in the database file. The file was passed in as a parameter. They query constructs a json object for each returned row. A list of json objects is passed, via pipes, to `gnu parallel`. Then parallel runs `birdcage.py` on the sets of json rows, eah crun of birdcage takes a chunck of data from each process. The result events are written to std out and then to the declared outfile.

This process is looped over for each file in the `dbfiles` list. 


# Acknowledgement 

slimbirdcage makes extensive use of [GNU Parallel](https://www.gnu.org/software/parallel/). Below is the .bib citation.

```latex
@book{ole2018gnu,
      author       = {Tange, Ole},
      title        = {GNU Parallel 2018},
      publisher    = {Ole Tange},
      month        = Mar,
      year         = 2018,
      ISBN         = {9781387509881},
      doi          = {10.5281/zenodo.1146014},
      url          = {https://doi.org/10.5281/zenodo.1146014}
}
```
