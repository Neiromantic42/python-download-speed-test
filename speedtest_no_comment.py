#!/usr/bin/env python3
import argparse
import sys
import time
import urllib.request
from urllib.error import HTTPError, URLError

REQUESTS_COUNT = 10
CHUNK_SIZE = 64 * 1024
TIMEOUT_SECONDS = 30


def download_once(url):
    request = urllib.request.Request(url, headers={"User-Agent": "speedtest-script/1.0"})
    total_bytes = 0
    start = time.perf_counter()

    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            total_bytes += len(chunk)

    elapsed = time.perf_counter() - start
    return total_bytes, elapsed


def main():
    parser = argparse.ArgumentParser(description="Замер скорости скачивания по URL")
    parser.add_argument("url", help="адрес файла, например тяжёлой картинки")
    args = parser.parse_args()

    durations = []
    total_bytes = 0

    print(f"Адрес: {args.url}")
    print(f"Делаем {REQUESTS_COUNT} запросов последовательно...\n")

    for i in range(1, REQUESTS_COUNT + 1):
        try:
            size, elapsed = download_once(args.url)
        except HTTPError as e:
            print(f"Ошибка HTTP {e.code} на запросе №{i}", file=sys.stderr)
            sys.exit(1)
        except (URLError, TimeoutError) as e:
            print(f"Ошибка сети на запросе №{i}: {e}", file=sys.stderr)
            sys.exit(1)

        durations.append(elapsed)
        total_bytes += size
        print(f"Запрос {i:>2}: {size / 1_000_000:.2f} МБ за {elapsed:.3f} с")

    total_time = sum(durations)
    avg_time = total_time / REQUESTS_COUNT
    speed_mbit = (total_bytes * 8) / total_time / 1_000_000
    speed_mbyte = total_bytes / total_time / 1_000_000

    print("\n--- Результаты ---")
    print(f"Среднее время запроса:  {avg_time:.3f} с")
    print(f"Всего скачано:          {total_bytes / 1_000_000:.2f} МБ")
    print(f"Скорость скачивания:    {speed_mbit:.2f} Мбит/с ({speed_mbyte:.2f} МБ/с)")


if __name__ == "__main__":
    main()