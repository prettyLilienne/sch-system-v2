// Initialize Icons

let currentRowEditing = null; 
let rowTable = null;
let row=null;
const allFields = ["amount", "slots", "deadline",  "status"]; 
let criteriaCount = 0;  


lucide.createIcons();
// Simple SPA Routing Logic
    function showPage(pageId) { //nav i the only one clickable
// Hide all pages. it was selected by class name (.content area)
        document.querySelectorAll('.content-area').forEach(page => {
page.classList.remove('active'); //Gets
});
// Remove active class from nav items
        document.querySelectorAll('.nav-item').forEach(item => {
item.classList.remove('active');
}); //same concept so gets
// Show current page. Parameters on nav should match their content
        document.getElementById('page-' + pageId).classList.add('active');
        //id of thr content area should match (e.g page-dashboard) to show current page. gets

// Set active nav item. 
        const activeNav = Array.from(document.querySelectorAll('.nav-item')).find(item =>
        item.innerText.toLowerCase().includes(pageId)
);      // activeNav = new variable
        //in .nav-item Array its finding navigation button with the same pageId
        if(activeNav) activeNav.classList.add('active');
// Update Breadcrumb or showing kung nasaang page ka na
            const breadcrumb = document.getElementById('header-breadcrumb');
            const pageTitle = pageId.charAt(0).toUpperCase() + pageId.slice(1);
            breadcrumb.innerHTML = `<i data-lucide="layout-dashboard" style="width:14px"></i>
            Admin Dashboard / ${pageTitle}`;
            lucide.createIcons();
            //gets
}



//for pop up div
    function openModal() {
        document.getElementById('addModal').style.display = 'flex';
            //i think i need to create id for each input so thats getelementbyid
            //then eavery input should stored in the table, byt idk how to d that
    }
    function closeModal() {
        document.getElementById('addModal').style.display = 'none';
}

  /*  function createModal(){
       const newName= document.getElementById('add-name').value;
       const newDesc= document.getElementById('add-desc').value;
       const newAmount= document.getElementById('add-amount').value;
       const newSlots= document.getElementById('add-slots').value;
       const newDeadline= document.getElementById('add-deadline').value;
       const newStat= document.getElementById('add-status').value;
       const newReqs= document.getElementById('add-reqs').value;
       const tbody = document.getElementById('tableBody');
       const row = document.createElement('tr');
    
       row.innerHTML=`
       <td>
       <strong>${newName}</strong><br>
       <small>${newDesc}</small>
       </td> 
       <td>${newAmount}</td>
       <td>${newSlots}</td>
       <td>${newDeadline}</td>
       <td><span class="badge badge-active">${newStat}</span></td>
       <td>
       <button class="edit-btn" onclick="openEditModal(this)">E</button>
       <button class="delete-btn" onclick="deleteScholarship(this)">T</button>
       </td>
      `;
        row.dataset.newReqs=newReqs;
        row.dataset.newDesc=newDesc;



      tbody.appendChild(row);
    closeModal();
    }

*/
    function openEditModal(button){
            //pre fills the inputs
      /*  const row = button.closest('tr');
        currentRowEditing=row;
       
        const cells = row.querySelectorAll("td");
        console.log(cells);

        const strong = cells[0].querySelector("strong");
        const small = cells[0].querySelector("small");

        //currentRowEditing = row;
        //const tds = Array.from(row.children);
         document.getElementById("edit-name").value=strong.textContent.trim();
         document.getElementById("edit-desc").value=small.textContent.trim();
        console.log(allFields);
        
        allFields.forEach((field, index) => {
            const input = document.getElementById('edit-'+ field);
            console.log(input);
            console.log(field);

            if (input){
                let value =cells[index+1].textContent.trim();
                console.log(value);
                if (field==="amount"){
                    value=value.replace(/[₱,]/g,"");
                }
                input.value=value;
            }
        });*/
        //console.log(input);
        document.getElementById('editModal').style.display = 'flex';
    }
       
    function closeEditModal() {
document.getElementById('editModal').style.display = 'none';

}

// --- ACTION FUNCTIONS ---
function saveChanges() {
    console.log("clicked!");
    if (!currentRowEditing) {
        console.log("no row selected");
        return
    }
     console.log(currentRowEditing)
    //const row = button.closest('tr');
    //console.log(row);
    const cells = currentRowEditing.querySelectorAll("td"); //null
    console.log(row);
    //const cells = currentRowEditing.querySelectorAll("td"); //null
    console.log("cells:" ,cells);
    cells[0].querySelector("strong").textContent=document.getElementById("edit-name").value;
    cells[0].querySelector("small").textContent=document.getElementById("edit-desc").value;

    allFields.forEach((td,i)=>{
        if (i>=allFields.length) return;
        console.log(td);

        const input=document.getElementById('edit-'+ td);
        console.log(input);

        if (!input) return;
        let value = input.value;

        if (td ==="amount"){
            value=value.replace(/[₱,]/g,"");
            console.log(value);
                }

        cells[i + 1].textContent = value;
        console.log(value);
    });
    
    document.getElementById('editModal').style.display = 'none';
    currentRowEditing=null;
        }

