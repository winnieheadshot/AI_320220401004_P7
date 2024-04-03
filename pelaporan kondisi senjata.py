import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file Excel
df = pd.read_excel('KONDISI SENJATA.xlsx')

# Inisialisasi variabel linguistik
kualitas_senjata = ctrl.Antecedent(np.arange(0, 11, 1), 'kualitas_senjata')
jumlah_kerusakan = ctrl.Antecedent(np.arange(0, 11, 1), 'jumlah_kerusakan')
biaya_perbaikan = ctrl.Consequent(np.arange(0, 11, 1), 'biaya_perbaikan')

# Fungsi keanggotaan untuk masing-masing variabel linguistik
kualitas_senjata['buruk'] = fuzz.trimf(kualitas_senjata.universe, [0, 0, 5])
kualitas_senjata['sedang'] = fuzz.trimf(kualitas_senjata.universe, [0, 5, 10])
kualitas_senjata['baik'] = fuzz.trimf(kualitas_senjata.universe, [5, 10, 10])

jumlah_kerusakan['sedikit'] = fuzz.trimf(jumlah_kerusakan.universe, [0, 0, 5])
jumlah_kerusakan['sedang'] = fuzz.trimf(jumlah_kerusakan.universe, [0, 5, 10])
jumlah_kerusakan['banyak'] = fuzz.trimf(jumlah_kerusakan.universe, [5, 10, 10])

biaya_perbaikan['murah'] = fuzz.trimf(biaya_perbaikan.universe, [0, 0, 5])
biaya_perbaikan['sedang'] = fuzz.trimf(biaya_perbaikan.universe, [0, 5, 10])
biaya_perbaikan['mahal'] = fuzz.trimf(biaya_perbaikan.universe, [5, 10, 10])

# Aturan fuzzy
rule1 = ctrl.Rule(kualitas_senjata['buruk'] | jumlah_kerusakan['sedikit'], biaya_perbaikan['mahal'])
rule2 = ctrl.Rule(kualitas_senjata['sedang'] & jumlah_kerusakan['sedang'], biaya_perbaikan['sedang'])
rule3 = ctrl.Rule(kualitas_senjata['baik'] & jumlah_kerusakan['banyak'], biaya_perbaikan['murah'])

# Sistem kontrol fuzzy
biaya_perbaikan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
biaya_perbaikan_simulasi = ctrl.ControlSystemSimulation(biaya_perbaikan_ctrl)

# Proses inferensi
results = []
for index, row in df.iterrows():
    biaya_perbaikan_simulasi.input['kualitas_senjata'] = row['kualitas_senjata']
    biaya_perbaikan_simulasi.input['jumlah_kerusakan'] = row['jumlah_kerusakan']
    biaya_perbaikan_simulasi.compute()
    results.append(biaya_perbaikan_simulasi.output['biaya_perbaikan'])

# Menyimpan hasil ke dalam file Excel
df['biaya_perbaikan'] = results
df.to_excel('BIAYA PERBAIKAN KONDISI SENJATA.xlsx', index=False)
