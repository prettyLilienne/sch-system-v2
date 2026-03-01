let scholarships = JSON.parse(localStorage.getItem("scholarships")) || [];
let applications = JSON.parse(localStorage.getItem("applications")) || [
    {student:"Juan Dela Cruz", scholarship:"TSU Academic Excellence", status:"Pending"},
    {student:"Maria Garcia", scholarship:"Financial Assistance", status:"Approved"}
];
function saveData(){
    localStorage.setItem("scholarships", JSON.stringify(scholarships));
    localStorage.setItem("applications", JSON.stringify(applications));
    updateDashboard();
}
function showSection(id){
    document.querySelectorAll(".section").forEach(sec=>sec.style.display="none");
    document.getElementById(id).style.display="block";
}
function openModal(){
    document.getElementById("scholarshipModal").style.display="flex";
}
function closeModal(){
    document.getElementById("scholarshipModal").style.display="none";
}
function addScholarship(){
    let name = document.getElementById("schName").value;
    let amount = document.getElementById("schAmount").value;
    let slots = document.getElementById("schSlots").value;
    let deadline = document.getElementById("schDeadline").value;
    
    if(!name) return alert("Please fill all fields");

    scholarships.push({name, amount, slots, deadline});
    saveData();
    renderScholarships();
    closeModal();
}
function renderScholarships(){
    let table = document.getElementById("scholarshipTable");
    table.innerHTML = "";
    scholarships.forEach((s,index)=>{
    table.innerHTML += `
        <tr>
            <td>${s.name}</td>
            <td>${s.amount}</td>
            <td>${s.slots}</td>
            <td>${s.deadline}</td>
                <td>
                <button class="danger" onclick="deleteScholarship(${index})">Delete</button>
                </td>
        </tr>
`;
});
}
function deleteScholarship(index){
    scholarships.splice(index,1);
    saveData();
    renderScholarships();
}
function renderApplications(){
    let table = document.getElementById("applicationTable");
    table.innerHTML = "";
    applications.forEach((a,index)=>{
    table.innerHTML += `
        <tr>
            <td>${a.student}</td>
            <td>${a.scholarship}</td>
            <td>${a.status}</td>
            <td>
            <button class="success" onclick="approve(${index})">Approve</button>
            <button class="danger" onclick="reject(${index})">Reject</button>
            </td>
        </tr>
`;
});
}
function approve(index){
    applications[index].status="Approved";
    saveData();
    renderApplications();
}
function reject(index){
    applications[index].status="Rejected";
    saveData();
    renderApplications();
}
function searchScholarship(){
    let input = document.getElementById("searchScholarship").value.toLowerCase();
    let rows = document.querySelectorAll("#scholarshipTable tr");
    rows.forEach(row=>{
    row.style.display = row.innerText.toLowerCase().includes(input) ? "" : "none";
});
}
function updateDashboard(){
    document.getElementById("totalScholarships").innerText = scholarships.length;
    document.getElementById("totalApplications").innerText = applications.length;
    document.getElementById("totalApproved").innerText =
    applications.filter(a=>a.status==="Approved").length;
}
renderScholarships();
renderApplications();
updateDashboard();