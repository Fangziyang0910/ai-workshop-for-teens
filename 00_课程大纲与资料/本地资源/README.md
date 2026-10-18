# 本地教学资源

本目录保存课程固定版本的软件与官方说明。教师从[全程演练指引](../教师备课与全程演练.md)开始；学生只领取当课工程、任务卡和本组资料。

## 一、目录与使用对象

| 位置 | 内容 | 使用者与操作 |
|---|---|---|
| `下载文件/01_MindPlus/` | Mind+ V1.8.1 RC3.0 Windows安装包 | 教师统一安装到18台电脑；包含ML5本地模型、micro:bit通信固件与官方示例 |
| `下载文件/02_Dify/` | Dify 1.17.1源码ZIP、Tongyi 0.2.23官方签名插件 | 技术负责人部署服务器；教师从文件安装插件 |
| `下载文件/03_官方资料/` | 29份官方网页原件、便于本地阅读的副本及教程配图 | 教师查接口、步骤、硬件说明和竞赛规则；见[官方资料索引](官方资料索引.md) |
| `下载文件/04_服务器依赖/Docker_Ubuntu2404_amd64/` | Docker Engine、CLI、containerd、Buildx、Compose共5个DEB包 | 新建Ubuntu 24.04 x86-64服务器安装 |
| `下载文件/04_服务器依赖/Tongyi_Python312/` | Tongyi固定版本需要的62个wheel | 插件离线安装；仅供Linux x86-64、Python 3.12，不安装到学生电脑 |
| `下载文件/04_服务器依赖/dify-course-images.tar` | 课程Dify服务镜像包 | 在服务器执行`docker load`；使用方式见[服务器安装指引](服务器安装指引.md) |
| `下载文件/05_教师参考附件/` | micro:bit官方AI素养教学包、教育部2025—2028学年竞赛名单附件 | 教师参考；不要求学生阅读英文课程包 |
| [资源清单](资源清单.json) | 文件名、官方URL、版本对应路径、大小和SHA-256 | 校验本地文件与恢复下载 |
| [官方资料下载索引](官方资料下载索引.json) | 网页、配图与本地阅读路径的对应关系 | 资料检索与维护 |
| [准备服务器配置](准备服务器配置.py) | 为新实例生成私有`.env` | 不覆盖已有配置，不打印密钥 |
| [准备离线插件](准备离线插件.py) | 复制依赖并建立本地包索引 | 在安装Tongyi前执行 |
| [镜像清单](镜像清单.json)及[取回工具](取回服务器镜像.py) | 10个服务镜像的官方源摘要与平台信息 | 固定Linux x86-64镜像，恢复下载并导出 |
| [课程Compose配置](compose.course.yaml) | 关闭未使用服务、挂载本地依赖、限制调试端口 | 与官方Compose文件合并使用 |

Mind+安装包、Dify源码、插件、官方网页及依赖共134个可按URL取得的文件，约1.55GB，另有网页本地阅读副本和Docker镜像包。镜像包约6.79GB，完整本地资源合计约8.34GB。文件体积以清单中的字节数为准。镜像包单独复制到教师或技术负责人的移动硬盘，不分发给16个学生小组。

## 二、已随课程提供的教学文件

这些文件直接纳入Git管理，无需到外站下载：

| 材料 | 入口 |
|---|---|
| 三份Mind+起始工程及可读源文件 | [MindPlus工程](../配套材料/MindPlus工程/README.md) |
| 三个Dify Chatflow模板 | [配套材料](../配套材料/README.md) |
| 展品短资料、12条知识库资料、提示词 | [配套材料](../配套材料/README.md) |
| 视觉测试表、语言测试题、十课任务卡 | [任务卡](../学生任务卡与课后实践.md)及[测试材料](../配套材料/README.md) |
| 第一课课件、内嵌视频、打印材料、两版浏览器小游戏 | [第一课目录](../../01_AI侦探/README.md) |

视觉训练图片由教师和学生在自己的摄像头、物品及背景条件下采集。下载包不以网络图片或虚构测试数字代替本校的数据。教师演练完成后，将示范原图、模型JSON、工程MP和测试记录一起留存。

## 三、校验本地文件

Ubuntu或已有Python的教师电脑，在本目录执行：

```bash
python3 资源管理.py verify
```

Windows没有Python时，在本目录打开PowerShell，执行以下校验。它检查资源清单中的134个文件，不安装任何软件。

```powershell
$courseManifest = Get-Content -Raw -Encoding UTF8 .\资源清单.json | ConvertFrom-Json
$courseFailures = @()
foreach ($item in $courseManifest.files) {
    $file = Join-Path $PWD $item.path
    if (!(Test-Path -LiteralPath $file)) { $courseFailures += $item.path; continue }
    $actual = (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLower()
    if ($actual -ne $item.sha256) { $courseFailures += $item.path }
}
if ($courseFailures.Count) { $courseFailures; throw "有文件缺失或校验不符" }
"资源清单中的文件全部通过校验"
```

Python校验命令还会检查镜像包，共135项。Windows可用`Get-FileHash`核对镜像清单中`archive.sha256`。复制大文件前后均应校验，避免把未复制完成的文件发到学校。

## 四、从GitHub恢复资源

GitHub保存教案、工程、应用模板、资源URL、校验清单和管理工具。大型第三方安装包、网页缓存与镜像放在`下载文件`，不写入Git提交。这样可以比较和追溯课程配置，也避免将第三方软件及完整网页副本直接放入公开仓库。

在能访问下载源的教师准备机上运行：

```bash
python3 资源管理.py download --category core
python3 资源管理.py download --category server
python3 资源管理.py download --category docs
```

工具从清单的HTTPS地址下载，校验通过后才替换正式文件。校验不符会保留`.part`，不会把新内容冒充原版本。官方网页会更新，之后下载的网页可能与2026年10月18日留存版不同；此时先阅读原站，更新资料判断，再更新网页清单。

`download`恢复原始网页与配图，不重新生成“本地阅读.html”。课堂转移时复制整个本地资源目录即可保留阅读副本。软件、插件和依赖按固定版本取得，不随网页更新。

Docker镜像在已安装Docker的Linux x86-64准备机上取得：

```bash
python3 取回服务器镜像.py
```

官方源较慢时使用`python3 取回服务器镜像.py --mirror`。缓存来自[DaoCloud公共镜像服务](https://github.com/DaoCloud/public-image-mirror)，仍使用从官方源核对的SHA-256内容摘要，不按缓存中的浮动标签取包。工具不修改全局镜像源或其他运行服务。导出的tar字节顺序可能随Docker版本变化；重新导出时核对镜像内容摘要，并重新记录本地包文件校验值。

## 五、许可与使用范围

下载文件的权利属于原作者或厂商。Mind+、Dify、Tongyi插件、Docker组件、Python依赖和官方图文分别适用各自许可。保留源码包、插件包中的许可证和版权说明；Dify使用其项目许可证，不能把它笼统称为无附加条件的Apache-2.0软件。

本地缓存用于教师备课、校内安装和查阅。公开分享课程时分享课程自行编写的材料、下载入口与清单，不重新打包销售第三方软件，不删除原产品标识。第一课外部图片和视频的来源见对应课件备注；使用范围按原许可和学校教学安排处理。

本目录不包含服务器账号、域名证书私钥、SMTP密码、百炼API Key、教师平台备份及学生个人数据。它们由学校单独管理，不提交GitHub。
