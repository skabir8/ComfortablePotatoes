var addPlayer = function(e){
    var name = this.getAttribute("value");
    var cteam = document.getElementById("team");
    var nteam = document.getElementById("team");
    nteam.innerHTML = cteam + name + "<br>" ;
}

var playerButtons = document.getElementsByClassName("player");
for(var i=0; i<playerButtons.length;i++){
    var b = playerButtons[i];
    b.addEventListener("click", addPlayer);
}
