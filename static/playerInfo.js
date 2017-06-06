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

/*var statButtons = document.getElementsByClassName("displayStats");
for(var i=0; i<statButtons.length; i++){
    var b = statButtons[i];
    b.addEventListener("click", add
}*/

var comp = function(player1, player2){
    var p1 = parseFloat(player1.innerHTML);
    if(p1 > player2){
	return "color:green";
    }if(p1 < player2){
	return "color:red";
    }if(p1 == player2){
	return "color:black";
    }
    
}

var compare = function(e){
    var stats = this.parentNode.parentNode.childNodes;
    var name = document.getElementById("name");
    name.innerHTML = stats[1].innerHTML;
    var n = name.innerHTML;
    var pnt = document.getElementById("pnt");
    pnt.innerHTML = stats[3].innerHTML;
    var p = parseFloat(pnt.innerHTML);
    var reb = document.getElementById("reb");
    reb.innerHTML = stats[5].innerHTML;
    var r = parseFloat(reb.innerHTML);
    var ast = document.getElementById("ast");
    ast.innerHTML = stats[7].innerHTML;
    var a = parseFloat(ast.innerHTML);
    var com = (a + p + r)/3;
    var avg = document.getElementById("avg");
    avg.innerHTML = com;
    var names = document.getElementsByClassName("name");
    var pnts = document.getElementsByClassName("pnt");
    var rebs = document.getElementsByClassName("reb");
    var asts = document.getElementsByClassName("ast");
    for(var i=0; i < pnts.length; i++){
	pnts[i].setAttribute("style", comp(pnts[i], p));
	rebs[i].setAttribute("style", comp(rebs[i], r));
	asts[i].setAttribute("style", comp(asts[i], a));
	if(names[i].innerHTML == n){
	    pnts[i].setAttribute("style", "color:blue");
	    rebs[i].setAttribute("style", "color:blue");
	    asts[i].setAttribute("style", "color:blue");
	}
    }

}    

var getInfo = function(e){
    var pid = this.getAttribute("id");
    $.ajax({
	url: "../utils/statsScraper",
	type: "POST",
	data: {param: pid},
	datatype: "dictionary"
    }).done(function(result) {
        alert(result['name']);
    }).fail(function() {
        console.log("oops");
    });;
}
var compareButtons = document.getElementsByClassName("compare");
for(var i=0; i<compareButtons.length; i++){
    var b = compareButtons[i];
    b.addEventListener("click", getInfo);
}
