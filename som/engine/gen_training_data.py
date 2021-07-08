import glob
import sys
from text_analize import JapanesePronouncation
import time

# python gen_training_data.py wikiextractor/text/ training.txt


if __name__ == '__main__':
    args = sys.argv
    text_dir = args[1]
    out_file = args[2]

    start = time.time()

    files = glob.glob("{}/**/wiki_*".format(text_dir), recursive=True)

    jp = JapanesePronouncation()

    with open(out_file, "w") as fw:
        cnt = 0
        for file in files:
            cnt += 1
            messages = open(file).readlines()
            cnt2 = 0
            for message in messages:
                cnt2 += 1
                print("  {} / {}: {} --- {} / {}       ".format(cnt, len(files), file, cnt2, len(messages)), end="\r")
                words = jp.wakati(message)
                fw.write(' '.join(words) + '\n')

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
