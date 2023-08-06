import os
import time
import threading


__version__ = '0.1.0'

class SpongeBot:

    """ Who lives in a pineapple under the sea?

    SpongeBot spends his days soaking up files that are unlucky enough to end
    up in the folder specified in 'path'. Each time he encounters a new file,
    he calls the callback function, passing in the filepath as the first
    argument. Since SpongeBot gets bored quite quickly, he'll only ever soak up
    each file once, keeping track of the files he has already soaked up.

    Contrary to popular belief, SpongeBot is not a child but an adult
    (https://www.quora.com/Is-SpongeBob-an-adult-or-a-child). This means that
    once you set him off (by calling start), you do not have to pay any
    attention to him (he runs as a thread). You can also call him back anytime
    by calling stop, however this is optional.
    """

    def __init__(self,
                 path,
                 callback,
                 interval=2.0,
                 static_args=[],
                 static_kwargs=dict(),
                 snapshot_file='./.spongeBot_snapshot.txt'):
        if not callable(callback):
            raise TypeError('The callback is not a callable')
        self.callback = callback
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.interval = float(interval)
        self.static_kwargs = static_kwargs
        self.static_args = static_args
        self.snapshot_file = os.path.abspath(snapshot_file)

        # Load files from the snapshot file if it exists. Files in the
        # directory that are not in the snapshot file will be processed as soon
        # as start() is called.
        if os.path.exists(self.snapshot_file):
            with open(self.snapshot_file, 'r') as f:
                files = [os.path.basename(f.strip()) for f in f.readlines()]
            self.snapshot = set(files)
        else:
            # Otherwise create new snapshot. The files that are already in the
            # directory will be ignored.
            files = os.listdir(self.path)
            with open(self.snapshot_file, 'w') as f:
                f.write('\n'.join(files) + '\n')
            self.snapshot = set(files)
        self.running = False

    def start(self):
        """ Sends SpongeBot on his way to patrol the folder and soak up files.
        """
        self.isRunning = True
        self.thread = threading.Thread(target=self._loop)
        self.thread.start()

    def stop(self):
        """ Calls SpongeBot back.
        """
        self.isRunning = False

    def _loop(self):
        """ Starts monitoring a folder for new files. If one or multiple files
        are created, the callback function is called, with the path of the
        respective new file as the first argument and the unpacked args and
        kwargs.

        We use sets to check whether there have been changes in the directory.
        This means that we get much better scalability.
        """
        while self.isRunning:
            new_snapshot = set(os.listdir(self.path))
            new_files = new_snapshot.difference(self.snapshot)
            deleted_files = self.snapshot.difference(new_snapshot)
            if new_files:
                # Since self.path is an absolute path, each file in files will
                # also be an absolute path.
                # Call the callback function on each new file while updating
                # the snapshot file. Since we can just append to the file, this
                # is a fairly cheap opertion.
                with open(self.snapshot_file, 'a') as f:
                    for file in new_files:
                        self.callback(os.path.join(self.path, file),
                                      *self.static_args,
                                      **self.static_kwargs)
                        f.write(file + '\n')
            if deleted_files:
                # Remove the deleted files from the snapshot file. This
                # operation is linear in the number of total files in the
                # directory, so it should probably be avoided to delete files
                # frequently.
                temp_file = self.snapshot_file + '.temp'
                # We use a temp file to make the operation atomic.
                with open(self.snapshot_file, 'r') as old_f:
                    with open(temp_file, 'w') as new_f:
                        for line in old_f:
                            if line.strip() not in deleted_files:
                                new_f.write(line)
                # os.replace is an atomic operation.
                #See https://docs.python.org/3/library/os.html#os.replace
                os.replace(temp_file, self.snapshot_file)
            self.snapshot = new_snapshot
            time.sleep(self.interval)

    def __str__(self):
        return '<SpongeBot on %s in %s>' % (self.callback.__name__, self.path)