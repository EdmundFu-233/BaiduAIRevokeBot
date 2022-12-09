# BaiduAIRevokeBot
使用百度AI文本审核功能防炸群
# 如何安装

将主程序复制到'plugins'文件夹下并简单填入你的APIKEY等信息即可

#Q&A

Q:有没有百度AI审核平台的链接

A:https://ai.baidu.com/tech/textcensoring

Q:如何修改撤回策略

A:进入百度AI审核平台的控制台，选择内容审核，按照上方的操作指引一步步完成即可

Q:AI一直在撤回/不撤回怎么办

A:建议在策略编辑内拉低或拉高违规值，本程序只会撤回认定为违规的发言

Q:撤回后的Base64解码后是乱码怎么回事

A:机器人生成的Base64里的b'XXXXXXXX' 其中X才是他说的话