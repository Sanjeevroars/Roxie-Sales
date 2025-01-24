import express from "express";
import mongoose from "mongoose";

const enquirySchema = new mongoose.Schema({
  name: String,
  contact: Number,
  date: Date,
  interested_model: {
    type: mongoose.Schema.ObjectId,
    ref: "Client", // Reference to the Client model
    required: true, // Ensure the field is populated
  },
  location: String,
  active: {
    type: String,
    default: "Active",
    enum: ["Active", "Not Active", "Converted"],
  },
});

const clientSchema = new mongoose.Schema({
  model: String,
  aliases: [String],
  category: [String],
  variants: [String],
});

const Client =
  mongoose.models.client_models ||
  mongoose.model("client_models", clientSchema);
const Enquiry =
  mongoose.models.enquiry_details ||
  mongoose.model("enquiry_details", enquirySchema);

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json);
const PORT = 3000;

app.post("/api/end_conversation", async (req, res) => {
  const { user_info } = req.body;
  console.log(user_info);

  const {interested_model,...otherData }= user_info;
  const client = Client.findOne({ name: interested_model });
  const updatedData  = {...otherData,interested_model:client._id}

  const enquiry = await Enquiry.create(updatedData)
  console.log(enquiry)
  res.status(201).json({
    status: "success",
    data: enquiry,
  });
});

app.listen(3000, () => {
  console.log(`App running on Port ${PORT}`);
});
