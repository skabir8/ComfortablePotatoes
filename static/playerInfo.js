var addPlayer = function(e){
    var name = this.getAttribute("value");
    var team = document.getElementById("team");
    team.innerHTML = team.innerHTML + name + "<br>" ;
}

var playerButtons = document.getElementsByClassName("player");
for(var i=0; i<playerButtons.length;i++){
    var b = playerButtons[i];
    b.addEventListener("click", addPlayer);
}

var statButtons = document.getElementsByClassName("displayStats");
for(var i=0; i<statButtons.length; i++){
    var b = statButtons[i];
    b.addEventListener("click", 
}
