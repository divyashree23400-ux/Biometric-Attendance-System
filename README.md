# Samarth — Firebase Setup Guide

## What's in this folder

| File | Purpose |
|------|---------|
| `database_schema.json` | Full schema for both Firestore collections |
| `sample_data.json` | 5 students + 15 attendance records (3 days) |
| `setup_firestore.js` | Run once to push all data to Firestore |
| `firestore.rules` | Security rules to paste into Firebase Console |

---

## Step 1 — Create the Firebase Project

1. Go to https://console.firebase.google.com
2. Click **Add project** → name it `samarth-attendance`
3. Disable Google Analytics (not needed) → **Create project**

---

## Step 2 — Enable Firestore

1. In the left sidebar → **Build → Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** (you'll add rules later)
4. Pick any region (e.g. `asia-south1` for India) → **Enable**

---

## Step 3 — Get the Service Account Key

1. In the left sidebar → ⚙️ **Project Settings → Service accounts**
2. Click **Generate new private key** → confirm
3. Save the downloaded `.json` file as **`serviceAccountKey.json`** in this folder

---

## Step 4 — Run the Setup Script

```bash
# Install the Firebase Admin SDK
npm install firebase-admin

# Push collections + sample data to Firestore
node setup_firestore.js
```

You should see:

```
📁  Creating 'students' collection...
   ✅  STU001 — Rahul Sharma
   ✅  STU002 — Priya Nair
   ...

📁  Creating 'attendance' collection...
   ✅  Rahul Sharma       | 2026-06-29 | Present
   ✅  Priya Nair         | 2026-06-29 | Present
   ...

🎉  Done!
```

---

## Step 5 — Apply Security Rules

1. Firebase Console → **Firestore → Rules tab**
2. Replace the default rules with the contents of `firestore.rules`
3. Click **Publish**

---

## Collections Created

### `students`
Stores the master list of registered students.

```
STU001/
  ├── studentId     : "STU001"
  ├── name          : "Rahul Sharma"
  ├── rollNo        : "22CS101"
  ├── branch        : "Computer Science"
  ├── year          : 3
  ├── fingerprintId : 1          ← matches ID on R307 sensor
  └── createdAt     : <timestamp>
```

### `attendance`
Every punch recorded by the ESP32 terminal.

```
<auto-id>/
  ├── studentId  : "STU001"
  ├── name       : "Rahul Sharma"   ← denormalised for fast reads
  ├── date       : "2026-07-01"
  ├── time       : "09:32:00"
  ├── status     : "Present" | "Late" | "Absent"
  ├── deviceId   : "ESP32-LAB-01"
  ├── synced     : true | false     ← false = came from offline queue
  └── timestamp  : <Firestore Timestamp>
```

---

## Sample Data Loaded

- **5 students** across `22CS101`–`22CS105`
- **15 attendance records** — 3 days (Jun 29, Jun 30, Jul 1)
- Mix of Present / Late / Absent statuses
- One record with `synced: false` to simulate an offline-queued push
