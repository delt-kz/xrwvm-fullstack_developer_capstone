const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const Reviews = require('./review');
const Dealerships = require('./dealership');
const app = express();
app.use(express.json({limit:'64kb'}));
const Counter = mongoose.model('Counter',new mongoose.Schema({_id:String,seq:Number}));
const route = handler => async(req,res,next)=>{try{await handler(req,res);}catch(e){next(e);}};
app.get('/',(req,res)=>res.json({status:'ok',service:'dealership-api'}));
app.get('/fetchReviews',route(async(req,res)=>res.json(await Reviews.find().lean())));
app.get('/fetchReviews/dealer/:id',route(async(req,res)=>res.json(await Reviews.find({dealership:Number(req.params.id)}).lean())));
app.get('/fetchDealers',route(async(req,res)=>res.json(await Dealerships.find().sort({id:1}).lean())));
app.get('/fetchDealers/:state',route(async(req,res)=>res.json(await Dealerships.find({state:req.params.state}).sort({id:1}).lean())));
app.get('/fetchDealer/:id',route(async(req,res)=>res.json(await Dealerships.find({id:Number(req.params.id)}).lean())));
app.post('/insert_review',route(async(req,res)=>{
 const data=req.body;
 if(!await Dealerships.exists({id:Number(data.dealership)}))return res.status(400).json({error:'Unknown dealership'});
 const count=await Counter.findByIdAndUpdate('reviews',{$inc:{seq:1}},{new:true});
 const review=await Reviews.create({...data,id:count.seq});
 res.status(201).json(review);
}));
app.use((err,req,res,next)=>{console.error(err.message);res.status(err.name==='ValidationError'?400:500).json({error:'Unable to process request'});});
async function start(){
 await mongoose.connect(process.env.MONGODB_URI || 'mongodb://mongo_db:27017/dealershipsDB');
 for(const [model,file,key] of [[Dealerships,'dealerships.json','dealerships'],[Reviews,'reviews.json','reviews']]){
  const rows=JSON.parse(fs.readFileSync(path.join(__dirname,'data',file),'utf8'))[key];
  if(!await model.exists({})) await model.insertMany(rows);
 }
 const latest=await Reviews.findOne().sort({id:-1});
 await Counter.updateOne({_id:'reviews'},{$max:{seq:latest?latest.id:0}},{upsert:true});
 app.listen(process.env.PORT || 3030,'0.0.0.0',()=>console.log('Dealership API ready on port '+(process.env.PORT || 3030)));
}
start().catch(err=>{console.error(err.message);process.exit(1);});
