cd ./Backend &&
(python3 database.py &
cd ../ML &&
(python3 newcolbase2.py & python3 ML_algorythm_new.py & python3 graphnew.py & python3 collaborative_baseline_new.py;
cd ../Backend &&
(python3 ensembler_update.py)));