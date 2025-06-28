#!/usr/bin/env python3
import argparse
import threading
from multiprocessing import cpu_count       # samo za autodetekciju broja jezgri
from PIL import Image                       # samo za ucitavanje slike

# Sobel matrice
Gx = ((-1, 0, 1),
      (-2, 0, 2),
      (-1, 0, 1))
Gy = ((-1, -2, -1),
      ( 0,  0,  0),
      ( 1,  2,  1))

# sobel filter u cistom Pythonu
def process_chunk(pixels, width, height, start_row, end_row, output):
    for y in range(max(1, start_row), min(end_row, height - 1)):
        for x in range(1, width - 1):
            sx = sy = 0
            for ky in range(3):
                for kx in range(3):
                    val = pixels[(y + ky - 1) * width + (x + kx - 1)]
                    sx += val * Gx[ky][kx]
                    sy += val * Gy[ky][kx]
            mag = int((sx * sx + sy * sy) ** 0.5)
            output[y * width + x] = min(255, mag)

def main():
    parser = argparse.ArgumentParser(description='Pure Python parallel Sobel filter')
    parser.add_argument('input_image', help='Input image path (JPEG, PGM, etc.)')
    parser.add_argument('output_image', help='Output image path (JPEG, PGM, etc.)')
    parser.add_argument('-t', '--threads', type=int, default=0,
                        help='Number of threads (0 = autodetect max cores)')
    args = parser.parse_args()

    img = Image.open(args.input_image).convert('L')
    width, height = img.size
    pixels = bytearray(img.tobytes())

    output = bytearray(width * height)

    num_threads = args.threads if args.threads > 0 else cpu_count()
    print(f'Using {num_threads} thread{"s" if num_threads > 1 else ""}')

    rows_per_thread = (height + num_threads - 1) // num_threads
    threads = []
    for i in range(num_threads):
        start_row = i * rows_per_thread
        end_row = min((i + 1) * rows_per_thread, height)
        t = threading.Thread(target=process_chunk,
                             args=(pixels, width, height, start_row, end_row, output))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    out_img = Image.frombytes('L', (width, height), bytes(output))
    out_img.save(args.output_image)

if __name__ == '__main__':
    main()
