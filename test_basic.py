import pytest

from pypcmringbuffer import PyPcmRingQueue


def test_init():
    queue_length = 10
    queue = PyPcmRingQueue(queue_length)
    assert queue is not None
    assert len(queue) == 0  # 初期状態ではキューは空であることを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    queue.enqueue([0, 1, 2, 3, 4])
    assert len(queue) == 5  # データを追加した後のキューの長さを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    queue.enqueue([5, 6, 7, 8, 9])
    assert len(queue) == 10  # データを追加した後のキューの長さを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    pcm = queue.dequeue(3)
    assert len(pcm) == 3  # データを取り出した後のキューの長さを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    assert pcm[0] == 0  # 取り出したデータの内容を確認する
    assert pcm[1] == 1
    assert pcm[2] == 2  # 取り出したデータの内容を確認する
    assert len(queue) == 7  # データを取り出した後のキューの長さを確認する
    pcm = queue.dequeue(3)
    assert len(queue) == 4  # データを取り出した後のキューの長さを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    assert pcm[0] == 3  # 取り出したデータの内容を確認する
    assert pcm[1] == 4
    assert pcm[2] == 5  # 取り出したデータの内容を確認する
    queue.enqueue([10, 11, 12, 13, 14, 15])
    assert len(queue) == 10  # データを追加した後のキューの長さを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    pcm = queue.dequeue(10)
    assert len(queue) == 0  # データを取り出した後のキューの長さを確認する
    assert queue.remaining_capacity() == queue_length - len(queue)  # データ数操作後のキューの空き容量を確認する
    # 取り出したデータの内容を確認する
    assert pcm[0] == 6
    assert pcm[1] == 7
    assert pcm[2] == 8
    assert pcm[3] == 9
    assert pcm[4] == 10
    assert pcm[5] == 11
    assert pcm[6] == 12
    assert pcm[7] == 13
    assert pcm[8] == 14
    assert pcm[9] == 15
