
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))