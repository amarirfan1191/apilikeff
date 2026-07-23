import json
import requests

# === Guna data terus dari GitHub awak ===
UIDPASS_URL = "https://raw.githubusercontent.com/amarirfan1191/apilikeff/main/uidpass.json"

# Alamat API
API_URL = "https://jwt-steel-seven.vercel.app/token"

# === Baca data dari GitHub ===
def read_uidpass():
    try:
        res = requests.get(UIDPASS_URL, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ Ralat baca data akaun: {e}")
        return {}

# === Ambil token dari API ===
def fetch_token(uid, password):
    url = f"{API_URL}?uid={uid}&password={password}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        full_token = data.get("token")
        if full_token:
            full_token = full_token.replace("Bearer ", "")
            return full_token
        return None
    except Exception as e:
        print(f"⚠️ Ralat untuk UID {uid}: {str(e)}")
        return None

# === Simpan token ===
def update_token_file(token_list):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_list, f, ensure_ascii=False, indent=4)

# === Jalankan proses ===
def main():
    print("🔄 Membaca senarai akaun...")
    data_akaun = read_uidpass()
    
    if not data_akaun:
        print("❌ Tiada data dimuatkan.")
        return

    print(f"✅ Ditemui {len(data_akaun)} akaun.\n")
    senarai_token = []

    # Ikut format data awak: guna kunci "pass" dan gelung betul
    for nama, maklumat in data_akaun.items():
        uid = maklumat["uid"]
        kata_laluan = maklumat["pass"]  # <-- Kunci awak ialah "pass", bukan "password"
        print(f"Proses {nama} | UID: {uid}")
        token = fetch_token(uid, kata_laluan)
        if token:
            senarai_token.append({"uid": uid, "token": token})
            print("✅ Token berjaya didapati\n")
        else:
            print("❌ Gagal dapat token\n")

    if senarai_token:
        update_token_file(senarai_token)
        print(f"🎉 Selesai! {len(senarai_token)} token disimpan dalam tokens.json")
    else:
        print("⚠️ Tiada token berjaya dikumpul. Kemungkinan API masih bermasalah.")

if __name__ == "__main__":
    main()
