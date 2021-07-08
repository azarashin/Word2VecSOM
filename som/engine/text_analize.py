class WordInfo:
    
    def __init__(self, source):
        if source is None:
            self.pronounce = []
            self.original = ''
            self.pos = ''
            self.accent_type = []
            self.accent_connect_type_c = []
            self.accent_connect_type_p = []
            self.accent_connect_type_f = []
            self.accent_modify_type = []
            self.modified_accent_type = []
        elif len(source) < 9:
            self.pronounce = [source[0].split('\t')[0]]
            self.original  = source[0].split('\t')[0]
            self.pos = source[0].split('\t')[1]
            self.accent_type = []
            self.accent_connect_type_c = []
            self.accent_connect_type_p = []
            self.accent_connect_type_f = []
            self.accent_modify_type = []
            self.modified_accent_type = []
        else:
            self.pronounce = self.to_mora(source[9])
            self.original  = source[0].split('\t')[0]
            self.pos = source[0].split('\t')[1]
            self.accent_type = [int(d) for d in source[24:-3] if self.isint(d)] # int(source[24]) if source[24] != '' else 0
            self.accent_connect_type_c = [d for d in source[24:-3] if 'C' in d] # source[25]
            self.accent_connect_type_p = [d for d in source[24:-3] if 'P' in d] # source[25]
            self.accent_connect_type_f = [d for d in source[24:-3] if 'F' in d] # source[25]
            self.accent_modify_type = [int(d) for d in source[24:-3] if 'M' in d] # source[26]
            self.modified_accent_type = []

    def isint(self, s):  # 整数値を表しているかどうかを判定
        try:
            int(s, 10)  # 文字列を実際にint関数で変換してみる
        except ValueError:
            return False
        else:
            return True


    def modify(self, value):
        if value != 0:
            self.modified_accent_type.append(value)


    def to_mora(self, source):
        src = source[:]
        ret = []
        for i in range(len(src)):
            if self.is_small_char_y(src[i]):
                continue
            if i >= len(src)-1:
                ret.append(src[i])
            elif self.is_small_char_y(src[i+1]):
                ret.append('{}{}'.format(src[i], src[i+1]))
            else:
                ret.append(src[i])
        return ret

    def is_small_char_y(self, c):
        return c == 'ャ' or c == 'ュ' or c == 'ョ' or c == 'ァ' or c == 'ィ' or c == 'ゥ' or c == 'ェ' or c == 'ォ'

    def __str__(self):
        con = [self.accent_connect_type_c, self.accent_connect_type_p, self.accent_connect_type_f]
        return '{} [{}:{}]\t({}, {}, {}: {})'.format(self.pronounce, self.original, self.pos, self.accent_type, self.accent_modify_type, con, self.modified_accent_type)

