===============
Python Tutorial
===============

Source text was copied from http://www.python.jp/doc/release/tut/node5.html.
Thank you for Japanese translation team.

3. 形式ばらない Python の紹介
=============================

以下の例では、入力と出力は (``>>>`` や ``...``) といった プロンプトがあるかないかで区別します: 例どおりに実行するなら、 プロンプトが表示されているときに、例中のプロンプトよりも後ろの内容全てを タイプ入力しなければなりません; プロンプトが先頭にない行はインタプリタ からの出力です。

例中には二次プロンプトだけが表示されている行がありますが、これは 空行を入力しなければならないことを意味するので注意してください; 空行の入力は複数の行からなる命令の終わりをインタプリタに教えるために 使われます。

このマニュアルにある例の多くは、対話プロンプトで入力されるものでも コメントを含んでいます。Python におけるコメント文はハッシュ文字 "#" で始まり、物理行の終わりまで続きます。 コメントは行の先頭にも、空白やコードの後にも書くことができますが、 文字列リテラル (string literal) の内部に置くことはできません。 文字列リテラル中のハッシュ文字はただのハッシュ文字です。

.. code-block:: python

   # これは１番目のコメント
   SPAM = 1                 # そしてこれは２番目のコメント
                            # ... そしてこれは３番目!
   STRING = "# これはコメントではありません。"

3.1 Python を電卓として使う
---------------------------

それでは、簡単な Python コマンドをいくつか試しましょう。 インタプリタを起動して、 一次プロンプト、 ``>>>`` が現れるのを待ちます。 (そう長くはかからないはずです)

3.1.1 数
~~~~~~~~

インタプリタは単純な電卓のように動作します。 式をタイプ入力することができ、その結果が書き出されます。 式の文法は素直なものです。 演算子 ``+``, ``-``, ``*``, ``/`` は (Pascal や C といった) 他のほとんどの言語と同じように動作します。 括弧をグループ化に使うこともできます。例えば:

.. code-block:: python
 
   >>> 2+2
   4
   >>> # これはコメント
   ... 2+2
   4
   >>> 2+2  # そしてこれはコードと同じ行にあるコメント
   4
   >>> (50-5*6)/4
   5
   >>> # 整数の除算は floor (実数の解を越えない最大の整数) を返す:
   ... 7/3
   2
   >>> 7/-3
   -3

等号 ("=") は変数に値を代入するときに使います。 代入を行っても、その結果が次のプロンプトの前に出力されたりはしません:

.. code-block:: python

   >>> width = 20
   >>> height = 5*9
   >>> width * height
   900

複数の変数に同時に値を代入することができます:

.. code-block:: python

   >>> x = y = z = 0  # x と y と z をゼロにする
   >>> x
   0
   >>> y
   0
   >>> z
   0

浮動小数点は完全にサポートしています; 被演算子の型が混合されているときには、 演算子は整数の被演算子を浮動小数点型に変換します。

.. code-block:: python

   >>> 3 * 3.75 / 1.5
   7.5
   >>> 7.0 / 2
   3.5

複素数もサポートされています。虚数は接尾辞 "j" または "J" を 付けて書き表します。ゼロでない実数部をもつ複素数は "(real+imagj)" のように書き表すか、 "complex(real, imag)" 関数で生成できます。

.. code-block:: python

   >>> 1j * 1J
   (-1+0j)
   >>> 1j * complex(0,1)
   (-1+0j)
   >>> 3+1j*3
   (3+3j)
   >>> (3+1j)*3
   (9+3j)
   >>> (1+2j)/(1+1j)
   (1.5+0.5j)

複素数は、常に実部と虚部に相当する二つの浮動小数点数で表されます。 複素数 z からそれぞれの部分を取り出すには、z.real と z.imag を使います。

.. code-block:: python

   >>> a=1.5+0.5j
   >>> a.real
   1.5
   >>> a.imag
   0.5

数値を浮動小数点数や整数へに変換する関数 (float(), int(), long()) は複素数に対しては動作しません -- 複素数を実数に変換する方法には、ただ一つの正解というものがないからです。 絶対値 (magnitude) を (浮動小数点数として) 得るには abs(z) を 使い、実部を得るには z.real を使ってください。

.. code-block:: python

	>>> a=3.0+4.0j
	>>> float(a)
	Traceback (most recent call last):
	  File "<stdin>", line 1, in ?
	TypeError: can't convert complex to float; use abs(z)
	>>> a.real
	3.0
	>>> a.imag
	4.0
	>>> abs(a)  # sqrt(a.real**2 + a.imag**2)
	5.0
	>>>

