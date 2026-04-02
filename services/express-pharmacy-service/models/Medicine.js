const mongoose = require('mongoose');

const MedicineSchema = new mongoose.Schema({
    name: { type: String, required: true },
    description: { type: String },
    stock: { type: Number, required: true, default: 0 },
    price: { type: Number, required: true },
    category: { type: String, default: 'General' }
}, { timestamps: true });

module.exports = mongoose.model('Medicine', MedicineSchema);