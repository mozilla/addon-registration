import hashlib


def get_file_hash(filename, block_size=2**20, algorithm=None):
    """Returns the hash of a file.

    :param filename:
        Complete path of the file you want to get the hash from.

    :param block_size:
        Size of the block to read when buffering the read.

    :param algorithm:
        Hash object ot use to do the hashing.

    """
    if algorithm is None:
        algorithm = hashlib.md5

    hash_ = algorithm()

    with open(filename, 'r') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hash_.update(data)
    return hash_.hexdigest()
