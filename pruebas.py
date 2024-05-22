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
foo = foo.hex()
print(foo)
print(output)
print(foo == output)
