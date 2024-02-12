for file in $(ls /data/Twitter\ dataset | grep geoTwitter20-.* )
do 
    ./src/map.py --input_path="/data/Twitter dataset/$file"&
done
