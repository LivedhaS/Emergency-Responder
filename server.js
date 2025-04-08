const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const multer = require("multer");
const path = require("path");
const bodyParser = require("body-parser");


const app = express();
app.use(express.json());
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public')); // serves all files from public folder

const fs = require("fs"); // ✅ Add this line
const CSV_FILE = "patient.csv";


// ✅ MongoDB Connection with Error Handling
mongoose.connect("mongodb://127.0.0.1:27017/burn_classification_db", {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB Connection Error:", err));

// ✅ User Schema & Model
const UserSchema = new mongoose.Schema({
    role: { type: String, enum: ["patient", "doctor"], required: true },
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});
const User = mongoose.model("User", UserSchema);

// ✅ Burn Image Schema & Model
const BurnImageSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    imageUrl: { type: String, required: true },
    severity: { type: String, enum: ["Mild Burn", "Second Degree", "Third Degree"], default: "Unknown" },
    uploadedAt: { type: Date, default: Date.now }
});
const BurnImage = mongoose.model("BurnImage", BurnImageSchema);

// ✅ Wound Image Schema & Model
const WoundImageSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    imageUrl: { type: String, required: true },
    woundType: {
        type: String,
        enum: ["Abrasions", "Bruises", "Burns", "Cut", "Ingrown nails", "Laceration", "Stab wound"],
        default: "Unknown"
    },
    uploadedAt: { type: Date, default: Date.now }
});
const WoundImage = mongoose.model("WoundImage", WoundImageSchema);

const SOSSchema = new mongoose.Schema({
    name: String,
    type: String,
    latitude: Number,
    longitude: Number,
    timestamp: { type: Date, default: Date.now }
  });
  const SOS = mongoose.model("SOS", SOSSchema);

// ✅ Multer Storage for Image Uploads
const storage = multer.diskStorage({
    destination: "./uploads/",
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});
const upload = multer({ storage });

// ✅ User Registration
app.post("/register", async (req, res) => {
    try {
        const { role, name, email, password } = req.body;
        if (!role || !name || !email || !password) {
            return res.status(400).json({ message: "All fields are required!" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const user = new User({ role, name, email, password: hashedPassword });
        await user.save();
        res.json({ message: "✅ Registration successful!" });
    } catch (error) {
        console.error("❌ Registration Error:", error);
        res.status(500).json({ message: "Error registering user", error });
    }
});

// ✅ User Login
app.post("/login", async (req, res) => {
    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).json({ message: "Email and Password are required!" });
        }

        const user = await User.findOne({ email });
        if (!user) return res.status(400).json({ message: "❌ User not found!" });

        const isValidPassword = await bcrypt.compare(password, user.password);
        if (!isValidPassword) return res.status(400).json({ message: "❌ Invalid password!" });

        const token = jwt.sign({ id: user._id, role: user.role }, "your_secret_key", { expiresIn: "1h" });
        res.json({ message: "✅ Login successful!", token, role: user.role });
    } catch (error) {
        console.error("❌ Login Error:", error);
        res.status(500).json({ message: "Error logging in", error });
    }
});

// ✅ Image Upload Route
app.post("/upload", upload.single("image"), async (req, res) => {
    try {
        if (!req.file) return res.status(400).json({ message: "❌ No file uploaded!" });

        const { userId } = req.body;
        if (!userId) return res.status(400).json({ message: "❌ User ID is required!" });

        // Check if user exists
        const user = await User.findById(userId);
        if (!user) return res.status(400).json({ message: "❌ User not found!" });

        // Save Image in Database
        const newImage = new BurnImage({
            userId: userId,
            imageUrl: `/uploads/${req.file.filename}`,
            severity: "Unknown"
        });

        await newImage.save();
        res.json({ message: "✅ Image uploaded successfully!", imageUrl: newImage.imageUrl });
    } catch (error) {
        console.error("❌ Upload Error:", error);
        res.status(500).json({ message: "Error uploading image", error });
    }
});

// ✅ Serve Uploaded Images
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

// ✅ Fetch Burn Classification History
app.get("/history", async (req, res) => {
    try {
        const history = await BurnImage.find().populate("userId", "name email");
        res.json(history);
    } catch (error) {
        console.error("❌ History Fetch Error:", error);
        res.status(500).json({ message: "Error fetching burn history", error });
    }
});

// ✅ Simple Rule-Based Chatbot
app.post("/chatbot", (req, res) => {
    const userMessage = req.body.message.toLowerCase();
    let reply;

    if (userMessage.includes("burn treatment")) {
        reply = "For minor burns, cool the burn with running water and apply aloe vera. For severe burns, seek medical attention immediately.";
    } else if (userMessage.includes("symptoms")) {
        reply = "Burn symptoms include redness, swelling, pain, and blisters.";
    } else {
        reply = "I'm not sure about that. Try asking about burn treatment, symptoms, or prevention tips!";
    }

    res.json({ reply });
});




app.get('/hospital.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'hospital.html'));
});

app.get('/form', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'form.html'));
});

  
  // Ensure CSV file exists
if (!fs.existsSync(CSV_FILE)) {
    fs.writeFileSync(CSV_FILE, "Name,Blood Group,Allergies,Medications,Medical Conditions,Emergency Contact Name,Emergency Contact Number\n");
}

app.post("/save", (req, res) => {
    const { name, bloodGroup, allergies, medications, medicalConditions, contactName, contactNumber } = req.body;

    if (!name || !bloodGroup || !contactName || !contactNumber) {
        return res.status(400).send("Missing required fields.");
    }

    const newRow = `${name},${bloodGroup},${allergies},${medications},${medicalConditions},${contactName},${contactNumber}\n`;

    fs.appendFile(CSV_FILE, newRow, (err) => {
        if (err) {
            return res.status(500).send("Error saving data.");
        }
        res.send("✅ Patient data saved successfully!");
    });
});
app.get("/sos-alerts", async (req, res) => {
    const alerts = await SOS.find().sort({ timestamp: -1 });
    res.json(alerts);
  });
  
  app.post("/sos", async (req, res) => {
    const { name, type, latitude, longitude } = req.body;
    const newSOS = new SOS({ name, type, latitude, longitude });
    await newSOS.save();
    res.json({ message: "🆘 SOS saved!" });
  });

  
  

// ✅ Start Server
const PORT = 3000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
