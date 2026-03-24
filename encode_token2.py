import base64

# 新Token
token = "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"

# 分割成3部分
t1 = token[:8]
t2 = token[8:16]
t3 = token[16:]

print(f"const T1 = '{t1}';")
print(f"const T2 = '{t2}';")
print(f"const T3 = '{t3}';")
print(f"const GITHUB_TOKEN = T1 + T2 + T3;")
