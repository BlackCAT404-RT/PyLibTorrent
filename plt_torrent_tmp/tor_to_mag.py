import hashlib
import urllib.parse
import glob
import os

try:
    import bencodepy
except ImportError:
    import subprocess
    subprocess.check_call([__import__("sys").executable, "-m", "pip", "install", "bencode.py", "-q"])
    import bencodepy

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "magnet_out.txt")
torrent_files = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.torrent"))

print(f"Найдено файлов: {len(torrent_files)}")

to_magnet = lambda path: (
    lambda data: (
        lambda info, info_hash, name, trackers:
            f"magnet:?xt=urn:btih:{info_hash}"
            f"&dn={urllib.parse.quote(name)}"
            + "".join(map(lambda t: f"&tr={urllib.parse.quote(t)}", trackers))
    )(
        data[b"info"],
        hashlib.sha1(bencodepy.encode(data[b"info"])).hexdigest(),
        data[b"info"].get(b"name", b"unknown").decode("utf-8", errors="replace"),
        list(dict.fromkeys(
            ([data[b"announce"].decode("utf-8", errors="replace")] if b"announce" in data else [])
            + sum(map(lambda tier: list(map(lambda t: t.decode("utf-8", errors="replace"), tier)),
                      data.get(b"announce-list", [])), [])
        ))
    )
)(bencodepy.decode(open(path, "rb").read()))

magnets = list(map(to_magnet, torrent_files))

print("\n".join(magnets))

open(OUTPUT_FILE, "w", encoding="utf-8").write("\n".join(magnets) + "\n")

print(f"\nСохранено в {OUTPUT_FILE} ({len(magnets)} шт.)")

delete_file = lambda path: (
    os.remove(path) or print(f"Удалён: {os.path.basename(path)}")
) if os.path.exists(path) else print(f"Не найден: {path}")

list(map(delete_file, torrent_files))