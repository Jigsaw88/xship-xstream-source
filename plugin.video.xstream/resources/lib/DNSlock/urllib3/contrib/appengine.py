
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))
