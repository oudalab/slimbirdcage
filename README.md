# slimbirdcage
A slimer reimplementation of the openventdata/birdcage code

# Dependencies

GNU Parallel
sqlite3 # (with Json support)
python3.6 # or greater
pip3 # apt install python3-pip


Be sure to add a myservers file

    ```echo ":" > myservers```

pip3 install --upgrade pip3
pip3 instal --user -r requirements.txt

# Additional

sudo apt install speedtest-cli iperf
sudo apt install jq

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
