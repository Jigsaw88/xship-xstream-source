
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))
