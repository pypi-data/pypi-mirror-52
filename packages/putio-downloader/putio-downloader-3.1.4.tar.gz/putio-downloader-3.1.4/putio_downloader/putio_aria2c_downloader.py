"""Put.io Aria2c Downloader."""
import binascii
import logging
import os
import shutil
import tempfile
import time
import xmlrpc.client

import putiopy


class PutioAria2cDownloader():
    """Put.io Aria2c downloader."""

    def __init__(self, **kwargs):
        """Put.io Aria2c downloader.

        Attributes:
            keep_folder_structure (bool): keep the same structure as on put.io
            aria2c_secret_token (str): aria2c rpc secret token
            incomplete_dir (int): put.io folder to start recursing from
            complete_dir (str): Where to move completed downloads
            watch_list (dict): folders to watch in incomplete_dir on put.io
            putio_client: putio.py library client object
            aria_client: aria2c xmlrpc client object

        """
        self.logger = logging.getLogger('putio.' + __name__)
        self.initialize(kwargs)

    def init_app(self, app):
        """Initialize app from Flask configuration."""
        config = dict(app.config)
        config = {key.lower(): value for key, value in config.items()}
        self.initialize(config)

    def initialize(self, config):
        """Set up objects from configuration."""
        self.keep_folder_structure = config.get('keep_folder_structure', True)
        aria2c_secret_token = config.get("aria2c_secret_token")
        self.aria2c_secret_token = f'token:{aria2c_secret_token}'
        self.incomplete_dir = config.get('incomplete_dir', tempfile.mkdtemp())
        self.complete_dir = config.get('complete_dir', os.getcwd())
        self.watch_list = config.get('watch_folders', [])

        self.putio_client = putiopy.Client(
            config.get('oauth_token'),
            use_retry=True,
            timeout=10
        )
        self.aria_client = xmlrpc.client.ServerProxy(
            config.get('rpc_url', 'https://localhost:6800/rpc'))

    def download_file(self, file_id: int, folder_id: int):
        """Download a file or folder from put.io.

        Intended to be used in conjunction with a webhook listener

        Args:
            file_id (int): Id of the file on put.io
            folder_id (int): id of the containing folder on put.io

        """
        self.logger.info('Downloading %s from %s', file_id, folder_id)
        folder = self.putio_client.File.get(folder_id)
        _file = self.putio_client.File.get(file_id)
        path = os.path.join(folder.name, _file.name)
        self.logger.info('Downloading to %s', path)
        self.download_all_in_folder(_file, path=path)

    def download_all_in_watchlist(
            self, root_watch_dir: int = 0, clear_results: bool = False):
        """Search for files to download in all watched folders.

        Args:
            root_watch_dir: put.io folder id to look in for watched folders
            clear_results: should we remove all download results from aria2c?

        """
        self.logger.info('Searching for files to download from put.io')
        files = self.putio_client.File.list(parent_id=root_watch_dir)
        for folder in files:
            if (
                    folder.content_type == 'application/x-directory' and
                    folder.name in self.watch_list
            ):
                self.download_all_in_folder(folder, path=folder.name)
            else:
                self.logger.info('Folder %s not in watchlist', folder.name)
        self.putio_client.close()
        if clear_results:
            self.aria_client.aria2.purgeDownloadResult(
                self.aria2c_secret_token)

    def download_all_in_folder(self, folder, path: str = '',):
        """Download all in folder.

        Args:
            folder (putiopy.File): folder on put.io to download from
            path: path to the folder

        """
        self.logger.info('Downloading everything in %s', folder.name)
        files = self.putio_client.File.list(folder.id)
        for _file in files:
            if _file.content_type == 'application/x-directory':
                self.process_folder(_file, path)
            else:
                self.process_file(_file, path)
        if not files:
            self.logger.info('No files to download in %s', folder.name)

    def process_folder(self, folder, path: str):
        """Process Folder.

        Args:
            folder (putiopy.Client.File): put.io file object
            path (str): path where folder lives

        Raises:
            OSError: if the directory can't be created in complete_dir

        """
        folderpath = os.path.join(path, folder.name)
        dest_dir = os.path.join(self.complete_dir, folderpath)
        try:
            self.logger.info(folderpath)
            self.logger.info('Making directory %s', folderpath)
            os.makedirs(dest_dir)
        except FileNotFoundError:
            raise OSError('Couldn\'t create directory')
        except FileExistsError:
            self.logger.info('Folder %s already exists', dest_dir)
        self.download_all_in_folder(folder, folderpath)
        self.logger.info('Files from %s sent to aria2c', folderpath)
        self.cleanup_empty_folders(folder)

    def process_file(self, _file, path: str,):
        """Process Folder.

        Args:
            _file (putiopy.Client.File): put.io file object
            path (str): path where folder lives

        """
        directory = os.path.join(self.incomplete_dir, path)
        completed = self.add_uri(
            _file.get_download_link(), directory=directory)
        if completed:
            self.logger.info(
                'File %s downloaded successfully by aria', _file.name)
            _file.delete(True)
            download_path = os.path.join(directory, _file.name)
            destination_path = os.path.join(
                self.complete_dir, path, _file.name)
            shutil.move(download_path, destination_path)
            try:
                os.rmdir(directory)
            except FileNotFoundError:
                self.logger.info(
                    'Tried to rm %s but it wasn\'t empty', directory)
        else:
            self.logger.info(
                'aria2c didn\'t download %s successfully', _file.name)

    def cleanup_empty_folders(self, folder):
        """Cleanup empty folders.

        Args:
            folder (putiopy.File): folder to cleanup

        """
        self.logger.info('Cleaning up...')
        files = self.putio_client.File.list(folder.id)
        if not files:
            if folder.name not in self.watch_list:
                folder.delete(True)
                self.logger.info('Deleted %s from put.io', folder.name)

    def add_uri(self, uri: str, directory: str) -> bool:
        """Add URI to aria2c.

        Args:
            uri: URI to add to aria2c
            directory: directory to place the download

        Returns:
            status: whether URI was added and completed successfully

        """
        if not self.keep_folder_structure:
            directory = self.incomplete_dir
        self.logger.info('Adding URI %s to %s', uri, directory)

        opts = {
            'dir': directory,
            'file-allocation': 'falloc',
            'always-resume': 'true',
            'max-connection-per-server': '4',
            'check-integrity': 'true'
        }
        gid = self.aria_client.aria2.addUri(
            self.aria2c_secret_token, [uri], opts)
        loop = True
        while loop:
            time.sleep(2)
            status = self.aria_client.aria2.tellStatus(
                self.aria2c_secret_token,
                gid,
                ['gid', 'status', 'errorCode', 'errorMessage']
            )
            self.logger.debug(status)
            if status['status'] == 'complete':
                loop = False
                return True
            if status['status'] == 'error':
                loop = False
            if status['status'] == 'removed':
                loop = False
        return False

    @staticmethod
    def crc(filename: str) -> str:
        """Check CRC32 value.

        Args:
            filename: Name of file for which to calculate crc32

        Returns:
            value: crc32 value

        """
        buf = open(filename, 'rb').read()
        buf32 = (binascii.crc32(buf) & 0xFFFFFFFF)
        return '%08X' % buf32