class JapanesePronouncation:

    # dic: unidic, neologd
    def __init__(self, dic="neologd"):
        # pip install ipadic
        # pip install unidic
        # pip install mecab-python3

        # # https://github.com/polm/fugashi
        # pip install fugashi
        # # https://pypi.org/project/unidic/
        # python -m unidic download
        #
        # 出力フォーマット
        # http://taku910.github.io/mecab/format.html
        #
        # アクセントについて＆その他詳細
        # https://unidic.ninjal.ac.jp/UNIDIC_manual.pdf
        import fugashi
        import unidic
        # 辞書の場所を強制的に書き換える。
        # これをやらないとバイナリ化した時に実行で失敗する
        if dic == "unidic":
            unidic.DICDIR = '/usr/local/lib/python3.9/site-packages/unidic/dicdir'
            self._tagger = fugashi.Tagger('-d "{}"'.format(unidic.DICDIR))
        if dic == "neologd":
            dic = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd'
            self._tagger = fugashi.GenericTagger('-d "{}"'.format(dic))
            
    def tagging(self, message):
        res = self._tagger.parse(message)
        print(res)
        original = [WordInfo([d0 for d0 in d.split(',')]) for d in res.split('\n') if len(d.split(',')) >= 2]
        modified = [WordInfo([d0 for d0 in d.split(',')]) for d in res.split('\n') if len(d.split(',')) >= 2]
        self.inflection_form(modified)
        self.connect(modified)
        self.post(modified)
        return original, modified

    def wakati(self, message):
        res = self._tagger.parse(message)
        return [w.split('\t')[0] for w in res.split('\n')][:-1]

    def inflection_form(self, word_infos):
        for wi in word_infos:
            for mod in wi.accent_modify_type:
                if mod[1] == '1':
                    p = int(mod.split('@')[1])
                    wi.modify(len(wi.pronounce) - p)
                if mod[1] == '2':
                    p = int(mod.split('@')[1])
                    if len(wi.accent_type) == 0:
                        wi.modify(len(wi.pronounce) - p)
                    else:
                        for acc in wi.accent_type:
                            wi.modify(acc)
                if mod[1] == '4':
                    p = int(mod.split('@')[1])
                    for acc in wi.accent_type:
                        if acc == 0 or acc == 1:
                            wi.modify(wi.accent_type)
                        else:
                            wi.modify(wi.accent_type - p)

    def connect_noun(self, ctype, n1, n2, m1, m2, pwi, wi):
        # wi.accent_connect_type -> ctype
        if ctype != '' and ctype[0] == 'C':
            if ctype[1] == '1':
                # wi.modified_accent_type = n1 + m2
                wi.modify(m2)
                pwi.modify(0)
            if ctype[1] == '2':
                # wi.modified_accent_type = n1 + 1
                print('#')
                wi.modify(1)
                pwi.modify(0)
            if ctype[1] == '3':
                wi.modify(0)
                pwi.modify(n1)
            if ctype[1] == '4':
                wi.modify(0)
                pwi.modify(0)
            if ctype[1] == '5':
                wi.modify(0)
                pwi.modify(m1)

    def connect_joint_words(self, ctype, n1, n2, m1, m2, pwi, wi):
        if ctype != '' and ctype[0] == 'P':
            if ctype[1:] == '1':
                if m2 == 0 or m2 == n2:
                    pwi.modify(0)
                    wi.modify(0)
                else:
                    pwi.modify(0)
                    wi.modify(m2)
            if ctype[1:] == '2':
                if m2 == 0 or m2 == n2:
                    pwi.modify(0)
                    wi.modify(1)
                else:
                    pwi.modify(0)
                    wi.modify(m2)
            if ctype[1:] == '4':
                if m2 == 0 or m2 == n2:
                    pwi.modify(0)
                    wi.modify(1)
                else:
                    pwi.modify(m1)
                    wi.modify(0)
            if ctype[1:] == '6':
                if m2 == 0 or m2 == n2:
                    pwi.modify(0)
                    wi.modify(0)
                else:
                    pwi.modify(0)
                    wi.modify(0)
            if ctype[1:] == '13':
                pwi.modify(m1)
                wi.modify(0)
            if ctype[1:] == '14':
                if m2 == 0 or m2 == n2:
                    pwi.modify(m1)
                    wi.modify(0)
                else:
                    pwi.modify(0)
                    wi.modify(m2)

    def connect_particle(self, ctype, n1, n2, m1, m2, pwi, wi):
        if ctype == '':
            return
        ctype_pair = ctype.split('%')
        if len(ctype_pair) == 2:
            target_pos = ctype_pair[0]
            ctype = ctype_pair[1]
            if target_pos != pwi.pos:
                return
        if ctype[0] == 'F':
            param = 0
            fs = ctype.split('@')
            if len(fs) >= 2:
                params = [int(d) for d in fs[1].split(',')]
            if ctype[1] == '1':
                wi.modify(0)
                pwi.modify(m1)
            if ctype[1] == '2':
                if m1 == 0:
                    wi.modify(params[0])
                    pwi.modify(0)
                else:
                    wi.modify(0)
                    pwi.modify(m1)
            if ctype[1] == '3':
                if m1 == 0:
                    wi.modify(0)
                    pwi.modify(m1)
                else:
                    wi.modify(params[0])
                    pwi.modify(0)
            if ctype[1] == '4':
                wi.modify(params[0])
                pwi.modify(0)
            if ctype[1] == '5':
                wi.modify(0)
                pwi.modify(0)
            if ctype[1] == '6':
                if m1 == 0:
                    wi.modify(params[0])
                    pwi.modify(0)
                else:
                    wi.modify(params[1])
                    pwi.modify(0)

    def connect(self, word_infos):
        for i in range(len(word_infos)):
            if i > 0:
                pwi = word_infos[i - 1]
            else:
                pwi = WordInfo(None) # dummy
            for pacc in word_infos[i - 1].accent_type:
                for acc in word_infos[i].accent_type:
                    wi = word_infos[i]
                    n1 = 0
                    n2 = len(word_infos[i].pronounce)
                    m1 = 0
                    m2 = 0
                    if i > 0:
                        n1 = len(word_infos[i - 1].pronounce)
                        m1 = int(pacc)
                        m2 = int(acc)

                    if wi.pos == '名詞' or wi.pos == '接尾辞':
                        for con in wi.accent_connect_type_c:
                            self.connect_noun(con, n1, n2, m1, m2, pwi, wi)
                    if wi.pos == '接頭辞':
                        for con in wi.accent_connect_type_p:
                            self.connect_joint_words(con, n1, n2, m1, m2, pwi, wi)
                    if wi.pos == '助詞' or wi.pos == '助動詞':
                        for con in wi.accent_connect_type_f:
                            self.connect_particle(con, n1, n2, m1, m2, pwi, wi)

    def post(self, word_infos):
        for w in word_infos:
            for acc in w.accent_type:
                if not acc in w.modified_accent_type:
                    w.modified_accent_type.append(acc)
                
    
    def to_accents(self, message):
        words, modified = self.tagging(message)
        ret = ''
        first = True
        for m in modified:
            print(m)
            pronounce = m.pronounce[:]
            if not first and not (m.pos == '助詞' or m.pos == '助動詞' or m.pos == '接尾辞'):
                ret += '/'
            first = False
            if len(m.modified_accent_type) > 0:
                for i in range(len(pronounce)):
                    if i in m.modified_accent_type:
                        ret += '\''
                    ret += pronounce[i]
                print('{} [{}]'.format(m.original, m.modified_accent_type))
            elif len(m.original) > 0 and m.original[0] == '、':
                ret += ','
            elif len(m.original) > 0 and m.original[0] == '。':
                ret += '.'
            else:
                ret += ''.join(pronounce)
        return ret


if __name__ == '__main__':
    jp = JapanesePronouncation()
    message = 'バブル期になると稟議書は１０枚以下でもＯＫになってる'
    print(jp.to_accents(message))

    words = jp.wakati(message)
    print(words)

