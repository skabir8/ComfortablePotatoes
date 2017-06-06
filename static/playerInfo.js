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

var percent = function(dec){
    var val = parseFloat(dec);
    val = Math.round(val * 1000)/10;
    var percent = val.toString() + "%";
    return percent
    
}

var compare = function(e){
    var stats = this.childNodes[1].innerHTML;
    var data = JSON.parse(stats);
    stats = data["stats"];
    var name = document.getElementById("name");
    name.innerHTML = data['name']
    var img = document.getElementById("image");
    img.innerHTML = "<img src=" + data['image'] + ">";
    var wl = document.getElementById("win-loss");
    wl.innerHTML = "Win-Loss: " + stats["W"] + "-" + stats["L"];
    var gp = document.getElementById("gp");
    gp.innerHTML = "Games Played: " + stats["GP"];
    var min = document.getElementById("min");
    min.innerHTML = "Minutes: " + stats["MIN"];
    var pts = document.getElementById("pts");
    pts.innerHTML = "Points " + stats["PTS"];
    var fg = document.getElementById("fg");
    fg.innerHTML = "Field Goals: " + stats["FGM"] + "(" + stats["FGA"] + ") - " + percent(stats["FG_PCT"]);
    var three = document.getElementById("3p");
    three.innerHTML = "3 Pointers: " + stats["FG3M"] + "(" + stats["FG3A"] + ") - " + percent(stats["FG3_PCT"]);
    var ft = document.getElementById("ft");
    ft.innerHTML = "Free Throws: " + stats["FTM"] + "(" + stats["FTA"] + ") - " + percent(stats["FT_PCT"]);
    var ast = document.getElementById("ast");
    ast.innerHTML = "Assists: " + stats["AST"];
    var oreb = document.getElementById("oreb");
    oreb.innerHTML = "Offensive Rebounds: " + stats["OREB"];
    var blk = document.getElementById("blk");
    blk.innerHTML = "Blocks: " + stats["BLK"];
    var stl = document.getElementById("stl");
    stl.innerHTML = "Steals: " + stats["STL"];
    var dreb = document.getElementById("dreb");
    dreb.innerHTML = "Defensive Rebounds: " + stats["DREB"];
    var pfd = document.getElementById("pfd");
    pfd.innerHTML = "Fouls Drawn: " + stats["PFD"];
    var pf = document.getElementById("pf");
    pf.innerHTML = "Fouls: " + stats["PF"];
}    


var compareButtons = document.getElementsByClassName("compare");
for(var i=0; i<compareButtons.length; i++){
    var b = compareButtons[i];
    b.addEventListener("click", compare);
}

var prev = document.getElementById("prev");
var next = document.getElementById("next");
var prevPage = function(e){
    var page = document.getElementById("pageNum");
    var nPage = parseInt(page.innerHTML);
    if(nPage > 1){
	page.innerHTML = nPage - 1;
    }
}
var nextPage = function(e){
    var page = document.getElementById("pageNum");
    var nPage = parseInt(page.innerHTML);
    if(nPage < 8){
	page.innerHTML = nPage + 1;
    }
}
prev.addEventListener("click", prevPage);
next.addEventListener("click", nextPage);
