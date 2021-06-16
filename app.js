const formidable = require('formidable');
var express = require('express');
const fs = require('fs');
const path = require('path')
var app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('uploads'));
const port = 3000;
const MYURL = 'ht.xyz'
const sizeLimitBytes = 20000000;
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


app.get("/",(req, res) => {
	res.send("ok!");
})


app.get("/:id",(req, res) => {
	res.sendFile(__dirname + '/uploads/' + req.params.id);
})

app.post("/", (req, res) => {

	

new formidable.IncomingForm().parse(req)
	.on('progress', function(bytesReceived, bytesExpected) {
 	 if(bytesReceived > sizeLimitBytes ){
   	 return false; //exit the program
  	}
	})
    .on('fileBegin', (name, file) => {
		var ext = file.name.split(".").pop();
		var finalname = makeid(4)+'.'+ext;
		
        file.path = __dirname + '/uploads/' + finalname
		res.send(MYURL+"/"+finalname+"\n");

    })
    .on('file', (name,file) => {
      console.log('Uploaded file', file)
    })	

});


app.listen(port,()=>{
	console.log('Server started at port 3000 successfully!');
});

