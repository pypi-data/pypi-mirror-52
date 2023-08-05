# rb3, the rb fork support Python3.7

## Changes compared to [getsentry/rb](https://github.com/getsentry/rb)

**Not a compatibility upgrade.**

From this version, this fork of rb will only support Python3.7+ (Python3.5+ is tested but not recommend).

At the moment, we focus on how to make rb work under Python3.7 like it workd well on Python2.7.

Change in `crc32`:

- [Python 3 crc32 documentation clarifications](https://bugs.python.org/issue22341)
- [crc32 Python 3 doc](https://docs.python.org/3/library/binascii.html)
- [crc32 Python 2 doc](https://docs.python.org/2/library/binascii.html)

For now, we decide to support Python2-like `crc32` computing result by editing `rb/router.py`:

```python
class PartitionRouter(BaseRouter):
    """A straightforward router that just individually routes commands to
    single nodes based on a simple ``crc32 % node_count`` setup.

    This router requires that the hosts are gapless which means that
    the IDs for N hosts range from 0 to N-1.

    ``crc32`` returns different value in Python2 and Python3, for details
    check this link: https://bugs.python.org/issue22341.
    """

    def __init__(self, cluster):
        BaseRouter.__init__(self, cluster)
        assert_gapless_hosts(self.cluster.hosts)

    def get_host_for_key(self, key):
        k = six.ensure_binary(key)
        # Make sure return value same as in Python3
        # return (crc32(k) & 0xffffffff) % len(self.cluster.hosts)

        # Make sure return value same as in Python2
        crc_res = crc32(k)
        crc_res = (crc_res - ((crc_res & 0x80000000) <<1))
        return crc_res % len(self.cluster.hosts)
```

But may turn to use Python 3's native `crc32` function in the future.

## TODO

- [ ] option to choose `crc32`'s method
- [ ] fix macOS travis test
- [ ] fix pypy travis test
- [ ] validate functions

# rb's original README

![logo](https://github.com/getsentry/rb/blob/master/docs/_static/rb.png?raw=true)

rb - the redis blaster.

The fastest way to talk to many redis nodes.  Can do routing as well as
blindly blasting commands to many nodes.  How does it work?

For full documentation see [rb.rtfd.org](http://rb.rtfd.org/)

## Quickstart

Set up a cluster:

```python
from rb import Cluster

cluster = Cluster({
    0: {'port': 6379},
    1: {'port': 6380},
    2: {'port': 6381},
    3: {'port': 6382},
}, host_defaults={
    'host': '127.0.0.1',
})
```

Automatic routing:

```python
results = []
with cluster.map() as client:
    for key in range(100):
        client.get(key).then(lambda x: results.append(int(x or 0)))

print('Sum: %s' % sum(results))
```

Fanout:

```python
with cluster.fanout(hosts=[0, 1, 2, 3]) as client:
    infos = client.info()
```

Fanout to all:

```python
with cluster.fanout(hosts='all') as client:
    client.flushdb()
```
