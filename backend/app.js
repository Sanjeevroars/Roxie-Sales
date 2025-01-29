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
    ref: "Client",
    required: true, // Ensure the field is populated
  },
  transcriptId: {
    type: mongoose.Schema.ObjectId,
    ref: "Transcript",
  },
  location: String,
  status: {
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

const transcriptSchema = new mongoose.Schema({
  user_info: {
    name: { type: String, required: true },
    contact: { type: String, required: true },
    date: { type: Date, required: true },
    interested_model: { type: String, required: true },
    location: { type: String, required: true },
  },
  transcript: [String],
});

enquirySchema.pre("aggregate", function (next) {
  // Retrieve pipeline options (default to empty object if not set)
  const { year, month } = this.options.pipelineOptions || {};

  const matchStage = {}; // Initialize match conditions

  // ✅ Filter by year if provided
  if (year !== undefined) {
    matchStage.date = {
      $gte: new Date(`${year}-01-01T00:00:00.000Z`),
      $lt: new Date(`${year + 1}-01-01T00:00:00.000Z`),
    };
  }

  // ✅ Filter by month if provided
  if (month !== undefined) {
    matchStage.$expr = { $eq: [{ $month: "$date" }, month] };
  }

  // ✅ Insert '$match' only if filters exist
  if (Object.keys(matchStage).length > 0) {
    this.pipeline().unshift({ $match: matchStage });
  }

  next();
});


const Client =
  mongoose.models.client_models ||
  mongoose.model("client_models", clientSchema);
const Enquiry =
  mongoose.models.enquiry_details ||
  mongoose.model("enquiry_details", enquirySchema);
const Transcript =
  mongoose.transcript_details ||
  mongoose.model("transcript_details", transcriptSchema);

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
  const { user_info, transcript } = req.body;
  // console.log(user_info);

  const { interested_model, ...otherData } = user_info;
  // console.log(interested_model)
  const client = await Client.findOne({ model: interested_model });
  // console.log(client);
  const userTranscript = await Transcript.create(req.body);
  const updatedData = {
    ...otherData,
    interested_model: client._id,
    transcriptId: userTranscript._id,
  };

  const enquiry = await Enquiry.create(updatedData);
  console.log(enquiry);
  res.status(201).json({
    status: "success",
    data: enquiry,
  });
});

app.get("/api/transcripts", async (req, res) => {
  try {
    const transcripts = await Transcript.find();
    res.status(200).json(transcripts);
  } catch (err) {
    console.log(err.message);
  }
});

app.get("/api/transcripts/:id", async (req, res) => {
  const transcriptId = req.params.id;
  try {
    const transcript = await Transcript.findById(transcriptId);
    if (!transcript) throw new Error("transcript not found");
    res.status(200).json({
      status: "ok",
      data: transcript,
    });
  } catch (err) {
    res.status(400).json({
      status: "error",
      data: err.message,
    });
  }
});

app.post("/api/transcripts/:id/status", async (req, res) => {
  const transcriptId = req.params.id;
  const { status } = req.body;
  try {
    const transcript = await Transcript.findById(transcriptId);
    if (!transcript) throw new Error("transcript not found");
    const enquiry = await Enquiry.findOne({ transcriptId: transcript._id });
    // console.log(enquiry)
    const updatedEnquiry = await Enquiry.findByIdAndUpdate(
      enquiry._id,
      { status },
      { new: true }
    );
    res.json({
      status: "ok",
      data: updatedEnquiry,
    });
  } catch (err) {
    res.status(400).json({
      status: "error",
      data: err.message,
    });
  }
});

const getTraffic = async (year , month) => {
  return await Enquiry.aggregate(
    [
      {
        $group: {
          _id: {
            dateTrunc: { $dateTrunc: { date: "$date", unit: "day" } },
          },
          count: { $sum: 1 },
        },
      },
      {
        $sort: { "_id.dateTrunc": 1 }, // Sort by actual Date field
      },

      {
        $setWindowFields: {
          sortBy: { "_id.dateTrunc": 1 }, // Ensure this is a Date type
          output: {
            movingAvg: {
              $avg: "$count",
              window: { range: [-6, 0], unit: "day" },
            },
          },
        },
      },
    ],
    { pipelineOptions: { year, month } }
  );
};

const getEnquiryForEachProduct = async () => {
  return await Enquiry.aggregate([
    {
      $lookup: {
        from: "client_models",
        localField: "interested_model",
        foreignField: "_id",
        as: "productDetails",
      },
    },
    {
      $unwind: "$productDetails",
    },
    {
      $group: {
        _id: "$productDetails.model",
        enquiriesCount: { $sum: 1 },
      },
    },
  ]);
};

const getEnquiryDispersion = async () => {
  return await Enquiry.aggregate([
    {
      $addFields: {
        dateOnly: {
          $dateToString: { format: "%Y-%m-%d", date: { $toDate: "$date" } },
        },
        hour: { $hour: { $toDate: "$date" } },
      },
    },
    {
      $group: {
        _id: { date: "$dateOnly", hour: "$hour" },
        count: { $sum: 1 },
      },
    },
    {
      $group: {
        _id: "$_id.date",
        hours: {
          $push: {
            hour: "$_id.hour",
            count: "$count",
          },
        },
      },
    },
    {
      $project: {
        _id: 0,
        date: "$_id",
        hours: 1,
      },
    },
    {
      $sort: { date: 1 },
    },
  ]);
};

app.get("/enquiry-dispersion-per-hour", async (req, res) => {
  const enquiryDispersion = await getEnquiryDispersion();
  console.log(enquiryDispersion);
  res.json({
    data: enquiryDispersion,
    len: enquiryDispersion.length,
  });
});

app.get("/traffic-each-day", async (req, res) => {
  const year = req.query.year ? parseInt(req.query.year) : undefined;
  const month = req.query.month ? parseInt(req.query.month) : undefined;

  const trafficData = await getTraffic(year, month);
  console.log(trafficData);
  res.json({
    data: trafficData,
  });
});

app.get("/enquiry-per-product", async (req, res) => {
  const enquiryPerProduct = await getEnquiryForEachProduct();
  console.log(enquiryPerProduct);
  res.json({
    data: enquiryPerProduct,
  });
});

app.get('/api/enquiries', async (req, res) => {
  const year = req.query.year ? parseInt(req.query.year) : undefined;
  const month = req.query.month ? parseInt(req.query.month) : undefined;
  try {
      const enquiries = await Enquiry.aggregate([
          {
              $group: {
                  _id: { $substr: ["$date", 0, 10] }, // Group by the date part of the 'date' field
                  count: { $sum: 1 }, // Count the number of enquiries per day
              },
          },
          { $sort: { _id: 1 } }, // Sort by date
      ],
      { pipelineOptions: { year, month } 
    });

  res.json(enquiries.map(entry => ({ date: entry._id, enquiries: entry.count })));
} catch (error) {
  res.status(500).send(error.message);
}
});

app.listen(3000, () => {
  console.log(`App running on Port ${PORT}`);
});
