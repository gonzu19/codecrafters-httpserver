import io
import gzip

def gzip_encode(data):
        """Compresses data using gzip and returns the gzipped bytes."""
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode='wb') as f:
            f.write(data)
        return out.getvalue()

output = "1f8b08008c643b6602ff4bcbcf07002165738c03000000"
foo = "foo"
foo = foo.encode("utf-8")

foo = gzip_encode(foo)
foo = foo.hex().rstrip()
print(foo)
print(output)
print(foo == output)

foo2 = "foo"
foo2 = gzip.compress(foo2.encode("utf-8"))
print(gzip.decompress(foo2))
foo2 = foo2.hex()

print(foo == foo2)
print(foo2 == output)