//application buttons
function filterTable (){
    console.log("searching...");
    const searchInput = document.getElementById("sInput").value.toLowerCase();
    console.log(searchInput);
    const table = document.getElementById('applicationTable');
    console.log("table: ", table);
    

    const rows = table.querySelectorAll("tbody tr");
    console.log("total rows found ", rows.length);

       rows.forEach((row,i) =>{
        const firstCell = row.querySelector("td");
        const name= (firstCell?.textContent || "").toLowerCase();
        console.log(`Row ${i}: ` , name);
       });
        rows.forEach(row => {
        const nameStrong = row.querySelector("td strong");
        const name = (nameStrong?.textContent || "").toLowerCase();
        
        if (name.includes(searchInput)){
            row.style.display=""; 
        } else { 
            row.style.display="none"; 
        } 
       }); 
}  

function menuToggle()  { 
     document.getElementById("profileMenu").style.display="block";

    
}

function deleteModal(button) { 
    rowTable = button.closest('tr');
    const name = rowTable.cells[0].querySelector('strong').textContent.trim();
    document.getElementById("deleteName").textContent = name;
    document.getElementById('deleteModal').style.display = 'flex';
}
function cancelDel() { 
    document.getElementById('deleteModal').style.display = 'none';
}
function confirmDel(){
    if (!rowTable){
        rowTable.remove();
        rowTable=null;
    }
   // const row = button.closest('tr');
     rowTable.remove();
     document.getElementById("deleteModal").style.display="none";
}

function evaluation(button){
    const row = button.closest('tr');
       
   // const cells = row.querySelectorAll("td");
   // console.log(cells);
   
    const name = row.querySelector("strong").textContent;
    console.log(name);

    document.getElementById("studName").textContent=name;

    document.getElementById('evaluationModal').style.display="flex";

}
function evalStud(){
    
}
function cancelEval(){
    document.getElementById("evaluationModal").style.display="none";
}
 
function addCriteriaRow(name = "", percent = "") { 
  const tbody = document.getElementById("criteriaTable").querySelector("tbody"); 
 
  const tr = document.createElement("tr"); 
  tr.setAttribute("data-id", criteriaCount); 
 
  tr.innerHTML = ` 
    <td><input type="text" class="criteria-name" placeholder="Criteria" 
value="${name}"></td> 
    <td><input type="number" class="criteria-percent" min="0" max="100" 
value="${percent}"></td> 
    <td><button type="button" 
onclick="removeCriteriaRow(${criteriaCount})">
❌
</button></td> 
  `; 
 
  tbody.appendChild(tr); 
  const percentInput = tr.querySelector(".criteria-percent"); 
  percentInput.addEventListener("input", updateCriteriaTotal); 
 
  criteriaCount++; 
  updateCriteriaTotal(); 
} 
 
function removeCriteriaRow(id) { 
  const tbody = document.getElementById("criteriaTable").querySelector("tbody"); 
  const row = tbody.querySelector(`tr[data-id='${id}']`); 
  if (row) row.remove(); 
  updateCriteriaTotal(); 
} 
 
function updateCriteriaTotal() { 
  const percentInputs = document.querySelectorAll(".criteria-percent"); 
  let total = 0; 
 
  percentInputs.forEach(input => { 
    const val = parseFloat(input.value); 
    if (!isNaN(val)) total += val; 
  });       
 
  document.getElementById("criteriaTotal").textContent = total; 
   if (total !== 100) { 
    document.getElementById("criteriaTotal").style.color = "red"; 
  } else { 
    document.getElementById("criteriaTotal").style.color = "green"; 
  } 
} 

function menuToggle() {
   // document.getElementById("profileMenu").style.display="block";
   // profileMenu.style.display = profileMenu.style.display === "block" ? "none" : "block"; 
    document.getElementById("profileMenu").classList.toggle("show");
}
window.onclick=function(event){
    if(!event.target.matches('.drop-btn')){
        var dropdowns = document.getElementsByClassName("profile-menu");
       var i;
       for (i=0;i<dropdowns.length;i++){
        var openD=dropdowns[i];
        if (openD.classList.contains('show')){
            openD.classList.remove('show');
        }}
    }
}

const modal = document.getElementId("editModal");

modal.addEventListener ("click" , function (event){
if (event.target===modal){
    console.log('click');
        modal.style.display="none";
    }
});
    
function closeMenu (){
    document.getElementById("profileMenu").style.display="none";
}

document.onclick = function (event ){
    const menu = document.getElementById("profileMenu");
    const btn = document.getElementById("profileIcon");

    if (menu.contains(event.target) && ! btn.contains (event.target)){
        menu.style.display="none";
    }
}


