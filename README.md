# นับเวลาจอดรถ + แจ้งเตือน LINE อัตโนมัติ (ไม่ต้องเปิดแท็บทิ้งไว้)

หน้าเว็บ (`index.html`) ให้คุณสแกน/กรอกเวลาเข้าจอด แล้วกด "เริ่มนับเวลา" — เวลาเป้าหมาย (เข้า + 3 ชม.)
จะถูกเขียนลงไฟล์ `data/state.json` ใน repo นี้ผ่าน GitHub API

จากนั้น GitHub Actions (`.github/workflows/check-parking.yml`) จะรันทุก ~5 นาที (ฟรี บน GitHub)
คอยเช็คไฟล์นี้ ถ้าถึงเวลาแล้วและยังไม่เคยแจ้ง จะยิงข้อความ LINE ให้อัตโนมัติ — **แม้คุณจะปิดแท็บ ปิดมือถือไปแล้วก็ตาม**

## ตั้งค่าครั้งแรก (ทำครั้งเดียว)

### 1. สร้าง repo และอัปโหลดไฟล์
สร้าง repo ใหม่บน GitHub (public หรือ private ก็ได้) แล้วอัปโหลดไฟล์ทั้งหมดในโฟลเดอร์นี้ให้ตรงตามโครงสร้าง:
```
index.html
check_and_notify.py
data/state.json
.github/workflows/check-parking.yml
```
(อัปโหลดผ่านหน้าเว็บ GitHub ได้เลย — ตอน "Create new file" พิมพ์ path เต็ม เช่น `.github/workflows/check-parking.yml`
ระบบจะสร้างโฟลเดอร์ให้อัตโนมัติ)

### 2. เปิด GitHub Pages
Settings → Pages → Branch เลือก `main` → Save
จะได้ลิงก์ เช่น `https://ยูสเซอร์เนม.github.io/ชื่อ-repo/`

### 3. เพิ่ม Secrets สำหรับ LINE (ให้ GitHub Actions ใช้ยิงข้อความ)
Settings → Secrets and variables → Actions → New repository secret
- `LINE_CHANNEL_TOKEN` = Channel Access Token จาก LINE Official Account (Messaging API)
- `LINE_USER_ID` = User ID ของคุณที่จะรับข้อความ

### 4. สร้าง Personal Access Token ให้หน้าเว็บเขียนไฟล์ได้
GitHub → Settings (โปรไฟล์) → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token
- Repository access: เลือกเฉพาะ repo นี้
- Permissions: **Contents → Read and write**
- คัดลอก token (ขึ้นต้นด้วย `github_pat_...`)

### 5. ตั้งค่าในหน้าเว็บ
เปิดลิงก์ GitHub Pages ของคุณ → เปิดการ์ด "เชื่อมต่อ GitHub" → กรอก username, ชื่อ repo, branch (`main`), และ token → กด "บันทึกการตั้งค่า"

## ใช้งานประจำวัน
1. เปิดเว็บ → กรอก/สแกนเวลาเข้าจอด → กด "เริ่มนับเวลา"
2. เว็บจะซิงก์เวลาไปที่ GitHub ให้อัตโนมัติ (เห็นข้อความ "ซิงก์กับ GitHub สำเร็จ")
3. ปิดแท็บได้เลย — ระบบ Actions จะยิง LINE แจ้งเตือนให้เองเมื่อครบ 3 ชั่วโมง

## ข้อจำกัดที่ควรรู้
- GitHub Actions cron อาจดีเลย์ได้ 1-10 นาทีในบางช่วงเวลา (ข้อจำกัดของ GitHub เอง ไม่ใช่บั๊ก)
- Token ที่กรอกในหน้าเว็บถูกเก็บไว้ในเครื่อง/เบราว์เซอร์ของคุณเท่านั้น แนะนำให้ใช้ fine-grained token ที่จำกัดสิทธิ์แค่ repo นี้ repo เดียว
- ถ้า repo เป็น public ใครก็ตามที่มีลิงก์เว็บสามารถเห็นหน้าเว็บได้ แต่จะเขียนไฟล์ `data/state.json` ไม่ได้ถ้าไม่มี token ของคุณ
