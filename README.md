# barrage_bilibil
b站弹幕测试

## 使用
- 修改脚本 第7行的 av_code 为你所要发送的b站av号 
- 先手动发一次弹幕进行抓包:
    + 获取rnd值，修改脚本 第16行的 rnd
    + 获取csrf值，修改脚本 第20行的 csrf
    + 获取cookie，修改脚本 第27行的 cookie， 这里cookie用一个list下面**Mark**做解释

## 用途
- 该脚本可以用于发....发弹幕(看你怎么用啦。。我只是用来循环刷弹幕....) 

## Mark

- mark1: b站发弹幕cookie值, rnd值, csrf值是要对应的, csrf包含在cookie中（csrf是跨站请求伪造，应该是防范刷礼物之类用的）
- mark2: 当你每隔5s发一条弹幕（隔10+s和5s是一样的）达15条之后，b站需要你等待300s,可能是300s吧..
- mark3: 当出现mark2时， 你手动再去b站发一条弹幕，b站会给你重新分配一个cookie
- mark4: 新的cookie的包里的rnd是变了的，但却还能成功发弹幕， 神奇
- mark5: b站cookie时效大概一小时或者半小时

- *至于cookie作为list*: 由mark2可知, 我只要在达到15条弹幕之后，自己手动再去获取多一个cookie，那么后续使用就很方便了嘛

## Demo
**在参数设置好的前提下**

```python
if __name__ == '__main__':
    for play_time in range(0, 250):
        index = 0
        while -1 == send_barrage(
            message='Hello world {time}s'.format(time=play_time), 
            av_code=av_code, 
            play_time=str(play_time), 
            color='ff0000'):

            index = (index + 1) % len(cookie) # index为cookie池的游标，初始值为0
            headers['Cookie'] = cookie[index]

            time.sleep(5)

        time.sleep(5)
```


