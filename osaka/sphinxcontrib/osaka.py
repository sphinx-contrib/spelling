# -*- encoding: utf-8 -*-

"""
Convert standard Japanese into Osaka dialect.

:Original Authors: Katsunari Seki, Hiro Kanno

Original code is in http://www.geocities.co.jp/Hollywood/4078/osaka/osakajs.html

"""

__version__ = "0.1"
__licence__ = "MIT/X"
__authoer__ = "SHIBUKAWA Yoshiki <yoshiki at shibu.jp>"

_table = [
    [u"ありがとうございました", u"おおきに"],
    [u"あなた", u"あんさん"],
    [u"あんな", u"あないな"],
    [u"りますので", u"るさかいに"],
    [u"りますから", u"るさかいに"],
    [u"あります", u"あるんや"],
    [u"あるいは", u"せやなかったら"],
    [u"或いは", u"せやなかったら"],
    [u"ありません", u"おまへん"],
    [u"ありました", u"おました"],
    [u"いない", u"おらへん"],
    [u"いまどき", u"きょうび"],
    [u"いわゆる", u"なんちうか，ようみなはんいわはるとこの"],
    [u"思いますが", u"思うんやが"],
    [u"思います", u"思うで"],
    [u"いただいた", u"もろた"],
    [u"いただきます", u"もらうで"],
    [u"いただきました", u"もろた"],
    [u"いくら", u"なんぼ"],
    [u"いるか", u"おるか"],
    [u"yいますので", u"おるさかいに"],
    [u"いますから", u"おるさかいに"],
    [u"いちど", u"いっぺん"],
    [u"一度", u"いっぺん"],
    [u"いますが", u"おるけどダンさん"],
    [u"いました", u"おったんや"],
    [u"います", u"いますわ"],
    [u"えない", u"えへん"],
    [u"おかしな", u"ケッタイな"],
    [u"おきました", u"おいたんや"],
    [u"かなあ", u"かいな"],
    [u"かならず", u"じぇったい"],
    [u"かわいい", u"メンコイ"],
    [u"おそらく", u"ワイが思うには"],
    [u"恐らく", u"ワイが思うには"],
    [u"おもしろい", u"オモロイ"],
    [u"面白い", u"おもろい"],
    [u"ください", u"おくんなはれ"],
    [u"詳しく", u"ねちっこく"],
    [u"くわしく", u"ねちっこく"],
    [u"けない", u"けへん"],
    [u"ございます", u"おます"],
    [u"ございました", u"おました"],
    [u"こちら", u"ウチ"],
    [u"こんな", u"こないな"],
    [u"この頃", u"きょうび"],
    [u"このごろ", u"きょうび"],
    [u"下さい", u"くれへんかの"],
    [u"さようなら", u"ほなさいなら"],
    [u"さん", u"はん"],
    [u"しかし", u"せやけどダンさん"],
    [u"しかたない", u"しゃあない"],
    [u"仕方ない", u"しゃあない"],
    [u"しなければ", u"せな"],
    [u"しない", u"せん"],
    [u"しばらく", u"ちーとの間"],
    [u"しました", u"したんや"],
    [u"しまいました", u"しもたんや"],
    [u"しますか", u"しまっか"],
    [u"しますと", u"すやろ，ほしたら"],
    [u"しまった", u"しもた"],
    [u"しますので", u"するさかいに"],
    [u"じゃ", u"や"],
    [u"すくなくとも", u"なんぼなんでも"],
    [u"少なくとも", u"なんぼなんでも"],
    [u"ずに", u"んと"],
    [u"すごい", u"どエライ"],
    [u"少し", u"ちびっと"],
    [u"せない", u"せへん"],
    [u"そこで", u"ほんで"],
    [u"そして", u"ほんで"],
    [u"そんな", u"そないな"],
    [u"そうだろ", u"そうやろ"],
    [u"それから", u"ほんで"],
    [u"それでは", u"ほなら"],
    [u"たのです", u"たちうワケや"],
    [u"たので", u"たさかい"],
    [u"ただし", u"せやけど"],
    [u"たくさん", u"ようけ"],
    [u"だった", u"やった"],
    [u"だけど", u"やけど"],
    [u"だから", u"やから"],
    [u"だが", u"やけど"],
    [u"だろ", u"やろ"],
    [u"だね。", u"やね。"],
    [u"ちょっと", u"ちーとばかし"],
    [u"つまらない", u"しょーもない"],
    [u"であった", u"やった"],
    [u"ている", u"とる"],
    [u"ていただいた", u"てもろた"],
    [u"ていただきます", u"てもらうで"],
    [u"ていただく", u"てもらうで"],
    [u"ていただ", u"ていただ"],
    [u"ていた", u"とった"],
    [u"てる。", u"てんねん。"],
    [u"ている。", u"てんねん。"],
    [u"多く", u"ようけ"],
    [u"ですか", u"やろか"],
    [u"ですよ", u"や"],
    [u"ですが", u"やけどアンタ"],
    [u"ですね", u"やね"],
    [u"でした", u"やった"],
    [u"でしょう", u"でっしゃろ"],
    [u"できない", u"でけへん"],
    [u"ではない", u"ではおまへん"],
    [u"です", u"や"],
    [u"てない", u"てへん"],
    [u"どういうわけか", u"なんでやろかわいもよーしらんが"],
    [u"どうだ", u"どや"],
    [u"どこか", u"どこぞ"],
    [u"どんな", u"どないな"],
    [u"という", u"ちう"],
    [u"とすれば", u"とするやろ，ほしたら"],
    [u"ところが", u"トコロが"],
    [u"ところ", u"トコ"],
    [u"とても", u"どエライ"],
    [u"なぜか", u"なんでやろかわいもよーしらんが"],
    [u"なった", u"なりよった"],
    [u"なのですが", u"なんやけど"],
    [u"なので", u"やので"],
    [u"なぜ", u"なんでやねん"],
    [u"など", u"やらなんやら"],
    [u"ならない", u"ならへん"],
    [u"なりました", u"なったんや"],
    [u"のちほど", u"ノチカタ"],
    [u"のです", u"のや"],
    [u"はじめまして", u"はじめてお目にかかりまんなあ"],
    [u"ほんとう", u"ホンマ"],
    [u"ほんと", u"ホンマ"],
    [u"まいますので", u"まうさかいに"],
    [u"まったく", u"まるっきし"],
    [u"全く", u"まるっきし"],
    [u"ません", u"まへん"],
    [u"ました", u"たんや"],
    [u"ますか", u"まっしゃろか"],
    [u"ますが", u"まっけど"],
    [u"ましょう", u"まひょ"],
    [u"ますので", u"よるさかいに"],
    [u"むずかしい", u"ややこしい"],
    [u"めない", u"めへん"],
    [u"もらった", u"もろた"],
    [u"もらって", u"もろて"],
    [u"ります", u"るんや"],
    [u"らない", u"りまへん"],
    [u"りない", u"りまへん"],
    [u"れない", u"れへん"],
    [u"ます", u"まんねん"],
    [u"もっとも", u"もっとも"],
    [u"ようやく", u"ようやっと"],
    [u"よろしく", u"よろしゅう"],
    [u"るのです", u"るちうワケや"],
    [u"だ。", u"や。"],
    [u"りました", u"ったんや"],
    [u"う。", u"うわ。"],
    [u"わがまま", u"ワガママ"],
    [u"まま", u"まんま"],
    [u"われわれ", u"ウチら"],
    [u"わたし", u"わい"],
    [u"わない", u"いまへん"],
    [u"本当", u"ホンマ"],
    [u"全て", u"みな"],
    [u"全然", u"さらさら"],
    [u"ぜんぜん", u"サラサラ"],
    [u"大変な", u"エライ"],
    [u"大変", u"エライ"],
    [u"非常に", u"どエライ"],
    [u"違う", u"ちゃう"],
    [u"私", u"わい"],
    [u"古い", u"古くさい"],
    [u"最近", u"きょうび"],
    [u"難しい", u"ややこしい"],
    [u"面倒", u"難儀"],
    [u"遅い", u"とろい"],
    [u"良い", u"ええ"],
    [u"同時", u"いっぺん"],
    [u"先頭", u"アタマ"],
    [u"最後", u"ケツ"],
    [u"我々", u"うちら"],
    [u"商人", u"あきんど"],
    [u"商売", u"ショーバイ"],
    [u"商業", u"ショーバイ"],
    [u"誰", u"どなたはん"],
    [u"再度", u"もっかい"],
    [u"再び", u"もっかい"],
    [u"無料", u"タダ"],
    [u"自分", u"オノレ"],
    [u"失敗", u"シッパイ"],
    [u"優先", u"ヒイキ"],
    [u"何も", u"なあんも"],
    [u"何か", u"何ぞ"],
    [u"いい", u"ええ"]]

