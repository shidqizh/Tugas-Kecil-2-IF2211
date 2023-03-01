import time
import random
import math
import plotly
import plotly.graph_objs as go

def euclideancalc(x1, x2):
    ## menghitung jarak antara dua titik 3 dimensi
    return math.sqrt((x1[0]-x2[0])**2 + (x1[1]-x2[1])**2 + (x1[2]-x2[2])**2)

def bruteforce(points):
    ## pencarian dua titik terdekat dengan metode exhaustive
    n = len(points)
    count = 0
    if n <= 1:
        return None
    elif n == 2:
        return [points,count]
    else:
        jarak_min = euclideancalc(points[0], points[1])
        count+=1
        closest = [points[0], points[1]]
        for i in range(n):
            for j in range(i+1, n):
                jarak = euclideancalc(points[i], points[j])
                count +=1
                if jarak < jarak_min:
                    jarak_min = jarak
                    closest = [points[i], points[j]]
        return [closest,count]

def dnc_search(points):
    n = len(points)
    count = 0
    if n <= 3:
        return bruteforce(points)
    else:
        ## pengurutan point terlebih dahulu dari yang terkecil
        sorted_points = sorted(points, key=lambda p: p[0])
        ## pembagian array point menjadi dua bagian/metode divide
        mid = n//2
        kiri = sorted_points[:mid]
        kanan = sorted_points[mid:]
        [left_closest, c1] = dnc_search(kiri)
        count += c1
        [right_closest,c2] = dnc_search(kanan)
        count += c2
        if euclideancalc(left_closest[0], left_closest[1]) < euclideancalc(right_closest[0], right_closest[1]):
            closest = left_closest
            jarak_min = euclideancalc(left_closest[0], left_closest[1])
        else:
            closest = right_closest
            jarak_min = euclideancalc(right_closest[0], right_closest[1])
        count += 2
        tmp = []
        for point in sorted_points:
            if abs(point[0] - sorted_points[mid][0]) < jarak_min:
                tmp.append(point)
        for i in range(len(tmp)):
            j = i + 1
            while j < len(tmp) and tmp[j][1] - tmp[i][1] < jarak_min:
                jarak = euclideancalc(tmp[i], tmp[j])
                count += 1
                if jarak < jarak_min:
                    jarak_min = jarak
                    closest = [tmp[i], tmp[j]]
                j += 1
        return [closest,count]

n = int(input("Masukkan banyaknya titik (n > 1): "))
points = [(random.randrange(0, 200), random.randrange(0, 200), random.randrange(0, 200)) for i in range(n)]
print("Kamu memasukkan n = " + str(n))
print("\nBerikut adalah titik sembarang pada ruang:", points)
print("-----------------------------------------------------------------------------------------")
start = time.time()
[closest1, count] = bruteforce(points)
print("Kedua titik paling dekat adalah ", closest1, "yang memiliki jarak sebesar", "{:.2f}".format(euclideancalc(closest1[0], closest1[1])))
print("Banyaknya operasi perhitungan rumus Euclidean dengan algoritma brute force adalah " + str(count) + " kali.")
end = time.time()
print("Waktu eksekusi yang dibutuhkan dengan algoritma brute force adalah " + "{:.6f}".format((end-start)*1000) + " milisekon")

print("-----------------------------------------------------------------------------------------")

start1 = time.time()
[closest2, count] = dnc_search(points)
print("Kedua titik paling dekat adalah ", closest2, "yang memiliki jarak sebesar", "{:.2f}".format(euclideancalc(closest2[0], closest2[1])))
print("Banyaknya operasi perhitungan rumus Euclidean dengan algoritma divide and conquer adalah " + str(count) + " kali.")
end1 = time.time()
print("Waktu eksekusi yang dibutuhkan dengan algoritma divide and conquer adalah " + "{:.6f}".format((end1-start1)*1000) + " milisekon")

## visualisasi titik
plotly.offline.init_notebook_mode()
titik = go.Scatter3d(
    x=[points[i][0] for i in range(len(points))],
    y=[points[i][1] for i in range(len(points))],
    z=[points[i][2] for i in range(len(points))],
    mode='markers',
    name="Titik lainnya",
    marker={
        'size': 3,
        'opacity': 1,
    }
)
jaraktitikterdekat = go.Scatter3d(
    x=[closest2[i][0] for i in range(2)],
    y=[closest2[i][1] for i in range(2)],
    z=[closest2[i][2] for i in range(2)],
    mode='lines',
    line=dict(color='black'),
    name="Jarak antara dua titik terdekat",
    marker={
        'size': 7,
        'opacity': 1,
    }
)

titikterdekat = go.Scatter3d(
    x=[closest2[i][0] for i in range(2)],
    y=[closest2[i][1] for i in range(2)],
    z=[closest2[i][2] for i in range(2)],
    mode='markers',
    line=dict(color='black'),
    name="Dua titik terdekat",
    marker={
        'size': 5,
        'opacity': 1,
    }
)

layout = go.Layout(
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
)

data = [titik] + [titikterdekat] + [jaraktitikterdekat]

plot_figure = go.Figure(data=data, layout=layout)

plotly.offline.iplot(plot_figure)