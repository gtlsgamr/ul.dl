//requirements
var express = require('express');
var fs = require('fs');
var path = require('path')
var multer = require('multer');

//app 

var app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('uploads'));

//someconstants

const port = 3000;
const sizeLimitBytes = 20000000;

//function to generate random ids

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return result;
}

//multer storage object to save file as random name

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './uploads')
  },
  filename: function (req, file, cb) {
	ext = file.originalname.split(".").pop();
    cb(null, makeid(4) + '.' + ext);
  }
})

//upload object for uploading files

var upload = multer({dest: 'uploads/',storage:storage,limits:{fileSize:sizeLimitBytes}}).single('file');

//GET request for homepage

app.get("/",(res) => {
	res.sendFile(__dirname+'/templates/'+'home.html');
})

//GET request for files that directly serves the files from public directory

app.get("/:id",(req, res) => {
	res.sendFile(__dirname + '/uploads/' + req.params.id);
})

//upload functionality

app.post("/",(req, res) => {
	upload(req,res,function(err){
		if (err instanceof multer.MulterError){
			res.send(err.message + '\n');
		}
	  fl = req.file;
	  res.send(req.headers.host+'/'+fl.filename+'\n');
	});
});


app.listen(port,()=>{
	console.log('Server started at port 3000 successfully!');
});

