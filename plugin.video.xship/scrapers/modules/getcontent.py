
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))
