# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

import os
import errno
import uuid
from datetime import datetime


class Message(object):

    def __init__(self, nr, uid, path, size):
        self.nr = nr
        self.uid = uid
        self.path = path
        self.size = size
        self.deleted = False


class Store(object):

    def __init__(self, directory):
        self.directory = directory
        self.counter = 0
        self.messages = []

    def __len__(self):
        return len(self.non_deleted_messages)

    def __iter__(self):
        for m in self.non_deleted_messages:
            yield m

    @property
    def total_byte_size(self):
        return sum((m.size for m in self.non_deleted_messages))

    @property
    def non_deleted_messages(self):
        return [m for m in self.messages if not m.deleted]

    def load(self):
        self.messages = []
        self.counter = 0
        for filename in os.listdir(self.directory):
            if not filename.endswith('.eml'):
                continue
            uid = self.parse_uid(filename)
            path = os.path.join(self.directory, filename)
            size = os.stat(path).st_size
            self.counter += 1
            self.messages.append(Message(self.counter, uid, path, size))

    def get(self, nr, include_deleted=False):
        messages = self.messages
        if not include_deleted:
            messages = self.non_deleted_messages
        for m in messages:
            if m.nr == nr:
                return m
        return None

    def save(self, data):
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        uid = uuid.uuid4().hex
        filename = '%s-%s.eml' % (timestamp, uid)
        path = os.path.join(self.directory, filename)
        with open(path, 'wb+') as f:
            f.write(data)
        self.counter += 1
        stat = os.stat(path)
        m = Message(self.counter, uid, path, stat.st_size)
        self.messages.append(m)
        return m

    def parse_uid(self, filename):
        return b'-'.join(filename[0:-len('.eml')].split('-')[1:])

    def delete_marked_messages(self):
        for m in self.messages:
            if m.deleted:
                try:
                    os.unlink(m.path)
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise
                self.messages.remove(m)
        return True

