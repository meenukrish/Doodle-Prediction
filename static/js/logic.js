

function submitted()
{
    console.log("submitted is clicked")
    selectedcanvas = d3.select("#maincanvas").node();
  
    /* Code to send canvas image with background color. Otherwise the image showup as black */
    // ###############################################################
    var context = selectedcanvas.getContext("2d");

    contextimage = context.getImageData(0,0,768,269);   

    console.log(`contextimage width ${contextimage.width}`);
    console.log(`contextimage height ${contextimage.height}`);

    var compositeOperation = context.globalCompositeOperation;
    context.globalCompositeOperation = "destination-over";
    // //set background color
    context.fillStyle = "rgb(230, 230, 230)";  //original color of the canvas
    // //draw background / rect on entire canvas
    context.fillRect(0,0,768,269);  //(250,60,164,191);

    MainCanvaswidth = 768 ; 
    MainCanvasheight = 269; 

    var innerBoxPerc = 50;
    var greyBoxStartX = MainCanvaswidth * ((1 - (innerBoxPerc / 100)) / 2);
    var greyBoxStartY = MainCanvasheight * ((1 - (innerBoxPerc / 100)) / 2);

    var greyBoxWidth = MainCanvaswidth * (innerBoxPerc / 100)/1.37  
    var greyBoxHeight = MainCanvasheight * (innerBoxPerc / 100)*2;

    // console.log(`greyBoxStartX : ${greyBoxStartX}`);
    // console.log(`greyBoxStartY : ${greyBoxStartY}`);
    // console.log(`greyBoxWidth : ${greyBoxWidth}`);
    // console.log(`greyBoxHeight : ${greyBoxHeight}`);

    var hidden_canv = document.createElement('canvas');
    hidden_canv.style.display = 'none';
    document.body.appendChild(hidden_canv);
    hidden_canv.width = greyBoxWidth;
    hidden_canv.height = greyBoxHeight;

    //Draw the data you want to download to the hidden canvas
    var hidden_ctx = hidden_canv.getContext('2d');
    hidden_ctx.drawImage(
    selectedcanvas, 
    greyBoxStartX,//Start Clipping
    greyBoxStartY,//Start Clipping
    greyBoxWidth,//Clipping Width
    greyBoxHeight,//Clipping Height
    0,//Place X
    0,//Place Y
    hidden_canv.width,//Place Width
  hidden_canv.height//Place Height
  );

  var compositeOperation = hidden_ctx.globalCompositeOperation;
  hidden_ctx.globalCompositeOperation = "destination-over";

  hidden_ctx.fillStyle = "rgb(230, 230, 230)"; 
  hidden_ctx.fillRect(0,0,hidden_canv.width,hidden_canv.height);
  
  var inputimage = hidden_canv.toDataURL("image/png");  //original
  
  hidden_ctx.globalCompositeOperation = compositeOperation;

    // //clear the canvas
    context.clearRect(0,0,768,269);  
    // //restore it with original / cached contextimage
    context.putImageData(contextimage,0,0); 
    
    //reset the globalCompositeOperation to what it was
    context.globalCompositeOperation = compositeOperation;
    
    // ###############################################################
      
    //  console.log(`inputimage: ${inputimage}`);    

    imagedata = inputimage.replace("data:image/png;base64,","");

    d3.select("#inputimage").attr("src",inputimage);

    predicturl = `/predict`

    d3.json(predicturl,{
        method:"POST",
        body: JSON.stringify({"imagedata": imagedata}),
        headers: { "Content-type": "image/png"}
      }).then(function(qdcategory)
    {
        // debugger;
        console.log(qdcategory);
        predictedcategory = qdcategory["category"]
        console.log(predictedcategory);
        predictedimage = d3.select("#predictedimage");
        imagepath = `./static/qdimages/${predictedcategory}.png`;
        predictedimage.attr("src",imagepath);
    });
    
}

function clearpredictions()
{
    console.log("Inside Clear function")
    d3.select("#inputimage").attr("src"," ");
    d3.select("#predictedimage").attr("src"," ");
}