対話モードでは、最後に印字された式は変数 _ に代入されます。 このことを利用すると、 Python を電卓として使うときに、計算を連続して 行う作業が多少楽になります。以下に例を示します:

.. code-block:: python

	>>> tax = 12.5 / 100
	>>> price = 100.50
	>>> price * tax
	12.5625
	>>> price + _
	113.0625
	>>> round(_, 2)
	113.06
	>>>

ユーザはこの変数を読取り専用の値として扱うべきです。 この変数に明示的な代入を行ってはいけません -- そんなことをすれば、 この組み込み変数と同じ名前で、元の組み込み変数の不思議な動作を覆い隠して しまうような、別個のローカルな変数が生成されてしまいます。

3.1.2 文字列
~~~~~~~~~~~~

数のほかに、Python は文字列も操作できます。 文字列はいくつもの方法で表現できます。 文字列はシングルまたはダブルのクォートで囲みます。

.. code-block:: python

	>>> 'spam eggs'
	'spam eggs'
	>>> 'doesn¥'t'
	"doesn't"
	>>> "doesn't"
	"doesn't"
	>>> '"Yes," he said.'
	'"Yes," he said.'
	>>> "¥"Yes,¥" he said."
	'"Yes," he said.'
	>>> '"Isn¥'t," she said.'
	'"Isn¥'t," she said.'

文字列リテラルはいくつかの方法で複数行にまたがって記述できます。継続行 を使うことができ、これには行の末尾の文字を バックスラッシュにします。こうすることで、次の行が現在の行と論理的に 継続していることを示します:

.. code-block:: python

	hello = "This is a rather long string containing¥n¥
	several lines of text just as you would do in C.¥n¥
	    Note that whitespace at the beginning of the line is¥
	 significant."

	print hello

¥n を使って文字列に改行位置を埋め込まなくてはならないことに注意 してください; 末尾のバックスラッシュの後ろにある改行文字は無視されます。 従って、上の例は以下のような出力を行います:

::

   This is a rather long string containing
   several lines of text just as you would do in C.
       Note that whitespace at the beginning of the line is significant.

一方、文字列リテラルを ''raw'' 文字列にすると、¥n のような エスケープシーケンスは改行に変換されません。逆に、行末のバックスラッシュ やソースコード中の改行文字が文字列データに含められます。つまり、以下の例:

.. code-block:: python

   hello = r"This is a rather long string containing¥n¥
   several lines of text much as you would do in C."

   print hello

は、以下のような出力を行います:

::
   This is a rather long string containing¥n¥
   several lines of text much as you would do in C.

