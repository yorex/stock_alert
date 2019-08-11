#!/bin/bash
#coding=utf-8

# doc:  https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
# dingtalk.api:  http://open-dev.dingtalk.com/download/openSDK/python

curl 'https://oapi.dingtalk.com/robot/send?access_token=857278ccfaf791efa64ebc9d19dfac88702bf3eed7632a920132506dae107c4a' \
   -H 'Content-Type: application/json' \
   -d '{"msgtype": "text", 
        "text": {
             "content": "我就是我, 是不一样的烟火"
        }
      }'


#curl 'https://oapi.dingtalk.com/robot/send?access_token=857278ccfaf791efa64ebc9d19dfac88702bf3eed7632a920132506dae107c4a' \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "msgtype": "markdown",
#     "markdown": {
#         "title":"杭州天气",
#         "text": "#### 杭州天气 @156xxxx8827\n" +
#                 "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
#                 "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n"  +
#                 "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
#     }
# }'
#
