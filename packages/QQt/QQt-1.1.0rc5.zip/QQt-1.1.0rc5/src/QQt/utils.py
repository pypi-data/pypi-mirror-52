# Copyright (c) 2012-2019 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib/

from .__config__ import origin

__all__ = ('StreamEmitter',)

origin = __import__(origin, globals(), locals(), ["QtCore"], 0)


class StreamEmitter(origin.QtCore.QObject):

    message = origin.QtCore.Signal(object)

    def write(self, data):
        self.message.emit(data)

    def flush(self):
        pass
