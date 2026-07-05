const { initializeApp, cert } = require("firebase-admin/app");
const { getFirestore, Timestamp, FieldValue } = require("firebase-admin/firestore");
const fs = require("fs");
const path = require("path");

// ── Load service account key ───────────────────────────────────
const keyPath = path.join(__dirname, "serviceAccountKey.json");
const serviceAccount = JSON.parse(fs.readFileSync(keyPath, "utf8"));
console.log("✅  Key loaded for project:", serviceAccount.project_id);

const sampleData = JSON.parse(fs.readFileSync(path.join(__dirname, "sample_data.json"), "utf8"));

// ── Init ──────────────────────────────────────────────────────
initializeApp({ credential: cert(serviceAccount) });
const db = getFirestore();

// ── Helpers ───────────────────────────────────────────────────
function buildTimestamp(date, time) {
  if (!date || !time) return null;
  return Timestamp.fromDate(new Date(`${date}T${time}+05:30`));
}

async function createStudents() {
  console.log("\n📁  Creating 'students' collection...");
  const col = db.collection("students");
  for (const student of sampleData.students) {
    await col.doc(student.studentId).set({
      ...student,
      createdAt: FieldValue.serverTimestamp(),
    });
    console.log(`   ✅  ${student.studentId} — ${student.name}`);
  }
}

async function createAttendance() {
  console.log("\n📁  Creating 'attendance' collection...");
  const col = db.collection("attendance");
  for (const record of sampleData.attendance) {
    await col.add({
      studentId: record.studentId,
      name:      record.name,
      date:      record.date,
      time:      record.time ?? null,
      status:    record.status,
      deviceId:  record.deviceId ?? null,
      synced:    record.synced,
      timestamp: buildTimestamp(record.date, record.time),
    });
    console.log(`   ✅  ${record.name.padEnd(18)} | ${record.date} | ${record.status}`);
  }
}

(async () => {
  try {
    await createStudents();
    await createAttendance();
    console.log("\n🎉  Done! Open Firebase Console → Firestore to see your data.");
    process.exit(0);
  } catch (err) {
    console.error("❌  Error:", err.message);
    process.exit(1);
  }
})();
