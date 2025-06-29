#!/usr/bin/env python3
import argparse
import threading

# Sobelove matrice
Gx = ((-1, 0, 1),
      (-2, 0, 2),
      (-1, 0, 1))
Gy = ((-1, -2, -1),
      (0, 0, 0),
      (1, 2, 1))

# Funkcija za učitavanje PGM slike (P5 format)
def parse_pgm(filename):
    with open(filename, 'rb') as f:
        assert f.readline().strip() == b'P5'  # Provjeri header
        line = f.readline()
        while line.startswith(b'#'):  # Preskoči komentare
            line = f.readline()
        width, height = map(int, line.strip().split())  # Dimenzije slike
        maxval = int(f.readline().strip())  # Maksimalna vrijednost piksela
        pixels = bytearray(f.read())  # Učitaj piksele
        assert len(pixels) == width * height  # Provjeri veličinu podataka
        return width, height, maxval,pixels

# Funkcija za spremanje PGM slike
def write_pgm(filename, width, height, maxval, pixels):
    with open(filename, 'wb') as f:
        f.write(b'P5\n')
        f.write(f'{width} {height}\n'.encode())  # Dimenzije
        f.write(f'{maxval}\n'.encode())  # Maksimalna vrijednost piksela
        f.write(pixels)  # Pikseli

# Funkcija za određivanje broja niti na temelju veličine slike
def calc_threads(width, height):
    total_size = width * height
    if total_size < 500 * 1024:
        return 1
    elif total_size < 1000 * 1024:
        return 2
    elif total_size < 4000 * 1024:
        return 4
    else:
        return 8

# Funkcija koja obrađuje dio slike pomoću Sobelovog filtra
def process_chunk(pixels, width, height, start_row, end_row, output):
    for y in range(max(1, start_row), min(height - 1, end_row)):
        for x in range(1, width - 1):
            sx = sy = 0
            for ky in range(3):
                for kx in range(3):
                    val = pixels[(y + ky - 1) * width + (x + kx - 1)]
                    sx += val * Gx[ky][kx]
                    sy += val * Gy[ky][kx]
            mag = int((sx * sx + sy * sy) ** 0.5)  # Izračun magnitude
            output[y * width + x] = mag if mag < 255 else 255  # Ograniči na 255

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', help='Putanja do ulazne .pgm slike')
    parser.add_argument('output_image', help='Putanja za spremanje izlazne .pgm slike')
    parser.add_argument('-t', '--threads', type=int, default=0,
                        help='Number of threads (0 = autodetect max cores)')
    args = parser.parse_args()

    # Učitaj sliku
    width, height, maxval, pixels = parse_pgm(args.input_image)
    output = bytearray(width * height)  # Rezultat

    # Odredi broj niti
    num_threads = args.threads if args.threads > 0 else calc_threads(width, height)
    print(f'Veličina slike: {width}x{height}, koristi {num_threads} nit{"i" if num_threads > 1 else ""}')

    # Podijeli među nitima
    rows_per_thread = (height + num_threads - 1) // num_threads
    threads = []
    for i in range(num_threads):
        start = i * rows_per_thread
        end = min((i + 1) * rows_per_thread, height)
        t = threading.Thread(target=process_chunk, args=(pixels, width, height, start, end, output))
        threads.append(t)
        t.start()

    # Čekaj da sve niti završe
    for t in threads:
        t.join()

    # Spremi
    write_pgm(args.output_image, width, height, maxval, output)

if __name__ == '__main__':
    main()
