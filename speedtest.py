#!/usr/bin/env python3
import argparse
import http.client
import time
import urllib.request

REQUEST_COUNT = 10
CHUNK_SIZE = 1024 * 1024


def measure(url):
    total_bytes = 0
    total_time = 0.0

    for attempt in range(1, REQUEST_COUNT + 1):
        started = time.perf_counter()
        with urllib.request.urlopen(url, timeout=30) as response:
            downloaded = 0
            while chunk := response.read(CHUNK_SIZE):
                downloaded += len(chunk)
        elapsed = time.perf_counter() - started

        total_bytes += downloaded
        total_time += elapsed
        formatted_bytes = f"{downloaded:,}".replace(",", " ")
        print(
            f"Запрос {attempt}/{REQUEST_COUNT}: {elapsed:.3f} с, "
            f"{formatted_bytes} байт",
            flush=True,
        )

    average_time = total_time / REQUEST_COUNT
    speed_mbps = total_bytes * 8 / total_time / 1_000_000
    return average_time, total_bytes, speed_mbps


def main():
    parser = argparse.ArgumentParser(
        description="Измеряет скорость скачивания по 10 последовательным запросам."
    )
    parser.add_argument("url", help="адрес ресурса для скачивания")
    args = parser.parse_args()

    try:
        average_time, total_bytes, speed_mbps = measure(args.url)
    except (OSError, http.client.HTTPException, ValueError) as error:
        parser.exit(1, f"Ошибка при выполнении запроса: {error}\n")

    print(f"\nСреднее время запроса: {average_time:.3f} с")
    print(f"Всего скачано: {total_bytes / 1_000_000:.2f} МБ ({total_bytes:,} байт)".replace(",", " "))
    print(f"Скорость скачивания: {speed_mbps:.2f} Мбит/с")


if __name__ == "__main__":
    main()
