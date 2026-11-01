"""Unit tests for stealth_fetch.classify_block.

No network and no cloakbrowser import: classify_block is pure. The URL,
title and text constants are literal snippets from
docs/superpowers/notes/2026-11-01-stealth-fetch-probe.md.
"""

from __future__ import annotations

from stealth_fetch import classify_block


REDDIT_SEARCH_URL = """https://www.reddit.com/r/algotrading/search/?q=backtest&restrict_sr=1"""

REDDIT_SEARCH_TITLE = """Reddit - Prove your humanity"""

REDDIT_SEARCH_TEXT = """Prove your humanity

We’re committed to safety and security. But not for bots. Complete the challenge below and let us know you’re a real person.

Reddit, Inc. © "2026". All rights reserved.
User Agreement
Privacy Policy
Content Policy
Help"""

OLD_REDDIT_URL = """https://old.reddit.com/login/?reason=lor2&dest=https%3A%2F%2Fold.reddit.com%2Fr%2Falgotrading%2Ftop%2F%3Ft%3Dmonth"""

OLD_REDDIT_TITLE = """Welcome to Reddit"""

OLD_REDDIT_TEXT = """Skip to main content
Log in to use old Reddit

To keep Reddit safe, accounts are required to access old Reddit. Log in, or continue without an account on reddit.com.

By continuing, you agree to our User Agreement and acknowledge that you understand the Privacy Policy.

Continue with Phone Number
Email me a one-time link
OR
Email or username 
Password 
Show password
Forgot password?
New to Reddit? 
Sign Up
Log In"""

X_SEARCH_URL = """https://x.com/i/jf/onboarding/web?redirect_after_login=%2Fsearch%3Ff%3Dlive%26q%3Dcloakbrowser&mode=login"""

X_SEARCH_TITLE = """X - The Everything App / X"""

X_SEARCH_TEXT = """See what's happening

Select an option below:

Continue with phone

Continue with Google
Continue with Google

Continue with Apple

or

Email or username

Continue

By continuing, you agree to our Terms of Service, Privacy Policy and Cookie Use."""

X_PROFILE_URL = """https://x.com/AnthropicAI"""

X_PROFILE_TITLE = """Anthropic (@AnthropicAI) / X"""

X_PROFILE_TEXT = """Anthropic
1,740 posts
Anthropic
@AnthropicAI
We're an AI safety and research company that builds reliable, interpretable, and steerable AI systems. Talk to our AI assistant @claudeai on claude.ai.
anthropic.com
Joined January 2021
2 Following
1.8M Followers
3 Affiliates
Mention
Follow
Posts
Replies
Reposts
Media
Anthropic
@AnthropicAI
15h
New Anthropic research: Automating subtle emergent misalignment research.

Red-teaming is a vital part of model safety testing, but it’s also limited by researchers’ time. To see if we could automate it, we set thousands of Claude agents the task of evading a training data Show more
477
557
3.1K
394K
Anthropic
@AnthropicAI
Oct 30
We’ve trained Claude to flag potential misuse in conversations, a technique we call self-assessment. Right after it responds, Claude gives a preliminary safety assessment of the conversation. 

Since we began using self-assessment in June, it has surfaced misuse that our other Show more
Scaling Misuse Detection with Self-Assessment
From safeguards.anthropic.com
1.4K
984
4.5K
2.1M
Anthropic
@AnthropicAI
Oct 29
We’ve expanded our AI for Science program beyond individual teams to support some of the world’s leading scientific foundations, institutions, and research groups.
AI for Science expands to foundations and institutions
From anthropic.com
379
395
3.2K
312K
Anthropic
@AnthropicAI
Oct 28
We're expanding our partnership with @USGSA. Under a new OneGov agreement, we are bringing Claude to federal, state, local, tribal, and territorial governments at 40% off.
Expanding our partnership with GSA to bring Claude to all levels of government
From anthropic.com
357
268
2.2K
504K
Anthropic
@AnthropicAI
Oct 28
Over the past few months, Anthropic scientists have engaged in deep research partnerships with six organizations developing new medicines. We've also begun drug discovery efforts of our own.

In doing so, we’ve learned much more about how Claude can support the many stages of Show more
Early progress on accelerating drug development with Claude
From anthropic.com
769
2K
11K
3.5M
Log in or sign up for X

See what’s happening and join the conversation

Continue with phone
Continue with Apple
Continue with Google
Continue with Google
or
Log in with username or email
Terms
·
Privacy
·
Cookies
·
Accessibility
·
Ads Info
·
More
© 2026 X Corp.
Scan to get the app"""

