from numpy.typing import NDArray
from numpy.typing import DTypeLike
import numpy

_QUEUE_INSTANCE_COUNT = 0


class PyPcmRingQueue:
    def __init__(self, queue_length: int, dtype: DTypeLike = type(numpy.float32), instance_label: str | None = None) -> None:
        global _QUEUE_INSTANCE_COUNT
        self.__buffer_length = queue_length
        # 常にデータを連続書き込み、連続読みだしするために、バッファを2倍の長さで用意する
        self.__queue = numpy.zeros(queue_length * 2, dtype=dtype)
        self.__head = 0  # キューの有効データの先頭位置でここからデータを取り出し始める
        self.__tail = 0  # キューの有効データの末尾位置でデータを追加する時はここからはじめる
        self.__label = instance_label if instance_label is not None else f'PyPcmRingQueue#{_QUEUE_INSTANCE_COUNT}'
        _QUEUE_INSTANCE_COUNT += 1
        # self.__tail - self.__headはキューの有効データの長さを表す
        return None

    def __len__(self):
        # head <= tail は常に成り立つ
        return self.__tail - self.__head

    def remaining_capacity(self):
        return self.__buffer_length - len(self)

    def enqueue(self, pcm: NDArray[numpy.float32 | numpy.float64 | numpy.int16 | numpy.int32] | list[float | int]) -> None:
        # 空き領域が不十分なら例外を出す
        if len(self.__queue) < self.__tail + len(pcm):
            raise Exception("Queue is full")
        # 高速化のためにブロードキャストを使う
        updated_tail = self.__tail + len(pcm)
        self.__queue[self.__tail:updated_tail] = pcm
        self.__tail = updated_tail
        return None

    def dequeue(self, size: int) -> numpy.ndarray:
        if size < 0:
            raise Exception("size must be positive")
        # データが無いなら例外を出す
        if len(self) < size:
            raise Exception("Queue is empty")
        # 余計なコピーを避けてスライスでデータを返す
        # バッファ長を2倍で用意しているので取り出すデータは常に連続配置になっている
        # ただし、headは常に0以上なので、headを基準にスライスする
        # 取り出すデータの長さはsizeで、headからsize分だけスライスする
        data = self.__queue[self.__head:self.__head + size]
        return data

    def discard(self, size: int) -> int:
        # 実際に捨てた要素数を返す
        # headをsize分だけ進めることでデータを捨てる
        if size < 0:
            raise Exception("size must be positive")
        if len(self) <= size:
            # 取り出すデータがキューの長さより大きい場合は、キューの長さを返す
            size = len(self)
            self.discard_all()
            return size
        self.__head += size
        # headがqueue_lengthを超えたらheadとtailをバッファの1ブロック目に戻す
        if self.__buffer_length <= self.__head:
            rewinded_head = self.__head - self.__buffer_length
            rewinded_tail = self.__tail - self.__buffer_length
            # コピー先がコピー元の範囲と重なっている場合は、スライスを使うとバッファが壊れるので、スライスを使わずにコピーする
            self.__queue[rewinded_head:rewinded_tail] = self.__queue[self.__head:self.__tail].copy()
            self.__head = rewinded_head
            self.__tail = rewinded_tail
        return size

    def discard_all(self) -> None:
        self.__head = 0
        self.__tail = 0
        return None
