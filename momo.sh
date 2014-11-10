sudo apt-get install g++ git subversion automake libtool zlib1g-dev libboost-all-dev libbz2-dev liblzma-dev python-dev libtcmalloc-minimal4
git clone https://github.com/moses-smt/mosesdecoder.git
cd mosesdecoder/
./bjam -j8
wget http://www.statmt.org/moses/download/sample-models.tgz
tar xzf sample-models.tgz
cd sample-models
~/mosesdecoder/bin/moses -f phrase-model/moses.ini < phrase-model/in > out
cat out