DOUYIN_URL = """https://www.douyin.com/search/%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93"""

DOUYIN_TITLE = """发现更多精彩视频 - 抖音搜索"""

DOUYIN_TEXT = """开启读屏标签
读屏标签已关闭
精选
推荐
关注
朋友
我的
小游戏
搜索

充值

客户端

壁纸

通知

消息

投稿

登录

综合
视频
用户
直播
多列
单列
筛选
登录后即可搜索更多精彩视频
扫码登录
如何扫码

打开「抖音APP」点击左上角

扫一扫

验证码登录
密码登录
获取验证码
登录
登录即代表同意用户协议和隐私政策"""

ZHIHU_URL = """https://www.zhihu.com/account/unhuman?type=S6E3V1&need_login=true&session=61a1ca7a5aa21e5c6180e32775a246c1"""

ZHIHU_TITLE = """安全验证 - 知乎"""

ZHIHU_TEXT = """进入知乎

系统监测到您的网络环境存在异常，为保证您的正常访问，请点击下方验证按钮进行验证。在您验证完成前，该提示将多次出现。

开始验证
登录知乎
·
意见反馈"""

BILIBILI_URL = """https://search.bilibili.com/zh-Hans/all?keyword=%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93"""

BILIBILI_TITLE = """量化交易-哔哩哔哩_bilibili"""