_table_cache = {}

def _create_table_cache():
    if _table_cache:
        return
    for standard, osaka in _table:
        items = _table_cache.setdefault(standard[0], [])
        items.append([standard, osaka])
        items.sort(key=len, reverse=True)


def convert(src):
    """
    This module converts standard Japanese into Osaka diagram.

    :param src: input string(standard Japanese)
    :type  src: unicode
    :return: converted string
    :rtype: unicode
    """
    if not isinstance(src, unicode):
        raise ValueError(
            "input of osaka.convert must be 'unicode' not %s" % type(src))

    _create_table_cache()
    words = []
    index = 0
    last_copy = 0
    last = len(src)
    while index < last:
        matched_list = _table_cache.get(src[index])
        if not matched_list:
            index += 1
            continue
        for standard, osaka in matched_list:
            if src[index:index+len(standard)] == standard:
                words.append(src[last_copy:index])
                words.append(osaka)
                last_copy = index + len(standard)
                index = last_copy - 1
                continue
        index += 1
    words.append(src[last_copy:])
    return u"".join(words)


def setup(app):
    app.connect("doctree-resolved", convert_handler_for_sphinx)


def convert_handler_for_sphinx(app, doctree, docname):
    from docutils.nodes import Text
    encoding = app.config.source_encoding
    for node in doctree.traverse(Text):
        node.data = convert(node.data.decode(encoding)).encode(encoding)


def test():
    test = u"""親譲りの無鉄砲で子供の頃から損ばっかりしている。
小学校にいる時、学校の二階から飛び降りて一週間ほど腰を抜かしたことがある。
なぜそんな無茶をしたと聞く人がいるかもしれない。
別に深い理由でもない。"""
    print convert(test)

if __name__ == "__main__":
    test()
