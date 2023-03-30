// const fs = require("fs")


// function writeFileFromInput(inputElement, filename) { 
//     // Get the first file selected by the user 
//     const file = inputElement.files[0]; 
   
//     // Create a new FileReader object 
//     const reader = new FileReader(); 
   
//     // Define a function to be called when the file is loaded 
//     reader.onload = function() { 
//       // Get the contents of the file 
//       const fileContent = reader.result; 
   
//       // Write the contents to a new file 
//       const blob = new Blob([fileContent], {type: 'c/text'}); 
//       const url = URL.createObjectURL(blob); 
//       const link = document.createElement('a'); 
//       link.download = filename; 
//       link.href = url; 
//       link.click(); 
//     }; 
   
//     // Read the file as text 
//     reader.readAsText(file); 
//   }

