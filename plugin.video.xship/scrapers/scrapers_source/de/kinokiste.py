
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))