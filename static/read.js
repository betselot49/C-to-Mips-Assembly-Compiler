
const form = document.getElementById("form");


let theInp = document.getElementById("inputFile")
theInp.value = contents

form.addEventListener("submit", (e)=> {
e.preventDefault()
})


function readFiles() { 
    let file = document.getElementById('fileInput').files[0]; 
   
    let reader = new FileReader(); 
    reader.onload = function(event) { 
      contents = event.target.result;
      console.log("path ",file)
      let theInp = document.getElementById("inputFile")
      theInp.value = contents
      //displayContents(contents); 
     // localStorage.setItem("content", contents)
    }; 
    reader.readAsText(file); 
  }

  function displayContents(contents) { 
    let element = document.getElementById('fileContents'); 
    element.innerText = contents; 
    console.log(contents)
  }

 
  //contents = localStorage.getItem("content")