また、対になった三重クォート """ または ''' で 文字列を囲むこともできます。 三重クォートを使っているときには、行末をエスケープする必要はありません、 しかし、行末の改行文字も文字列に含まれることになります。

.. code-block:: python

   print """
   Usage: thingy [OPTIONS] 
        -h                        Display this usage message
        -H hostname               Hostname to connect to
   """

は以下のような出力を行います::

   Usage: thingy [OPTIONS] 
        -h                        Display this usage message
        -H hostname               Hostname to connect to

インタプリタは、文字列演算の結果を、タイプ入力する時のと同じ方法で 出力します: 文字列はクオート文字で囲い、クオート文字自体やその他の 奇妙な文字は、正しい文字が表示されるようにするために バックスラッシュでエスケープします。 文字列がシングルクオートを含み、かつダブルクオートを含まない場合には、 全体をダブルクオートで囲います。そうでない場合にはシングルクオートで 囲みます。 (後で述べる print を使って、クオートやエスケープ のない文字列を書くことができます。)

文字列は + 演算子で連結させる (くっつけて一つにする) ことができ、 * 演算子で反復させることができます。

.. code-block:: python

   >>> word = 'Help' + 'A'
   >>> word
   'HelpA'
   >>> '<' + word*5 + '>'
   '<HelpAHelpAHelpAHelpAHelpA>'

互いに隣あった二つの文字列リテラルは自動的に連結されます: 例えば、上記の最初の行は "word = 'Help' 'A'" と書くことも できました; この機能は二つともリテラルの場合にのみ働くもので、 任意の文字列表現で使うことができるわけではありません。

.. code-block:: python

   >>> 'str' 'ing'             #  <-  これは ok
   'string'
   >>> 'str'.strip() + 'ing'   #  <-  これは ok
   'string'
   >>> 'str'.strip() 'ing'     #  <-  これはダメ
     File "<stdin>", line 1, in ?
       'str'.strip() 'ing'
                     ^
   SyntaxError: invalid syntax

文字列は添字表記 (インデクス表記) することができます; C 言語と同じく、文字列の最初の文字の添字 (インデクス) は 0 となります。 独立した文字型というものはありません; 単一の文字は、単に サイズが 1 の文字列です。Icon 言語と同じく、部分文字列を スライス表記: コロンで区切られた二つのインデクスで指定する ことができます。

.. code-block:: python

   >>> word[4]
   'A'
   >>> word[0:2]
   'He'
   >>> word[2:4]
   'lp'

スライスのインデクスには便利なデフォルト値があります; 最初のインデクスを省略すると、0 と見なされます。 第 2 のインデクスを省略すると、スライスしようとする文字列のサイズと みなされます。

.. code-block:: python

   >>> word[:2]    # 最初の 2 文字
   'He'
   >>> word[2:]    # 最初の 2 文字を除くすべて
   'lpA'

C 言語の文字列と違い、Python の文字列は変更できません。 インデクス指定された文字列中のある位置に代入を行おうとすると エラーになります:

.. code-block:: python

   >>> word[0] = 'x'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: object doesn't support item assignment
   >>> word[:1] = 'Splat'
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: object doesn't support slice assignment

一方、要素どうしを組み合わせた新たな文字列の生成は、簡単で効率的です:

.. code-block:: python

   >>> 'x' + word[1:]
   'xelpA'
   >>> 'Splat' + word[4]
   'SplatA'

スライス演算には便利な不変式があります: s[:i] + s[i:] は s に等しくなります。

.. code-block:: python

   >>> word[:2] + word[2:]
   'HelpA'
   >>> word[:3] + word[3:]
   'HelpA'

スライス表記に行儀の悪いインデクス指定をしても、値はたしなみよく処理 されます: インデクスが大きすぎる場合は文字列のサイズと置き換えられます。 スライスの下境界 (文字列の左端) よりも小さいインデクス値を上境界 (文字列の右端) に指定すると、空文字列が返されます。

.. code-block:: python

   >>> word[1:100]
   'elpA'
   >>> word[10:]
   ''
   >>> word[2:1]
   ''

インデクスを負の数にして、右から数えることもできます。 例えば:

.. code-block:: python

   >>> word[-1]     # 末尾の文字
   'A'
   >>> word[-2]     # 末尾から 2 つめの文字
   'p'
   >>> word[-2:]    # 末尾の 2 文字
   'pA'
   >>> word[:-2]    # 末尾の 2 文字を除くすべて
   'Hel'

-0 は 0 と全く同じなので、右から数えることができません。 注意してください!

.. code-block:: python

   >>> word[-0]     # (-0 は 0 に等しい)
   'H'

負で、かつ範囲外のインデクスをスライス表記で行うと、インデクス は切り詰められます。しかし、単一の要素を指定する (スライスでない) インデクス指定でこれを行ってはいけません:

.. code-block:: python

   >>> word[-100:]
   'HelpA'
   >>> word[-10]    # エラー
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   IndexError: string index out of range

スライスの働きかたをおぼえる最も良い方法は、 インデクスが文字と文字のあいだ (between) を指しており、最初の 文字の左端が 0 になっていると考えることです。そうすると、 n 文字からなる文字列中の最後の文字の右端はインデクス n となります。例えば::

   +---+---+---+---+---+ 
   | H | e | l | p | A |
   +---+---+---+---+---+ 
   0   1   2   3   4   5 
  -5  -4  -3  -2  -1

といった具合です。

数が記された行のうち、最初の方の行は、文字列中のインデクス 0...5 の 位置を表します; 次の行は、対応する負のインデクスを表しています。 i から j までのスライスは、それぞれ i, j とラベル付けされたけられた端点間のすべての文字からなります。

非負のインデクス対の場合、スライスされたシーケンスの長さは、スライスの両端の インデクスが境界内にあるかぎり、インデクス間の差になります。 例えば、 word[1:3] の長さは 2 になります。

組込み関数 len() は文字列の長さ (length) を返します。

.. code-block:: python

   >>> s = 'supercalifragilisticexpialidocious'
   >>> len(s)
   34
