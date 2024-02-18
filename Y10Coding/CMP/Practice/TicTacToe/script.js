turn = 0;
end = 0;
player = 0;

document.getElementById("p1").innerHTML = prompt("First player's name");
document.getElementById("p2").innerHTML = prompt("Second player's name");

function takeTurn(e) {
    if (e.innerHTML == '<img src="UCC.png" width="100px">' && !end) {
        if (turn%2) e.innerHTML = '<img src="Turnitin.png" width="100px">';
        else e.innerHTML = '<img src="ChatGPT.png" width="90px">';
        turn += 1;
        if (turn > 4) checkWin(e.innerHTML);
    }
} 

function checkWin(p) {
    grid = document.getElementsByClassName("gameCell");
    for (let i = 0; i < grid.length; i+=3) {
        if (grid[i].innerHTML == grid[i+1].innerHTML && grid[i].innerHTML == grid[i+2].innerHTML && grid[i].innerHTML == p) Win(p);
    }
    for (let i = 0; i < grid.length/3; i++) {
        if (grid[i].innerHTML == grid[i+3].innerHTML && grid[i].innerHTML == grid[i+6].innerHTML && grid[i].innerHTML == p) Win(p);
    }
    if (grid[0].innerHTML == grid[4].innerHTML && grid[0].innerHTML == grid[8].innerHTML && grid[0].innerHTML == p) Win(p);
    else if (grid[2].innerHTML == grid[4].innerHTML && grid[2].innerHTML == grid[6].innerHTML && grid[2].innerHTML == p) Win(p);
    if (turn-player == grid.length && !end) Cat(p);
}

function Win(p) {
    console.log("Winner is "+p);
    document.getElementById("gameMsg").innerHTML = "Winner is "+p+'<br><button type="button" onclick=reset();>Play Again</button>';
    end = 1;
    addScore(p);
}

function Cat() {
    console.log("Cat's game.");
    document.getElementById("gameMsg").innerHTML = "Cat's game."+'<br><button type="button" onclick=reset();>Play Again</button>';
    end = 1;
    addScore('');
}

function addScore(p) {
    if (p == '<img src="ChatGPT.png" width="90px">') document.getElementById("1").innerHTML = parseFloat(document.getElementById("1").innerHTML) + 1
    else if (p == '<img src="Turnitin.png" width="100px">') document.getElementById("2").innerHTML = parseFloat(document.getElementById("2").innerHTML) + 1
    else {
        document.getElementById("1").innerHTML = parseFloat(document.getElementById("1").innerHTML) + 0.5
        document.getElementById("2").innerHTML = parseFloat(document.getElementById("2").innerHTML) + 0.5
    }
    player ^= 1
}

function reset() {
    turn = player;
    end = 0;
    grid = document.getElementsByClassName("gameCell");
    for (let i = 0; i < 9; i++) {
        grid[i].innerHTML = '<img src="UCC.png" width="100px">';
    }
    document.getElementById("gameMsg").innerHTML = '';
}
