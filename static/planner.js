// Courses Remaining toggle 
let remainingToggle = document.getElementById("courses-remaining-toggle");
remainingToggle.addEventListener("click", (event) => {
  let remainingTable = document.getElementById("remaining-table");
  let finishedTable = document.getElementById("finished-table");
  let classes = [];
  
  for (let i = 0; i < remainingTable.classList.length; i++) {
    classes.push(remainingTable.classList[i]);
  }
  
  if (classes.includes("visible")) {
    // Hide Remaining Table 
    remainingTable.classList.remove("visible");
    remainingTable.classList.add("hidden");
    
    // Show Finished Table 
    finishedTable.classList.remove("hidden");
    finishedTable.classList.add("visible");
    
  } else {
    // Show Remaining Table 
    remainingTable.classList.remove("hidden");
    remainingTable.classList.add("visible");
    
    // Hide Finished Table 
    finishedTable.classList.remove("visible");
    finishedTable.classList.add("hidden");
  }
});

// Courses Finished toggle 
let finishedToggle = document.getElementById("courses-finished-toggle");
finishedToggle.addEventListener("click", (event) => {
  let finishedTable = document.getElementById("finished-table");
  let remainingTable = document.getElementById("remaining-table");
  
  let classes = [];
  
  for (let i = 0; i < finishedTable.classList.length; i++) {
    classes.push(finishedTable.classList[i]);
  }
  
  if (classes.includes("visible")) {
    // Hide Finished Table 
    finishedTable.classList.remove("visible");
    finishedTable.classList.add("hidden");
    
    // Show Remaining Table 
    remainingTable.classList.add("visible");
    remainingTable.classList.remove("hidden");
  } else {
    // Show Finished Table 
    finishedTable.classList.remove("hidden");
    finishedTable.classList.add("visible");
    
    // Hide Remaining Table
    remainingTable.classList.remove("visible");
    remainingTable.classList.add("hidden");
     
    
  }
});