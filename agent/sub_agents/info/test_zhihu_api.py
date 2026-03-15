# -*- coding: utf-8 -*-
"""
测试知乎热榜接口：与 zhihu_hot skill 使用相同请求方式，便于本地验证接口是否可用。
若本机出现 SSL 证书校验失败，本脚本会自动以不校验证书方式重试一次（仅本脚本内、本地调试用）。

用法（在仓库根目录，与 agent 平级）：
  python3 -m agent.sub_agents.info.test_zhihu_api
"""
from __future__ import annotations

import json
import os
import ssl
from urllib.request import Request, urlopen

# 与 skill 中一致
ZHIHU_HOT_API = "https://www.tianchenw.com/hot/zhihu/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def _fetch(use_ssl_verify: bool = True) -> str:
    req = Request(ZHIHU_HOT_API, headers={"User-Agent": USER_AGENT})
    ctx = None
    if not use_ssl_verify:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    with urlopen(req, timeout=15, context=ctx) as r:
        return r.read().decode()


def main() -> None:
    print("请求:", ZHIHU_HOT_API)
    print("User-Agent:", USER_AGENT[:50], "...")
    print()
    raw = None
    try:
        raw = _fetch(use_ssl_verify=True)
    except Exception as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e).upper():
            print("SSL 证书校验失败，正在以不校验证书方式重试（仅本脚本、本地调试用）...")
            try:
                raw = _fetch(use_ssl_verify=False)
            except Exception as e2:
                print("请求异常:", e2)
                return
        else:
            print("请求异常:", e)
            return
    if raw is None:
        return
    try:
        data = json.loads(raw)
        print("原始响应（前 500 字符）:", raw[:500])
        print()
        if data.get("code") == 200 and "data" in data:
            items = data["data"]
            print("解析成功: updateTime =", data.get("updateTime"), "条数 =", len(items))
            for i, item in enumerate(items[:5], 1):
                print(f"  {i}. {item.get('title', '')[:40]}... hot={item.get('hot')}")
        else:
            print("解析失败或非预期格式: code =", data.get("code"), "keys =", list(data.keys()))
    except json.JSONDecodeError as e:
        print("响应非 JSON:", e)


if __name__ == "__main__":
    main()
