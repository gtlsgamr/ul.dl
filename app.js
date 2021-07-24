//requirements
var express = require('express');
var fs = require('fs');
var path = require('path')
var multer = require('multer');
var exts = require('./exts')

//app 

var app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
//someconstants

const port = 3121;
const sizeLimitBytes = 20000000;
console.log(exts.extensions);
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

app.get("/",(req,res) => {
	res.sendFile(__dirname+'/templates/'+'home.html');
})

//GET request for files that directly serves the files from public directory

app.get("/:id",(req, res) => {
	f1 = req.params.id.split(".")[0] //filename
	f2 = req.params.id.split(".")[1] //file extension
	if(exts.extensions.includes(f2)){ //if file is of "Text" type
		var file = __dirname + '/uploads/' + req.params.id;
		fs.readFile(file, {encoding: 'utf-8'}, function(err,data){
			if (!err) {
				res.writeHead(200, {'Content-Type': 'text/plain'});
				res.write(data);
				res.end();
			} else {
				console.log(err);
			}
		});
	}
	else{
		var file = __dirname + '/uploads/' + req.params.id;
		res.sendFile(file);
	}
})

app.get("/robots.txt", () => {
	return ```User-agent: *
Disallow: /
	```
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

