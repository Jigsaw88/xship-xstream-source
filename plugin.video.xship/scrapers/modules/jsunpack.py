
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))
