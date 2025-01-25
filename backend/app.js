import express from "express";
import mongoose from "mongoose";
import { DateTime } from "luxon";

mongoose
  .connect(
    "mongodb+srv://sanjeevsitaraman7:sanjeevsitaraman7@cluster0.4dte6.mongodb.net/client_info",
    {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    }
  )
  .then(() => console.log("MongoDB Connected"))
  .catch((err) => console.log(err));

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
app.use(express.json());
console.log("ok");
const PORT = 3000;

app.get("/", (req, res) => {
  console.log("sdfsdfg");
  res.json({
    status: "success",
  });
});

app.post("/api/end_conversation", async (req, res) => {
  // console.log("ok");
  const { user_info } = req.body;
  // console.log(user_info);

  const { interested_model, ...otherData } = user_info;
  // console.log(interested_model)
  const client = await Client.findOne({ model: interested_model });
  // console.log(client);
  const updatedData = { ...otherData, interested_model: client._id };

  const enquiry = await Enquiry.create(updatedData);
  console.log(enquiry);
  res.status(201).json({
    status: "success",
    data: enquiry,
  });
});

const getTraffic = async () => {
  return await Enquiry.aggregate([
    {
      $addFields: {
        dateOnly: {
          $substr: ["$date", 0, 10],
        },
      },
    },
    {
      $group: {
        _id: "$dateOnly", // Group by the formatted date
        trafficCount: { $sum: 1 }, // Count the number of documents for each date
      },
    },
  ]);
};

const  getEnquiryForEachProduct = async  ()=>{
  return await Enquiry.aggregate([
    {
      $lookup:{
        from:"clientmodels",
        localField:"interested_model",
        foreignField:"_id",
        as:"productDetails",
      },
    },
    {
      $unwind:"$productDetails",
    },
    {
      $group: {
        _id: "$productDetails.name", // Group by product name
        enquiriesCount: { $sum: 1 }, // Count the number of enquiries
      },
    },
  ])
}

app.get("/traffic-each-day", async (req, res) => {
  const trafficData = await getTraffic();
  console.log(trafficData);
  res.json({
    data: trafficData,
  });
});
app.get("/enquiry-per-product",async (req,res)=>{
  const enquiryProduct = await getEnquiryForEachProduct();

})
app.listen(3000, () => {
  console.log(`App running on Port ${PORT}`);
});
