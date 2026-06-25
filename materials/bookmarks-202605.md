西尾のアンテナ 2026.5
## 2026.05.29
- [AIで誰もがツールを作る時代、実は来ないんじゃないか説 - Sweet Escape](https://www.keisuke69.net/entry/2026/05/22/073948)
    - 「作りたい人」は希少なのと、保守が大変という見解。強く同意するけど、他のシナリオもありそう。
- [【Skill配布あり】中間記法パターン(MNP)について：どんなツールでも簡単&爆速&安定にAI化する内部実装方法｜なつ (生活者/デザイナー/リサーチャー)](https://note.com/art_reflection/n/nccfe6cc57073)
    - なるべく決定論的な仕組みを切り出してコードに落とし込むのが重要だと思う
## 2026.05.28
- [Claude Codeをビジネス職が安全に使うためのエンジニア主導研修 | CyberAgent Developers Blog](https://developers.cyberagent.co.jp/blog/archives/64022/)
    - いいね。
## 2026.05.27
- [OpenClaw作者、エージェントスキルのチェックツール「Skill Cleaner」をGitHubで公開 | gihyo.jp](https://gihyo.jp/article/2026/05/skill-cleaner)
    - スキルがトークンを無駄遣いしないようにしてくれるらしい
- [ナレッジグラフをエージェントの「記憶」にする設計](https://zenn.dev/knowledge_graph/articles/kg-agent-ontology-design)
    - ナレッジグラフなかなか手を出せないでいる
- [イノベーション実現の鍵は「移転」にある｜山口周](https://note.com/shu_yamaguchi/n/n08c6c946767f)
    - イノベーションが起きるのは2パターン。どちらも「移転」が起こっているという分析
        - 未来の課題を現代で解決する。他の業界で成功した問題解決を自業界に適用する
- [Catch security issues as Claude writes code - Claude Code Docs](https://code.claude.com/docs/en/security-guidance)
    - Anthropic公式プラグインが脆弱性を検査してくれる。コード書いてる最中にも指摘してくれるのは良いかも
## 2026.05.26
- [Anthropic's coordinated vulnerability disclosure dashboard](https://red.anthropic.com/2026/cvd/)
    - 昨日に引き続き、Mythos Previewのパフォーマンスに関する情報。Project Grasswingにより、これまで1596件の脆弱性がメンテナーに開示され、100件弱が修正済みとのこと
- [「AI推進担当」になった人が最初に向き合うべき、たった一つの問い｜リベルクラフト公式note](https://note.com/libercraft/n/n175698f380c4)
    - 「AI推進とは、事業課題をAI要件に翻訳し、プロジェクトとして動かし続ける仕事である。」
    - 人間の判断している箇所を洗い出すことから始める
- [[2605.22166] Adapting the Interface, Not the Model: Runtime Harness Adaptation for Deterministic LLM Agents](https://arxiv.org/abs/2605.22166)
    - Agentの振る舞いの改善をハーネスの方に反映すればモデルを変えても成立する、という話みたい
- [Xユーザーのelvisさん: 「Just released my new /lesson-generator skill. Use it with your agent to learn anything: - generate lessons/courses on any topic - include nano-banana images with my /image-generator skill - present the course as an HTML artifact And it's also available to use in our academy. https://t.co/6et9bAjXBF」 / X](https://x.com/omarsar0/status/2058284649630339194)
    - 教育コンテンツを生成するClaude Codeのプラグインだそう。すごそう。
    - 生成したコンテンツのサイト？ https://academy.dair.ai/
    - プラグインの配布元 https://github.com/dair-ai/dair-academy-plugins/
## 2026.05.25
- [OpenClaw 入門 (1) - 概要｜npaka](https://note.com/npaka/n/n562ebadce4b5)
- [OpenClaw入門 (2) - 事始め｜npaka](https://note.com/npaka/n/n1f3b978ed400)
    - OpenClaw 結局触れてないな
- [Claude Codeを業務基盤にするために押さえるたった5つのこと——Claude Code超入門 vol.3 - STUDY HACKER（スタディーハッカー）｜社会人の勉強法＆英語学習](https://studyhacker.net/toshimitsu-miyachi-interview03)
    - 非エンジニア向けの記事。vol.1 が分かりにくい。vol.2はインストールの説明
- [Center for Responsible, Decentralized Intelligence at Berkeley](https://rdi.berkeley.edu/blog/exploitgym/)
    - *ExploitGymは、ユーザー空間プログラム、GoogleのV8 JavaScriptエンジン（Chromeの基盤となるエンジン）、Linuxカーネルなど、実世界の898の脆弱性を対象とした新しいベンチマークです。*
    - Claude MythosとGPT-5.5が比較されている。こう見るとGPT-5.5もかなり高性能だと知れる。
- [Managed Agents API on Agent Platformを解説 - G-gen Tech Blog](https://blog.g-gen.co.jp/entry/managed-agents-api-explained)
    - このエージェントは、Antigravityのもののようだ
- [Future_of_Software_Engineering_Retreat_Findings.docx](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future%20_of_software_development_retreat_%20key_takeaways.pdf)
    - 2月の資料だが Thoughtworks の資料なので後で読んでおこう
## 2026.05.22
- [XユーザーのHedgieさん: 「🦔Microsoft canceled its internal Claude Code licenses this week after token-based billing made the cost untenable, even for a company with effectively infinite cloud resources. Uber's CTO sent an internal memo warning the company burned through its entire 2026 AI budget in just https://t.co/zBGccaP3e6」 / X](https://x.com/HedgieMarkets/status/2057531661785628841)
    - ![image.png](https://image.docbase.io/uploads/0d870191-6670-41db-a087-7bf1b1e8b14a.png =WxH)
    - 長時間動くAIエージェントを当てにし過ぎない方が良いのかも
- [SaaS で AI Agent を提供するあなたへ贈る、Bedrock AgentCore マルチテナント実装 - Runtime 編](https://zenn.dev/aws_japan/articles/6640624910acc3?shem=dsdf,sharefoc,agadiscoversdl,,sh/x/discover/m1/4)
    - Bedrock を使う時は来るだろうか。AWSの中の人が書いた記事なので一応ブクマ
- [コードレビューを6段階にしたら、AIと人間の分業が見えた](https://zenn.dev/kenimo49/articles/code-review-6-stages-ai-human-boundary)
    - ![image.png](https://image.docbase.io/uploads/f5dda83e-6634-4636-b4df-158044f3fab1.png =WxH)
    - 上の3つはハーネスエンジニアリングで言われているやつかなと思った。著者も認識しているが4が切り分けもレビューそのものも結局難しい。見落としは仕様と実装の不整合らしいから、AIに仕様を読ませるハーネスを追加すると良さそう。
- [AIハーネスの心臓部 ── AIのAIによるAIのためのナレッジグラフ（連載Part 2）](https://zenn.dev/aircloset/articles/f6c990989e60d4)
    - ソフトウェア保守をするために、システムのメンタルモデルをナレッジグラフで表すというアイデア。
    - _人がコードを書く前提の世界では現実的に維持できないけど、AIが書く前提に切り替わった瞬間に成立するタイプの設計です。_
- [Build Long-running AI agents that pause, resume, and never lose context with ADK - Google Developers Blog](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/)
    - *このチュートリアルでは、エージェント開発キット（ADK）を使用して、数週間安定して動作する新入社員オンボーディングコーディネーターエージェントを構築する手順を説明します。*
    - *このチュートリアルで紹介するパターン（永続的なステートマシン、永続的なチェックポイントと再開、イベント駆動型のアイドル時間処理、マルチエージェント委任）は、エージェントを単なる対話型ツールから、数日から数週間にわたるワークフローを確実に管理する本番環境のバックグラウンドプロセスへと変革します。*

## 2026.05.20
- [Claudeを組織で安全に使うために NOT A HOTELで実施している４つのレイヤー｜kajinari | モダンな情シス](https://note.com/kajinari/n/n6494b35a4826)
    1. アクセス制御：ドメインクレーム + Okta SSO 必須化 + IdP プロビジョニング自動化で、シャドーテナントを構造的に発生させない状態を作り、申請対応や退職時の棚卸しを自動化しました。
    1. ガードレール：Managed Settings を MDM 経由で配布し、危険な振る舞いや未承認 MCP をそもそも実行できない設定にしました。API キーは 1Password CLI(op)で平文ファイル保存を避け、間接プロンプトインジェクションの被害面を最小化しています。
    1. コスト最適化：Anthropic Console 経由の従量課金で「使わない人に課金しない」状態を実現し、利用実績が認められたメンバーには claude.ai シートを段階的に配賦。OpenTelemetry + BigQuery で利用量を個人別・部署別に可視化し、課金プランの最適化提案までつなげています。
    1. 組織への展開：全社勉強会、利用ガイドライン、段階的ロールアウトで「安全に使える人」を継続的に増やしています。
- [[2605.18747] Code as Agent Harness](https://arxiv.org/abs/2605.18747)
    - サーベイ論文![image.png](https://image.docbase.io/uploads/d30f192a-5bb7-4c9f-ace4-04f85621fc26.png =WxH)
    - 本調査において、コードとは、実行可能システムによって生成または消費されるプログラム、スクリプト、形式仕様、証明スクリプト、APIスキーマ、ツール定義、テスト、リポジトリ、シミュレータ、構成ファイル、およびトレースやログなどのコードに隣接する実行アーティファクトを含む、実行可能または機械検証可能な成果物を指します。
## 2026.05.19
- [We built SmithDB, the data layer for agent observability](https://www.langchain.com/blog/introducing-smithdb)
    - Claudeをクライアントとするのではなく、独立したAIエージェントとして作る時に、トレースなどを保管してくれる層らしい。LangChainは使ったことないけどそのうち調べたい![image.png](https://image.docbase.io/uploads/1097a03f-37d1-4213-866c-1b361c356c0a.png =WxH)
- [AI Agents Need Your Data to Work. Your SaaS Vendors Are Making Sure They Can't.](https://www.thestateofbrand.com/news/saas-vendor-data-ownership)
    - AIによる陳腐化を恐れてSaaSサービスは競争力の源泉であるデータをAIから隠そうとするが、それは利用者にサービスを自作させる圧力を高めることになる。
- [Stainless - Blog - Stainless is joining Anthropic](https://www.stainless.com/blog/stainless-is-joining-anthropic/)
    - StainlessはAPIやSDK、MCP、ドキュメントを生成するための有償サービス。Anthropicに買収されたので普通の人は使えなくなった。今後Claude CodeのSkillか何かになるのかな

## 2026.05.18
- [DuckDBをクライアント／サーバ化する「Quack」プロトコルが登場。複数のDuckDBインスタンス間で接続が可能に － Publickey](https://www.publickey1.jp/blog/26/duckdbquackduckdb.html)