BILIBILI_TEXT = """下载客户端
登录
Switch language here after login !
更多
消息
动态
收藏
历史
创作中心
投稿
搜索
综合
番剧
0
用户
99+
16.6万
212
08:29
量化交易普通人为什么根本没机会
MatthewTL
· 5月2日
263
0
02:05:47
【量化交易合集】一口气看完15个量化策略和量化交易软件工具 | 恒生ptrade | 迅投qmt | 小市值策略 | 双均线策略 | 动量策略 | 巴菲特
量化研究员Andy
· 8月7日
1364
2
03:52
为什么不禁止量化？
丨王大沁
· 8月8日
1.6万
3
15:41
我把GPT-6 Astra变成全天候股票交易员，完整搭建教程 - Nate Herk | AI Automation TLQLfa7yH4I
黑纹白斑马
· 9月9日
1.3万
3
11:46
9月份全自动化量化策略实盘分享
做币圈量化的左右
· 10月3日
94.5万
1502
50:14:27
【量化交易教程】B站强推！目前最适合零基础入门的量化交易教程，整整108集，手把手教学，保姆级教程！让你不再走弯路！
B站Python官方资源
· 2025年11月14日
995
1
02:26:24
【量化交易】小白必看！量化交易教程从零基础到精通（全程干货）存下来吧！很难找全的
黑客小师妹
· 6月29日
93
0
00:58
量化交易的魅力
applematrix的log
· 10月23日
5797
1
16:37:51
【耶鲁大学】《量化金融》全42讲（完整版）：面向金融+AI方向的系统训练、MIT 量化交易/量化金融/金融数学/
AI课程研究院
· 10月16日
480
0
04:33
量化交易入门九问
国金量化工坊
· 9月28日
2.5万
5
05:11
收益和认可度最高的4只量化基金
晖哥的财务自由之路
· 3月30日
41.1万
108
03:26
股市四大女武神
华尔街之汪__
· 8月4日
18.3万
676
18:31
8年FX经验外汇量化交易员点评久留美第一集 外汇交易知识科普
FX_切嗣papa
· 10月7日
2040
0
13:38
Grok Bot 自动化交易代理构建：市场扫描与加密货币研究实操指南 | 市场扫描 / 投资组合追踪 / 加密货币研究
赛博门外憨
· 9月17日
4712
15
09:40
全网说的爆仓神器，我却跑了好几年，月化2%~5%
和AlgoLee一起交易
· 10月15日
309
0
01:50
DeepSeek HARNESS 它扫了全市场 422 只机会，最后只给我留了 11 只，明天开盘直接买
打开mosa说量化
· 10月16日
58.8万
4399
01:16:16
想提前退休？保证你一学就会还可照搬的投资方法|保姆级完整教学，基本一听就懂，且长期收益秒杀95%的大V | 想财务自由提前退休必看！
行长王德发
· 8月18日
5996
0
03:00:50
【中英】3小时入门Python量化交易-2023
量化Quantgirl
· 2023年9月4日
18.5万
155
29:19
第732期 天涯神贴：什么样的人适合炒股❓投资股票能赚大钱的只有三种人！
天涯神贴-最后的楼主
· 5月1日
2.3万
0
04:51
如何实现自动交易？
加密羊BTC
· 2024年7月1日
1.2万
204
39:37
【模型量化】一天学会大模型量化，从原理讲解、代码实现到微调实战，快速上手，超详细教程，过程可视化，让你完全搞懂模型量化
AI-智能体搭建教程
· 2025年10月9日
10.1万
29
05:03
DeepSeek Harness 一个多月：4200 块饭钱，长出一个大管家｜附复刻手册
剑箫
· 10月27日
2.5万
5
06:14
还在找币圈量化工具？最新“止盈”工具，5分钟看完你就懂
AkB圈量化青
· 6月20日
7972
34
06:12
量化入门书单，读完这6本等于入行3年！！
龙猫说财
· 5月13日
2.3万
4
02:01
00后杀进币圈！全自动量化直接躺平？
小天量化
· 2025年12月27日
2万
5
05:05
【干货】凯利公式——一个教我们每次买票买多少？的数学公式
跟着Jim学量化
· 6月18日
2.5万
23
03:22
盘点一周AI大事(10月25日)｜12G显存跑满血DeepSeek
产品君
· 10月25日
3.8万
94
59:22:38
MIT 量化交易/量化金融/金融数学/12周的课程几乎解决所有量化金融问题
吴老师讲人工智能
· 5月20日
14.2万
113
08:30
一口气轻松了解量化，量化是怎么赚钱的？
黑白夜谈
· 10月12日
1.8万
3
18:09
普通人如何从0开始做量化？（保姆级全流程）
QuantX西蒙斯
· 8月20日
115
0
01:15
AI量化能完全取代主观交易吗？
指南姐_量化编程
· 10月11日
1.3万
3
13:36
AI帮你零基础上手加密货币量化交易
Tiger-Web3
· 2025年3月8日
306
0
00:55
什么是量化交易？新手如何入门
小靓盈策本
· 10月9日
203
0
05:17
10万本金，1到9月回测近450%？ETF折价轮动，实盘先填这3个资金坑
上班做量化的鳄鱼
· 10月23日
844
0
04:51
大学老师使用量化交易一个月，赚钱了吗？
斜阳不知归
· 9月3日
431
0
05:39
游资交易心法：大学生 用量化打败量化 如何做成量化的交易模式
陌颜论市
· 7月26日
94
0
03:10
大学生用AI写量化交易策略，耗时一个月从0到1全过程
黄大圣叨叨叨录播
· 10月18日
447
0
08:15
什么是量化交易？一个视频给你讲清楚！
剑平聊投资
· 8月26日
343
0
01:03
【小牛经济学】什么是量化交易？
方正证券官方账号
· 10月20日
74
0
01:09
量化交易是什么？如何开始量化交易？
国金证券宜宾营业部
· 10月20日
59
0
02:43
主观交易VS量化交易
码上论投资
· 10月16日
1569
0
06:19
做交易15年，我为什么建议日内交易者，尽早了解Ai交易？
道诚交易
· 10月8日
上一页
1
2
3
4
5
6
7
...
22
下一页
bilibili
用户协议
隐私协议
Bilibili社区准则
侵权申诉"""

HN_ALGOLIA_URL = """https://hn.algolia.com/api/v1/search?query=cloakbrowser&tags=story"""

