from flask import Flask, request, jsonify
from command import *
from tanggal import *
from database import *
import sqlite3
import json

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tasks.db")

app = Flask("__main__")

@app.route("/")
def my_index():
    return "Hello world!"

@app.route("/chat", methods=["POST"])
def chat_conditionals():
    # connect to db
    conn = create_connection(db_path)
    cursor = conn.cursor()

    # get message
    messages = request.get_json()["messages"]
    message = messages[len(messages)-1]

    # inisialisasi variabel awal
    tanggal = matkul = tugas = topik = id_num = n_hari = n_minggu = None

    # pencarian tanggal pada message
    if (temp := findTanggal(message)):
        tanggal = temp
    # pencarian matkul pada message
    if (temp := findMatkul(message)):
        matkul = temp
    # pencarian jenis tugas pada message
    if (temp := findTask(message)):
        tugas = temp
    # pencarian topik pada message
    if (temp := findTopik(message)):
        topik = temp
    # pencarian ID setelah 'task' pada message
    if (temp := findNumberAfterWord(message, "task")):
        id_num = temp
    # pencarian N sebelum 'hari' pada message
    if (temp := findNumberBeforeWord(message, "hari")):
        n_hari = temp
    # pencarian N sebelum 'minggu' pada message
    if (temp := findNumberBeforeWord(message, "minggu")):
        n_minggu = temp

    # test untuk POST tanggal, matkul, tugas dan topik
    if (tanggal and matkul and tugas and topik):
        insert_task = """INSERT INTO tasks (tanggal, matkul, tugas, topik)
                         VALUES (?, ?, ?, ?)"""
        cursor = conn.execute(insert_task, (tanggal[0], matkul[0].upper(), tugas, topik[0]))
        conn.commit()

        return f"[TASK BERHASIL DICATAT]\n(ID: {cursor.lastrowid}) {tanggal[0]} - {matkul[0].upper()} - {tugas} - {topik[0]}"
    
    # test untuk GET (harus ada kata deadline)
    elif (findWord(message, "deadline")):
        # test untuk GET all daftar deadlines
        if (findWord(message, "semua") or findWord(message, "sejauh")):
            # kasus terdapat filter task
            if (tugas):
                get_deadline = """SELECT * FROM tasks
                                  WHERE tugas = ?"""
                cursor = conn.execute(get_deadline, [tugas])
            else: # tidak ada filter tugas
                get_deadline = """SELECT * FROM tasks"""
                cursor = conn.execute(get_deadline)

        # test untuk GET daftar deadlines between 2 tanggal
        elif (tanggal and len(tanggal) == 2):
            # kasus terdapat filter task
            if (tugas):
                get_deadline = """SELECT * FROM tasks
                                  WHERE tugas = ? AND tanggal >= ? AND tanggal <= ?"""
                cursor = conn.execute(get_deadline, [tugas, tanggal[0], tanggal[1]])
            else: # tidak ada filter tugas
                get_deadline = """SELECT * FROM tasks
                                  WHERE tanggal >= ? AND tanggal <= ?"""
                cursor = conn.execute(get_deadline, [tanggal[0], tanggal[1]])

        # # test untuk GET daftar deadlines N hari/minggu dari sekarang
        # elif (findWord(message, "depan")):
        #     if (n_hari):
        #         # kasus terdapat filter task
        #         if (tugas):
        #             get_deadline = """SELECT strftime('%d/%m/%Y', tanggal) FROM tasks"""
        #             cursor = conn.execute(get_deadline)
        #             print(cursor.fetchall())
            #     else: # tidak ada filter tugas
            #         get_deadline = """SELECT * FROM tasks WHERE tanggal-strftime('%d-%m-%Y', 'now') <= ? AND tanggal >= date('now')"""
            #         cursor = conn.execute(get_deadline, [n_hari[0]])

            # elif (n_minggu):
            #     # kasus terdapat filter task
            #     if (tugas):
            #         get_deadline = """SELECT * FROM tasks
            #                         WHERE tugas = ? AND tanggal-strftime('%d-%m-%Y', 'now') <= ? AND tanggal >= date('now')"""
            #         cursor = conn.execute(get_deadline, [tugas, n_minggu[0]*7])
            #     else: # tidak ada filter tugas
            #         get_deadline = """SELECT * FROM tasks WHERE tanggal-strftime('%d-%m-%Y', 'now') <= ? AND tanggal >= date('now')"""
            #         cursor = conn.execute(get_deadline, [n_minggu[0]*7])

        # test untuk GET daftar deadlines hari ini
        elif (findWord(message, "hari ini")):
            # kasus terdapat filter task
            if (tugas):
                get_deadline = """SELECT * FROM tasks
                                  WHERE tugas = ? AND tanggal = strftime('%d/%m/%Y','now')"""
                cursor = conn.execute(get_deadline, [tugas])
            else: # tidak ada filter tugas
                get_deadline = """SELECT * FROM tasks WHERE tanggal = strftime('%d/%m/%Y','now')"""
                cursor = conn.execute(get_deadline)

        # test untuk GET daftar deadlines task tertentu
        elif (tugas):
            # kasus ada tugas
            get_deadline = """SELECT * FROM tasks
                              WHERE tugas = ?"""
            cursor = conn.execute(get_deadline, [tugas])

        results = cursor.fetchall()                
        retString = ""

        for i in range(len(results)):
            retString += f"\n{i+1}. (ID: {results[i][0]}) {results[i][1]} - {results[i][2]} - {results[i][3]} - {results[i][4]}"
    
        if (retString):
            return f"[Daftar Deadline]{retString}"

        # test untuk GET deadlines TUGAS matkul tertentu
        if (findWord(message, "tugas") and matkul):
            get_deadline = """SELECT tanggal FROM tasks
                              WHERE (tugas = "Tubes" OR tugas = "Tucil") 
                              AND matkul = ?"""
            cursor = conn.execute(get_deadline, [matkul[0]])

        results = cursor.fetchall()                
        retString = ""

        for i in range(len(results)):
            retString += f"{results[i][0]}"
            if (i < len(results)):
                retString += "\n"

        if (not(retString)):
            return "Tidak ada"
        else:
            return retString
    
    # test untuk UPDATE (harus ada ID, undur/maju, tanggal)
    elif (findWord(message, "undur") or findWord(message, "maju") or findWord(message, "update")):
        if (tanggal and id_num):
            count_query = """SELECT COUNT(*) FROM tasks
                             WHERE id = ?"""
            cursor = conn.execute(count_query, [id_num[0]])
            
            if (cursor.fetchall()[0][0] == 0):
                # apabila tidak ditemukan ID yang sesuai atau tanggal
                retString = f"Error: task tidak dikenali"
            else:
                # apabila ditemukan entry dengan ID sesuai
                retString =  f"Sukses memperbaharui task"

            update_tanggal = """UPDATE tasks
                                SET tanggal = ?
                                WHERE id = ?"""
            cursor = conn.execute(update_tanggal, [tanggal[0], id_num[0]])
            conn.commit()

            return retString

    # test untuk DELETE (harus ada selesai, ID)
    elif (findWord(message, "selesai") or findWord(message, "delete")):
        if (id_num):
            count_query = """SELECT COUNT(*) FROM tasks
                             WHERE id = ?"""
            cursor = conn.execute(count_query, [id_num[0]])
            
            if (cursor.fetchall()[0][0] == 0):
                # apabila tidak ditemukan ID yang sesuai atau tanggal
                retString =  f"Error: task tidak dikenali"
            else:
                # apabila ditemukan entry dengan ID sesuai
                retString =  f"Sukses menyelesaikan task"

            delete_entry = """DELETE FROM tasks
                              WHERE id = ?"""

            cursor = conn.execute(delete_entry, [id_num[0]])
            conn.commit()

            return retString

    # test untuk GET opsi helep
    elif (findWord(message, "apa") and (findWord(message, "lakukan") or findWord(message, "bisa"))):
        return f"[Fitur]\n1. Menambahkan task baru\n2. Melihat daftar task\n3. Menampilkan deadline tugas\n4. Memperbaharui task tertentu\n5. Menandai selesai suatu task\n6. Opsi help\n\n[Daftar kata penting]\n1. Kuis\n2. Ujian\n3. Tucil\n4. Tubes\n5. Praktikum"


    # close connection to db
    conn.close()

    return "Maaf, pesan tidak dikenali"

PORT = 5000
if __name__ == "__main__":
    app.run(host="localhost", port=PORT, debug=True)