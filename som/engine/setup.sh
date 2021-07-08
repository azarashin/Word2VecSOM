FLAG_WIKI_EXTRACT=/home/som/.wiki_extract
FLAG_UNI_DIC=/home/som/.uni_dic
FLAG_NEOLOGD_DIC=/home/som/.neologd_dic

pip install --no-cache-dir -r requirements.txt

if [ -f ${WIKI_DATA} ]; then 
    echo ${WIKI_URL} exists. 
else
    echo download from ${WIKI_URL} ... 
    curl ${WIKI_URL} -o ${WIKI_DATA}
fi

if [ -f ${FLAG_WIKI_EXTRACT} ]; then 
    echo wiki data is already extracted. 
else
    echo extract wiki data...
    git clone https://github.com/attardi/wikiextractor.git wikiextractor
    cd wikiextractor
    python setup.py install
    echo wait a moment...
    python -m wikiextractor.WikiExtractor  ${WIKI_DATA}
    echo "done" >  ${FLAG_WIKI_EXTRACT}
fi

if [ -f ${FLAG_UNI_DIC} ]; then 
    echo unidic is already downloaded. 
else
    echo download unidic...
    python -m unidic download
    echo "done" >  ${FLAG_UNI_DIC}
fi

if [ -f ${FLAG_NEOLOGD_DIC} ]; then 
    echo NEologd is already downloaded. 
else
    echo download unidic...
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git ${NEOLOGD_DATA}
    cd ${NEOLOGD_DATA}
    yes | ./bin/install-mecab-ipadic-neologd -n -a 
    echo "done" >  ${FLAG_NEOLOGD_DIC}
fi

cd /home/som

if [ -f ${TRAINING_SRC} ]; then 
    echo training source is already generated. 
else
    echo generate training source...
    python gen_training_data.py wikiextractor/text/ ${TRAINING_SRC}
fi

if [ -f ${VECTOR_DATA} ]; then 
    echo training is already done. 
else
    echo generate training source...
    python run_training.py ${TRAINING_SRC} ${VECTOR_DATA}
fi


