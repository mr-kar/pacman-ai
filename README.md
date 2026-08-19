# 👻 Pac-Man AI: Search Algorithms

Project permainan Pac-Man sederhana yang mengimplementasikan algoritma pencarian untuk mengontrol pergerakan Ghost secara otomatis.

Dalam project ini, Ghost menggunakan algoritma Artificial Intelligence untuk mencari dan mengejar posisi Pac-Man di dalam maze.

Saat ini terdapat dua algoritma pencarian yang telah diimplementasikan:

- 🟦 Breadth First Search (BFS)
- 🟩 Depth First Search (DFS)

Project dikembangkan menggunakan Python dan Pygame.

---

# 🎮 Demo Project

Ghost akan secara otomatis mencari jalur menuju Pac-Man menggunakan algoritma yang dipilih.

User tetap mengontrol Pac-Man secara manual menggunakan keyboard, sedangkan Ghost dikendalikan oleh algoritma pencarian.

```text
┌─────────────────────────────┐
│         PAC-MAN AI          │
│                             │
│  🟡 Pac-Man  ← User Control │
│                             │
│  👻 Ghost    ← AI Control   │
│                             │
└─────────────────────────────┘
```

---

# 🧠 Implementasi Artificial Intelligence

## 1. Breadth First Search (BFS)

BFS adalah algoritma pencarian yang menggunakan struktur data **Queue** dengan konsep:

```text
FIFO
First In First Out
```

BFS melakukan pencarian node berdasarkan level atau kedalaman.

Contoh sederhana:

```text
        👻
      /  |  \
     ●   ●   ●
    / \      / \
   ●   ●    ●   🟡
```

Pada maze dengan setiap jalur memiliki bobot yang sama, BFS dapat menemukan jalur terpendek dari Ghost menuju Pac-Man.

### Karakteristik BFS

- Menggunakan Queue
- Melakukan pencarian berdasarkan level
- Menjamin shortest path pada graph tanpa bobot
- Biasanya menghasilkan jalur yang lebih pendek

Contoh:

```text
👻 ────────────────→ 🟡

Path: 21 steps
```

---

## 2. Depth First Search (DFS)

DFS adalah algoritma pencarian yang menggunakan struktur data **Stack** dengan konsep:

```text
LIFO
Last In First Out
```

DFS akan menelusuri satu jalur sedalam mungkin sebelum kembali dan mencoba jalur lainnya.

Contoh:

```text
👻
│
●
│
● ─── ●
      │
      ●
      │
      🟡
```

DFS tidak menjamin jalur terpendek.

Karena itu Ghost dapat mengambil jalur yang lebih panjang atau memutar sebelum mencapai Pac-Man.

### Karakteristik DFS

- Menggunakan Stack
- Menelusuri node sedalam mungkin
- Tidak menjamin shortest path
- Dapat menghasilkan jalur yang lebih panjang

Contoh:

```text
👻 → ↓ → → ↑ → ↓ → → 🟡

Path: 73 steps
```

---

# ⚔️ Perbandingan BFS vs DFS

| Algoritma | Struktur Data | Strategi Pencarian         | Shortest Path   |
| --------- | ------------- | -------------------------- | --------------- |
| BFS       | Queue         | Berdasarkan level          | ✅ Ya           |
| DFS       | Stack         | Menelusuri sedalam mungkin | ❌ Tidak selalu |

Dalam project ini perbedaan kedua algoritma dapat dilihat secara langsung melalui pergerakan Ghost.

```text
BFS
👻 ───────────────→ 🟡


DFS
👻 → ↓ → → ↑ → ↓ → → 🟡
```

---

# 🎮 Controls

Pac-Man dikontrol langsung oleh user.

Gunakan:

```text
Arrow Keys
```

atau:

```text
W A S D
```

Untuk memilih algoritma AI:

| Tombol | Algoritma            |
| ------ | -------------------- |
| `B`    | Breadth First Search |
| `D`    | Depth First Search   |

Contoh:

```text
B → Ghost menggunakan BFS

D → Ghost menggunakan DFS
```

---

# 📊 Informasi di Layar

Saat program berjalan, informasi algoritma akan ditampilkan di bagian atas layar.

Contoh:

```text
Algorithm: DFS

Visited: 103

Path: 73 steps
```

Keterangan:

- **Algorithm**: Algoritma AI yang sedang digunakan.
- **Visited**: Jumlah node yang dikunjungi selama proses pencarian.
- **Path**: Panjang jalur dari Ghost menuju Pac-Man.

Nilai tersebut akan diperbarui ketika Ghost melakukan pencarian ulang terhadap posisi Pac-Man.

---

# 📁 Struktur Project

```text
pacman-ai/
│
├── main.py
├── README.md
│
├── ai/
│   ├── __init__.py
│   ├── bfs.py
│   └── dfs.py
│
├── game/
│   ├── __init__.py
│   ├── maze.py
│   ├── pacman.py
│   └── ghost.py
│
└── utils/
    ├── __init__.py
    └── config.py
```

---

# ⚙️ Requirements

Project ini menggunakan:

- Python 3
- Pygame

Install Pygame:

```bash
pip install pygame
```

---

# ▶️ Cara Menjalankan Project

Clone repository:

```bash
git clone https://github.com/USERNAME/pacman-ai-search-algorithms.git
```

Masuk ke folder project:

```bash
cd pacman-ai-search-algorithms
```

Install dependency:

```bash
pip install pygame
```

Jalankan program:

```bash
python main.py
```

---

# 🔄 Cara Kerja AI

Secara sederhana, sistem bekerja seperti berikut:

```text
              GAME DIMULAI
                    │
                    ▼
            User Menggerakkan
                Pac-Man
                    │
                    ▼
           Ghost Membaca Posisi
               Pac-Man
                    │
                    ▼
          ┌─────────────────────┐
          │ Pilih Algoritma AI  │
          └─────────────────────┘
                    │
           ┌────────┴────────┐
           ▼                 ▼
          BFS               DFS
           │                 │
           ▼                 ▼
       Cari Path         Cari Path
           │                 │
           └────────┬────────┘
                    ▼
             Ghost Mengikuti
                 Path
                    │
                    ▼
              Mengejar Pac-Man
```

---

# 🚀 Development Progress

| Step    | Fitur               | Status |
| ------- | ------------------- | ------ |
| Step 1  | Setup Project       | ✅     |
| Step 2  | Maze                | ✅     |
| Step 3  | Pac-Man Movement    | ✅     |
| Step 4  | Ghost Movement      | ✅     |
| Step 5  | Gameplay Stabil     | 🔒     |
| Step 6A | Project Structure   | 🔒     |
| Step 7  | BFS vs DFS          | 🔒     |
| Step 8  | Best First Search   | ⏳     |
| Step 9  | Visualisasi AI      | ⏳     |
| Step 10 | AI Enhancement      | ⏳     |
| Step 11 | Final Polish & Demo | ⏳     |

---

# 🧠 Future Development

Beberapa algoritma dan fitur yang direncanakan untuk ditambahkan:

- Best First Search
- Visualisasi proses pencarian
- Perbandingan performa algoritma
- Statistik waktu pencarian
- AI Mode Selection
- Peningkatan tampilan game
- Fitur tambahan

---

# 👨‍💻 Author

Developed using:

```text
Python + Pygame + Search Algorithms
```

---

# 📜 License

This project is created for educational and experimental purposes.
