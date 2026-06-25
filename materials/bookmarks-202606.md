西尾のアンテナ 2026.6
## 注目テーマ
* AIを前提とした新しい世の中のトレンド
    * ソフトウェア開発ライフサイクル
    * SaaSビジネス
    * マーケティングと消費行動
    * ホワイトワーカーの生産性
* 業務に使うAIエージェントの構築技法

## 2026.6.22
* [AIエージェント時代の品質保証 ― 監査駆動フィードバック開発という考え方](https://zenn.dev/ichikawa_y/articles/audit-driven-feedback-development)
    * 自動化できるなら監査を受けても良い。最初からあれこれ監査しすぎないように注意。
* [Sakana Fugu — Multi-Agent System as a Model](https://sakana.ai/fugu/)
    * 予告されてたけど正式リリースしたのか。価格と安定性はいかほどだろう。
* [インサイドセールス構築・代行 | NEC VALWAY](https://www.necvw.co.jp/ja/sales-dx/inside.html)
    * ベンチマークとして要ブクマ
* [Steering Claude Code: skills, hooks, subagents and more | Claude](https://claude.com/ja/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)
    * ルール、と出力スタイル知らなかった
* [自己改善エージェントはなぜ前提を覆せないのか ― 局所最適とハーネスでの脱出](https://zenn.dev/layerx/articles/b36ceffe6b5e20)
    * 難しくて良く分からなかった
* [【draw.io】エンジニアの「雑なMermaid」を、綺麗な図解に変換する【アップデート版】 #初心者 - Qiita](https://qiita.com/ktdatascience/items/735ebfa8504fc658c812)
    * draw.io のXMLを書かせる
* [ローカルLLMをいつ使うべきか？](https://zenn.dev/sompojapan_dx/articles/74624afa03040c)
    * 安いから使うのではない。情報の秘匿性が問題になるケース以外だと、レイテンシが低く安定できることが価値で、それが必要なタスクを見極めてファインチューニングできるのであれば、という前提がある。
## 2026.6.19
* AIエージェントによる開発が一般化するとともに新しいバージョン管理システムの提案が相次いでいる
    * [Lore | 次世代オープン ソース バージョン管理 - Lore](https://lore.org/)
        * ゲーム開発向け
    * DeltaDB (6.15の記事)
    * [GitLab、AIエージェント向けの次世代Git互換ソースコード管理サービス「Project Switch」発表。最大で50倍高速かつ半分のトークンで利用可能に － Publickey](https://www.publickey1.jp/blog/26/gitlabaigitproject_switch50.html)
    * [Cursor、AIエージェントのワークロードに対応したGitフォージ「Origin」を発表|CodeZine（コードジン）](https://codezine.jp/news/detail/24581)
* [From AGI to ASI — Google DeepMind](https://deepmind.google/research/publications/239142/)
   * ついに議論がAGIの先に進み始めた
* [生成AI時代のデータ統合基盤、そして「コンピュータ」の姿とは？ | IT Leaders](https://it.impress.co.jp/articles/-/29451)
    * DevRevは グラフデータを中心に据え、LLMをそのデータを処理するコンピュータとみなす。2022年にDevCRMをリリースしたらしい。データの持ち方から再考してみるべきかもしれない。
* [高卒・無所属の札幌在住主夫、AIとの対話約1年半で、単著論文がSpringer Natureの心理学誌「Discover Psychology」で査読へ - どさんこ会社のプレスリリース](https://www.value-press.com/pressrelease/376053)
    * *目の前の問いを、外の人が検証できる形へ変え続けていたら、論文のほうが自分より先に査読へ着いていました*
    * かっこいい
## 2026.6.17
* [エージェントスキルライブラリ - AIDB](https://ai-data-base.com/agent-skill-library)
    * 論文解説サイトが、解説した論文に基づくエージェントスキルを「会員向けに」提供している。プライベートな試みとしては良いと思うけどサービスにするというと何か引っかかるものがある。あと、論文からスキルを作るスキルがあるんじゃないの？

## 2026.6.16
* [XユーザーのKoichiさん: 「Claude Code と Codex の往復コピペをやめたくて、agmsg を作った」 / X](https://x.com/fujibee/status/2059357190725783892)
    * トークン負荷を分散する意味でも分業は検討したい。
* [Skillに context: fork を1行足すだけで、Claude Codeのコンテキストが綺麗になった | DevelopersIO](https://dev.classmethod.jp/articles/claude-code-context-fork/)
    * 長時間タスクのコンテキスト分離について調べてた時に見つけた。`context: fork` ってあるんだ。

## 2026.6.15
* [Shudesu/line-harness-oss: Open-source LINE Official Account CRM — free alternative to paid tools. Step delivery, broadcasts, forms, rich menus, scoring, automation, and more.](https://github.com/Shudesu/line-harness-oss)
    * 作者のインタビュー動画を見て遅ればせながら認知した。Cloudflareの無料枠を使うことで有償サービスを代替できるもので、オープンソース化されている
    * https://gemini.google.com/share/d/1FisuU9yzACk-ya5vvqz6Pv4v58EP51mI?usp=sharing
* [AIへの指示まで履歴として保存する新バージョン管理システム「DeltaDB」をZedが発表|au Webポータル経済・ITニュース](https://article.auone.jp/detail/1/3/7/48_7_r_20260612_1781254642884802?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * まだ提供前みたい。GitにコーディングAIとの対話履歴を残すアイデアは別のところでも見た。ニーズがありそう
* [Claude Fable 5に作ってもらった日本語プログラミング入門教材「言語の庭」が凄い](https://zenn.dev/nextbeat/articles/2026-06-cs-edu-site-fable5?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * AIで人間の学習を支援するという方向には可能性を感じる
* [AI Readyな設計書を目指して。人もAIも読みやすい設計書管理 #GitHubActions - Qiita](https://qiita.com/grhg/items/eee10528b403baf89631?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * ちょっと思ってたよりツール寄りの話だった
    * *設計書を AI でも扱いやすくしつつ、人が読むときの見やすさも保ちたい場合、Markdown + MkDocs Material + GitHub Pages は試す価値のある構成*
* [OpenClaw+AWSで情報収集botを作る方法と、そのリスク](https://zenn.dev/exwzd/articles/20260522-event-monitor?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * リスク=自動巡回を禁止しているサイトの存在と、危険なサイトによる乗っ取り
* [XユーザーのSatya Nadellaさん: 「A frontier without an ecosystem is not stable」 / X](https://x.com/satyanadella/status/2066182223213293753)
    * どうやって学習サイクルを構築するか検討する必要がある。
* [機能を作るな。楽して作るな。 （LayerX社内資料） Don’t Build Features. Don’t Take the Easy Way Out. - Speaker Deck](https://speakerdeck.com/mosa_siru/don-t-build-features-dot-don-t-take-the-easy-way-out)
    * 速いのは前提だけど、楽なのは危険ということか
## 2026.6.12
* [AIエージェント時代の権限管理が、いまアツい - LayerX エンジニアブログ](https://tech.layerx.co.jp/entry/ai-agent-authorization)
    * 大変だということは分かる。答えはまだないらしい
* [Claude Code の Dynamic Workflows を試す前に知っておきたいこと（特にトークン消費の話） #AI - Qiita](https://qiita.com/leomarokun/items/a7a9068324a8fa2f6e0d?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * *プロンプトのどこかに `ultracode`が含まれていると、Claude Code がそのキーワードをハイライトし、ターンごとに作業するのではなくワークフロースクリプトを書いてくれます*
    * こわいからまだ使えない
* [「速く作る」から「正しく作る」へ ─ AI活用レベル3段階のロードマップ｜AI Engineering Summit Tokyo 2026 登壇レポート - Findy Tech Blog](https://tech.findy.co.jp/entry/2026/06/10/100000?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * レベル3は要件定義とQAをAIが支援すること、らしい
* [バイブ コーディングはローカルホストで終わる | HackerNoon](https://hackernoon.com/lang/ja/vibe-coding-ends-at-localhost)
    * 開発環境と実行環境が分離すると、AIエージェントは途端に無能になる、と。なるほど？
    * コメント欄では、実行環境側にもエージェントを置けば良いとか意見が出ていた
* [手順書をエージェントに実行させる——5年使ったWindowsからMacへの移行を「RUNBOOK as Code」で乗り切った話](https://zenn.dev/tokium_dev/articles/runbook-as-prompt-agent-migration?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * 環境の移行を双方にAIエージェントを入れれば自動化できる、かも
* [自分専用のAIニュースキュレーターをCodexで作って約1か月運用してみた](https://zenn.dev/mkj/articles/966c62588bd8fc?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * これやりたい。情報源をどうするか。
* [LLMと共に進化するプロセスを目指して - Speaker Deck](https://speakerdeck.com/ymatsuwitter/llmtogong-nijin-hua-surupurosesuwomu-zhi-site)
    * 従来の開発がほぼゼロコストになったので、その周辺を仕組み化できるし、しなければいけない。
## 2026.6.10
* [XユーザーのAddy Osmaniさん: 「Loop Engineering.」 / X](https://x.com/addyosmani/status/2064127981161959567)
    * Addy Osmani氏が共有した「ループエンジニアリング（Loop Engineering）」の要点は以下の3点です。
        1. 開発者がプロンプトを打つのではなく、AIエージェントにプロンプトを打ち続けさせる「ループ（仕組み）」を設計する手法である。
        1. 「自動化」「独立した作業スペース」「プロジェクト知識（スキル）」「外部ツール連携」「作成と検証の役割分担」という5つの要素で構成される。
        1. エージェントが自律して動き続けるため便利だが、トークンコストの肥大化や、人間による成果物の検証・コードへの理解（形骸化の防止）が不可欠である。
* [Harness, Scaffold, and the AI Agent Terms Worth Getting Right](https://huggingface.co/blog/agent-glossary)
    * 何か、逆に混乱した。ScaffoldとHarnessの違いは何？
        * 両者の最も決定的な違いは、Scaffoldが「設計・静的レイヤー」であるのに対し、Harnessは「実行・動的レイヤー」である点、らしい。
* [AIエージェントのトークン代を節約するNetflixのエンジニアが作ったツール「Headroom」について調べてみた #LLM - Qiita](https://qiita.com/shinkai_/items/61b10d10c63db47a64e7?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * LLMの入力から余分な情報を削除するが、節約できない場合もある
* [Opus 4.8 と GPT-5.5、effort の効き方を帰納的に明らかにした（オトナの自由研究 #23）](https://zenn.dev/nnakapa/articles/lab-23-opus48-gpt55-effort-effects?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * GPT-5.5 ＝ 思考量タイプ, Opus 4.8 ＝ 思考回数タイプ
* [プロダクトマネジメント研修を受講して振り返る過去案件の失敗事例](https://zenn.dev/nttdata_tech/articles/f4a12e031d5d63?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * 次はちゃんとやろう
* [open-code-review/README.ja-JP.md at main · alibaba/open-code-review](https://github.com/alibaba/open-code-review/blob/main/README.ja-JP.md?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * レビューの進行をコードで制御するからトークンの節約になるらしい。Goインストールするの面倒だから移植して使うか？
* [[2606.09498] Self-Harness: Harnesses That Improve Themselves](https://arxiv.org/abs/2606.09498)
<details><summary>アイデア部分の要約</summary>

    * Self-Harnessは、モデルの重みを変更するのではなく、固定されたモデルの周りにあるハーネスを「証拠（実行ログ）に基づいて進化させる」ため、以下の3つのステップを繰り返すサイクル（ループ）として設計されています。

① 弱点のマイニング（Weakness Mining）
内容: エージェントをタスクで実行し、失敗した際のログ（実行トレース）を収集します。

特徴: 単に「タイムアウトした」という表面的な結果で終わらせず、検証器（Verifier）のフィードバックとエージェントの行動を結びつけ、モデル特有の構造的な失敗パターンとして自動でクラスタリング（分類）し、具体的な証拠（エビデンス）としてまとめます。

② ハーネスの提案（Harness Proposal）
内容: 抽出された失敗パターンを基に、同じモデル自身が「プロンプター（提案者）」となってハーネスの修正案を生成します。

特徴: 闇雲にプロンプトを書き換えるのではなく、特定された弱点に対して「多様でありながら、最小限の変更（Minimal Modifications）」を加えるアプローチをとります。これにより、既存の正常な挙動を壊すリスクを抑えます。

③ 提案の検証（Proposal Validation）
内容: 提案された修正ハーネスが本当に優れているかを判断するための「厳格な門番」の役割です。

特徴: 修正のきっかけとなったタスク群（held-in）だけでなく、エージェントが関知していない未知のタスク群（held-out）でも回帰テストを行います。「既存の性能をどこも低下させず、少なくとも一方のタスク群で性能を向上させたもの」のみを合格（プロモート）とし、複数の合格案はマージされて次の世代のハーネスになります。
</details>


## 2026.6.8
* [[アップデート] Amazon Bedrock AgentCore Managed HarnessのSkillsがS3からの読み込みに対応しました | DevelopersIO](https://dev.classmethod.jp/articles/bedrock-agentcore-harness-skills-s3-source/?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * 読み取りのオーバーヘッドが気になる。同梱したら駄目なのかな？
* [【図解】エンジニアの「雑なMermaid」を、ビジネス側に刺さる図解に変換する #初心者 - Qiita](https://qiita.com/ktdatascience/items/4b35eb4e157becfac073)
    * Mermaidで雑に構造化して清書をNanobananaに任せるアイデア。図解は奥が深い
* [Claude を使って Gemini 議事録から必要な情報を抽出する仕組み](https://zenn.dev/tokium_dev/articles/d806c7ad4fd458?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * 同様の投稿はいっぱいありそうだが、まだ実践できてないのでメモ
* [推薦システムの新たなパラダイム Generative Recommendation](https://zenn.dev/rintaro121/articles/generative-recommendation?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * *GRはユーザーの行動履歴を入力とし、推薦のタスクを「次のアイテムIDを生成する問題」として定式化する*
    * なるほど、そういう意味か。DeepLearningの登場でTwo-Towerというアーキテクチャになったが、その次ということか。性能がスケーリング則で向上できるのが利点らしい
* [問い合わせ調査のリードタイムを平均70%削減 ── Claude Code Skillを"動くマニュアル"にしたZOZOTOWNの取り組み - ZOZO TECH BLOG](https://techblog.zozo.com/entry/cs-inquiry-ai-automation?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * システム保守における問い合わせ対応業務の効率化事例。
* [メモアプリの限界をグラフで超える:パーソナルナレッジグラフを実装する](https://zenn.dev/kenimo49/articles/personal-knowledge-graph-obsidian-infranodus?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    * *InfraNodus は、テキストをナレッジグラフに変換し、ネットワーク科学で分析するツールです*
    * 後で調べてみよう
* [Amazon Bedrock AgentCore 実践入門 | SBクリエイティブ](https://www.sbcr.jp/product/4815641238/)
    * Agent Coreはランタイム、Strandsはフレームワーク。Agent Coreの上でStrandsで書いたエージェントを動かせる、という理解で良いか
## 2026.6.5
* [韓非子 主道篇から学ぶClaude Codeの高度な使いこなし](https://zenn.dev/tomfook/articles/e4613c2f2fbb28)
    * 人間に忖度するAIの特性を考えると、自分の趣味、アイデアをAIに教えるのは控えるべき
    * AIに完了条件も提案させ、それを満たすかどうかで評価する（形名参同）
* [Reasoning Effort「Low」は逆効果——Opus 4.8 と GPT-5.5 を720試行で比較（オトナの自由研究 #21）](https://zenn.dev/nnakapa/articles/lab-21-opus48-gpt55-reasoning-effort)
    * Effortを下げるくらいだったらモデルをグレードダウンした方が良いのかもしれない
* [AIエージェントに1年分のニュースを読ませて4,500件の長期記憶を作って見えた課題 - LayerX エンジニアブログ](https://tech.layerx.co.jp/entry/ai-agent-long-term-memory-simulation)
    * やってみるのは大事だな。お金かかるけど
* [Generative UI Is the New Frontend | X記事](https://x.com/Saboo_Shubham_/article/2062220865643982875)
    * 忘れてた。今ならClaude Codeとかでできるのかな。
* [AnthropicがClaudeを使ってセルフサービスデータ分析を実現する方法 | Claude](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude)
    * データモデル、セマンティックレイヤー、スキル（ドキュメント）を管理（バージョン管理、テスト、メンテナンス）している
* [MAI-Thinking-1: Building a Hill-Climbing Machine](https://microsoft.ai/wp-content/uploads/2026/06/main_20260602_2.pdf)
    * ちゃんと読んでないけど、構築方法を詳細に説明している珍しいモデルらしい。
## 2026.6.3
* [XユーザーのThariqさん: 「A harness for every task: dynamic workflows in Claude Code 」 / X](https://x.com/trq212/status/2061907337154367865)
    * どういうものかは何となく分かった。しかし大規模なタスクを動的に作るのは無駄が多い気がしてならない
* [移動中でも就寝前でも、Codexと育てる「技術ノート」](https://zenn.dev/ttaniguchi/articles/instant-question-html-notes)
    * 手でブックマークとかしてる場合ではないな
## 2026.6.2
* [トークンマキシングからトークンマネジメントへ｜福島良典 | LayerX](https://note.com/fukkyy/n/n2a6a68814e72)
    * 安価なモデルや決定論的なコードに処理を逃がす、あえて人間に判断を残す、といったことも考えないといけない

## 2026.6.1
* [メルカリ、CTOの木村俊也がCHRO兼CAIOに就任 | 株式会社メルカリ](https://about.mercari.com/press/news/articles/20260601_chrocaio/)
    * なるほど、と思うけど良く決断できるね
* [Sprocketがデータ分析エージェントで「分析レシピ」を提供、分析の属人化を解消 | Web担当者Forum](https://webtan.impress.co.jp/n/2026/05/29/52726)
    * 定番っぽい分析メニューの提供と、顧客ごとのレシピも作れる、と。
* [Claude Code x Obsidianで、LLM Wiki構築 | セッションを切り替えても会話を続けられる方法 #ClaudeCode - Qiita](https://qiita.com/usayamadausako/items/c8b5cca97554f6f64782)
    * プロジェクトごとにVaultを作るのね
* [Palantir の「オントロジー」を Python で再現してみた](https://zenn.dev/channnnsm/articles/e0be25fadca0df)
    * DDDとの違いは何だろう？
* [AI 時代のソフトウェア設計の学び方 - Speaker Deck](https://speakerdeck.com/masuda220/ai-shi-dai-nosohutoueashe-ji-noxue-bifang)
    * 事業目的適合性と変更容易性がソフトウェア設計のキモ。両者を同時に判断・改善できるようになるための訓練方法とは。
* [コンパウンド戦略とは？メリット・注意点・事例・成果創出方法・Tipsをわかりやすく解説！｜Goodpatch Blog グッドパッチブログ](https://goodpatch.com/blog/compound-strategy)
    * 複数のプロダクトで顧客の業務範囲を幅広くカバーする戦略。
* [Avoiding Death on the Yellow Brick Road - by Joe Schmidt IV](https://www.a16z.news/p/avoiding-death-on-the-yellow-brick)
    * 大手に飲み込まれない生き残り戦略とは。以下が重要
        * データと学習のフライホイール
        * モデルの多様性と複雑性の管理
        * コスト最適化（安価なモデル、決定論的なコードを上手く使い分ける）
        * ガバナンス（特定のユースケースに特化すること）
* [テック業界の次の主役は「プロダクトエンジニア」という新たな職種かもしれない | Business Insider Japan](https://www.businessinsider.jp/article/2605-ai-jobs-product-engineers-managers/)
    * コーディングがほとんどゼロコストになったので、PdMを兼ねる必要がある
* [AIが変えた"品質の守り方" - Speaker Deck](https://speakerdeck.com/kkakizaki/aigabian-eta-pin-zhi-noshou-rifang)
    * 品質を担保する仕組みを作ることが仕事になる