# pypcmringbuffer

## 概要

python用PCMリングバッファモジュールです。

## インストールの方法

```sh
pip install pypcmringbuffer
```

## 使い方

### リングキュークラス

```python
from pypcmringbuffer import PyPcmRingQueue

# 最大10要素をキューイングできるキューインスタンスを作成
queue = PyPcmRingQueue(10)
queue.enqueue([0,1,2,3])
print(len(queue)) # 4
pcm = queue.dequeue(3)
print(pcm) # [0, 1, 2]
print(len(queue)) # 1
```
