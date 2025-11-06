import os
import shutil
from PIL import Image

def create_image_grid(images, output_file):
    """Membuat grid dari beberapa gambar dan menyimpannya ke file output"""
    try:
        # Buka semua gambar
        img_list = []
        for img_path in images:
            try:
                img = Image.open(img_path)
                img_list.append(img)
                print(f"Berhasil memuat: {os.path.basename(img_path)}")
            except Exception as e:
                print(f"Gagal memuat {img_path}: {str(e)}")
        
        if not img_list:
            print("Tidak ada gambar yang dapat diproses.")
            return
        
        # Hitung ukuran grid (1 kolom, sejumlah baris sesuai jumlah gambar)
        max_width = max(img.width for img in img_list)
        total_height = sum(img.height for img in img_list)
        
        # Buat gambar baru dengan latar belakang putih
        result = Image.new('RGB', (max_width, total_height), 'white')
        
        # Tempelkan gambar-gambar ke dalam grid
        y_offset = 0
        for img in img_list:
            result.paste(img, (0, y_offset))
            y_offset += img.height
        
        # Simpan hasilnya
        result.save(output_file)
        print(f"\nGambar berhasil digabungkan dan disimpan ke: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")

def is_image_file(file_path):
    """Memeriksa apakah file adalah gambar"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']
    return os.path.splitext(file_path)[1].lower() in image_extensions

def merge_text_files(input_files, output_file):
    """Menggabungkan beberapa file teks menjadi satu"""
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filename in input_files:
                try:
                    with open(filename, 'r', encoding='utf-8') as infile:
                        outfile.write(f"\n\n=== Isi dari {os.path.basename(filename)} ===\n\n")
                        outfile.write(infile.read())
                    print(f"Berhasil menambahkan: {filename}")
                except FileNotFoundError:
                    print(f"File tidak ditemukan: {filename}")
                except Exception as e:
                    print(f"Terjadi kesalahan saat membaca {filename}: {str(e)}")
        
        print(f"\nFile teks berhasil digabungkan ke: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    print("=== Program Penggabung File ===")
    print("Program ini mendukung penggabungan file teks dan gambar.")
    
    # Input file yang akan digabungkan
    files_to_merge = []
    while True:
        file_path = input("\nMasukkan path file (kosongkan jika sudah selesai): ").strip('"')
        if not file_path:
            break
        if not os.path.exists(file_path):
            print(f"File tidak ditemukan: {file_path}")
            continue
        files_to_merge.append(file_path)
    
    if not files_to_merge:
        print("Tidak ada file yang dimasukkan.")
    else:
        # Cek apakah semua file adalah gambar
        all_images = all(is_image_file(f) for f in files_to_merge)
        
        if all_images:
            # Jika semua file adalah gambar, buat grid
            output_file = input("\nMasukkan nama file output untuk gambar gabungan (default: gabungan_gambar.jpg): ").strip()
            if not output_file:
                output_file = "gabungan_gambar.jpg"
            create_image_grid(files_to_merge, output_file)
        else:
            # Jika ada file non-gambar, gabungkan sebagai teks
            output_file = input("\nMasukkan nama file output (default: gabungan_teks.txt): ").strip()
            if not output_file:
                output_file = "gabungan_teks.txt"
            merge_text_files(files_to_merge, output_file)
