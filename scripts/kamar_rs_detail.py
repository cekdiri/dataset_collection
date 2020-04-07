import pandas as pd
import csv
import datetime
from pathlib import Path
from bs4 import BeautifulSoup as soup
from selenium import webdriver

if __name__ == '__main__':
    now = datetime.datetime.now()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    browser = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
    data_folder = Path("../data/")
    file_data = 'data_kamar_detail-' + now.strftime("%Y%m%d") + '-' + now.strftime("%H%M") + '.csv'
    filename = data_folder / file_data
    csvFile = open(filename, 'a')
    # Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(
        ['satker', 'nama', 'alamat', 'prov', 'ruang', 'kelas', 'total_kamar', 'terisi_lk', 'terisi_pr', 'total_terisi',
         'kosong_lk', 'kosong_pr', 'total_kosong', 'waiting_list', 'last_update', 'lat', 'lng'])
    faskes_df = pd.read_csv("../data/Faskes - Rumah Sakit.csv", delimiter=',', encoding='ISO-8859-1')
    global _temp_ruang
    for index, row in faskes_df.iterrows():
        print("Currently on row: {}; Currently iterrated {}% of rows".format(index,
                                                                             round((index + 1) / len(faskes_df.index) * 100)))
        satker = str(row['kode_rs'])
        nama_rs = str(row['nama_unit'])
        alamat = str(row['alamat'])
        prov = str(row['nama_prov'])
        lat = row['lat']
        long = row['lng']
        try:
            link = 'http://sirs.yankes.kemkes.go.id/integrasi/data/bed_monitor.php?satker=' + satker
            browser.get(link)
        except TimeoutError:
            browser.close()
            print('error timeout')
            break
        # print(r)
        data = browser.page_source
        url = soup(data, "lxml")

        table = url.find('table', attrs={'class': 'tbl-responsive table table-striped table-bordered'})
        # print(table)

        if table is not None:
            res = []
            table_rows = table.find_all('tr')

            num_rows = len(table_rows)
            # print(satker+'-'+nama_rs)

            i = 0
            for tr in table_rows:
                _satker = satker
                _nama = nama_rs
                _alamat = alamat
                _prov = prov
                _lat = lat
                _long = long
                _ruang = '-'
                _kelas = '-'
                _total_kamar = '-'
                _terisi_lk = '-'
                _terisi_pr = '-'
                _total_terisi = '-'
                _kosong_lk = '-'
                _kosong_pr = '-'
                _total_kosong = '-'
                _waiting_list = '-'
                _last_update = '-'

                if i > 1 and i < (num_rows - 1):

                    td = tr.find_all('td')
                    # print(td)
                    row = [tr.text.strip() for tr in td if tr.text.strip()]
                    # print(row)
                    # print(str(i)+'-'+str(len(row)))
                    if len(row) == 12:
                        _temp_ruang = row[1]

                    # print(_temp_ruang)
                    if row:

                        if len(row) == 12:
                            _ruang = row[1]
                            _kelas = row[2]
                            _total_kamar = row[3]
                            _terisi_lk = row[4]
                            _terisi_pr = row[5]
                            _total_terisi = row[6]
                            _kosong_lk = row[7]
                            _kosong_pr = row[8]
                            _total_kosong = row[9]
                            _waiting_list = row[10]
                            _last_update = row[11]

                        elif len(row) == 11:
                            _ruang = _temp_ruang
                            _kelas = row[1]
                            _total_kamar = row[2]
                            _terisi_lk = row[3]
                            _terisi_pr = row[4]
                            _total_terisi = row[5]
                            _kosong_lk = row[6]
                            _kosong_pr = row[7]
                            _total_kosong = row[8]
                            _waiting_list = row[9]
                            _last_update = row[10]
                        elif len(row) == 10:
                            _ruang = _temp_ruang
                            if row[0].isnumeric():
                                _kelas = '-'
                            else:
                                _kelas = row[0]
                            _total_kamar = row[1]
                            _terisi_lk = row[2]
                            _terisi_pr = row[3]
                            _total_terisi = row[4]
                            _kosong_lk = row[5]
                            _kosong_pr = row[6]
                            _total_kosong = row[7]
                            _waiting_list = row[8]
                            _last_update = row[9]
                        elif len(row) == 9:
                            _ruang = _temp_ruang
                            _kelas = '-'
                            _total_kamar = row[0]
                            _terisi_lk = row[1]
                            _terisi_pr = row[2]
                            _total_terisi = row[3]
                            _kosong_lk = row[4]
                            _kosong_pr = row[5]
                            _total_kosong = row[6]
                            _waiting_list = row[7]
                            _last_update = row[8]
                        # print(_waiting_list)

                    csvWriter.writerow(
                        [_satker, _nama, _alamat, _prov, _ruang, _kelas, _total_kamar, _terisi_lk, _terisi_pr,
                         _total_terisi, _kosong_lk, _kosong_pr, _total_kosong, _waiting_list, _last_update, _lat,
                         _long])
                i = i + 1
    csvFile.close()
    dataset = pd.read_csv(filename)
    print(dataset.shape)
