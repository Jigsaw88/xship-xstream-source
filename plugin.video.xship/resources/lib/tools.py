
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))