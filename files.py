import os
import io
import re

from config import *

class Files():

    def _prepare_file_name(self, file):
        return file + ".waiting"

    def _append_file_name(self, file):
        return file + ".writing"

    def _is_file(self, file):
        return os.path.isfile(file)

    def _get_size(self, file):
        return os.path.getsize(file)

    def _remove_file(self, file):
        return os.remove(file)

    def _rename_file(self, ofile, nfile):
        return os.rename(ofile, nfile)

    def _path_exist(self, path):
        return os.path.exists(path)

    def _make_dir(self, dir):
        return os.makedirs(dir)

    def _files(self, type = 'list'):
        path = self.full_path()
        r = []

        if os.path.isdir(path):

            for f in os.listdir(path):

                file_path = self.full_path(f)

                if self._is_file(file_path):

                    if type == 'size':

                        r.append(self._get_size(file_path))

                    else:

                        r.append(f)

        return r

    def full_path(self, file=None):
        return os.path.join(PATH, file) if file != None else PATH

    def file_name_check(self, name):
        return re.findall(r'[^A-Za-z0-9_\-\\]',name)

    def file_write(self, file, data, type='wt', seek=None): #w-write, a-append, t-text, b-binary

        try:
            with io.open(self.full_path(file), type) as f:

                if not seek == None:
                    f.seek(int(seek))

                f.write(unicode(data))

            return True

        except IOError as e:

            return False

    def file_read(self, file, type='rt', rtype='read'): #r-read, t-text, b-binary

        with open(self.full_path(file), type) as f:

            return f.readlines() if rtype == 'lines' else f.read() #f.readline()

    def file_check(self, file, size = 1):
        file_path = self.full_path(file)

        if self._is_file(file_path):

            if self._get_size(file_path) >= int(size):

                return True

        return False

    def dir_check(self, path):

        if not self._path_exist(path):

            self._make_dir(path)

        return self._path_exist(path)

    def prepare_file(self, file, size):
        file = self._prepare_file_name(file)

        self.file_write(file, b"\0", 'wb', int(size)-1)

        return self.file_check(file, int(size))

    def append_file(self, file, data, seek):
        prepare_file = self._prepare_file_name(file)
        append_file = self._append_file_name(file)

        if self.file_check(prepare_file):

            self.rename_file(prepare_file, append_file)

        if not self.file_check(append_file):

            return 'FAIL'

        if not self.file_write(append_file, data, 'r+b', seek):

            return 'FAIL'

        if self.get_file_size(append_file) == len(data) + seek:

            self.rename_file(append_file, file)

            return 'DONE'

        return 'WAIT'

    def is_prepared_file(self, file, size):
        return self.file_check(self._prepare_file_name(file), size) or self.file_check(self._append_file_name(file), size)

    def get_files_list(self):
        return self._files('list')

    def get_file_size(self, file):
        file_path = self.full_path(file)
        return self._get_size(file_path)

    def rename_file(self, ofile, nfile):
        ofile = self.full_path(ofile)
        nfile = self.full_path(nfile)
        return self._rename_file(ofile, nfile)

    def get_files_size(self):
        return sum(self._files('size'))

    def remove_file(self, file):
        file_path = self.full_path(file)

        if self._is_file(file_path):

            self._remove_file(file_path)

            return True

        return False