HN_ALGOLIA_TEXT = 'k<p>- docs.docker.com/engine/install \\u2014 187k \\u2192 0.9k<p>- en.wikipedia.org/wiki/LLM \\u2014 222.7k \\u2192 29.7k<p>Heads up: passes Cloudflare, can\'t solve &quot;click traffic lights&quot; captchas (reCAPTCHA v2, hCaptcha)<p>MIT. Happy to answer questions"},"title":{"matchLevel":"none","matchedWords":[],"value":"Show HN: Snitchmd \\u2'

EXAMPLE_URL = """https://example.com/"""

EXAMPLE_TITLE = """Example Domain"""

EXAMPLE_TEXT = """This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring purposes.

هذا النطاق مُخصص للاستخدام في أمثلة التوثيق دون الحاجة إلى إذن. هذه ليست خدمة، يُرجى تجنب الاعتماد عليها لأغراض الاختبار والمراقبة.

该域名仅用于文档示例，无需获得许可。这并非一项服务，请勿将其用于测试和监控目的。

L’usage de ce domaine est réservé à des exemples de documentation, sans autorisation préalable. Il ne s’agit pas d’un service ; son utilisation à des fins de test ou de surveillance est à éviter.

Данный домен предназначен для использования в примерах документации без необходимости получения предварительного разрешения. Это не сервис; не рекомендуется его использование для тестирования и мониторинга.

Este dominio está destinado al uso en ejemplos de documentación sin necesidad de permiso. Esto no es un servicio; evitar utilizarlo para realizar pruebas o monitoreos.

Learn more"""


def test_reddit_search_is_captcha():
    assert (
        classify_block(
            status=200,
            text=REDDIT_SEARCH_TEXT,
            final_url=REDDIT_SEARCH_URL,
            title=REDDIT_SEARCH_TITLE,
        )
        == "captcha"
    )


def test_old_reddit_is_login_wall():
    assert (
        classify_block(
            status=200,
            text=OLD_REDDIT_TEXT,
            final_url=OLD_REDDIT_URL,
            title=OLD_REDDIT_TITLE,
        )
        == "login_wall"
    )


def test_x_search_onboarding_is_login_wall():
    assert (
        classify_block(
            status=200,
            text=X_SEARCH_TEXT,
            final_url=X_SEARCH_URL,
            title=X_SEARCH_TITLE,
        )
        == "login_wall"
    )


def test_x_profile_is_not_blocked():
    assert (
        classify_block(
            status=200,
            text=X_PROFILE_TEXT,
            final_url=X_PROFILE_URL,
            title=X_PROFILE_TITLE,
        )
        == "none"
    )


def test_douyin_login_modal_is_login_wall():
    assert (
        classify_block(
            status=200,
            text=DOUYIN_TEXT,
            final_url=DOUYIN_URL,
            title=DOUYIN_TITLE,
        )
        == "login_wall"
    )


def test_zhihu_unhuman_403_is_captcha():
    assert (
        classify_block(
            status=403,
            text=ZHIHU_TEXT,
            final_url=ZHIHU_URL,
            title=ZHIHU_TITLE,
        )
        == "captcha"
    )


def test_bilibili_is_not_blocked():
    assert (
        classify_block(
            status=200,
            text=BILIBILI_TEXT,
            final_url=BILIBILI_URL,
            title=BILIBILI_TITLE,
        )
        == "none"
    )


def test_hn_algolia_json_mentioning_captcha_is_not_blocked():
    assert (
        classify_block(
            status=200,
            text=HN_ALGOLIA_TEXT,
            final_url=HN_ALGOLIA_URL,
            is_json=True,
        )
        == "none"
    )


def test_example_com_is_not_blocked():
    assert (
        classify_block(
            status=200,
            text=EXAMPLE_TEXT,
            final_url=EXAMPLE_URL,
            title=EXAMPLE_TITLE,
        )
        == "none"
    )


def test_empty_text_is_empty():
    assert classify_block(status=200, text="", final_url="https://example.com/empty") == "empty"


def test_short_404_page_is_http_error():
    assert (
        classify_block(
            status=404,
            text="Not Found",
            final_url="https://example.com/missing",
            title="404 Not Found",
        )
        == "http_error"
    )
