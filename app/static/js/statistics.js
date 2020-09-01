var topDiv = document.getElementById("TopBut");
var midDiv = document.getElementById("MidBut");
var botDiv = document.getElementById("BotBut");
var topOp = document.querySelectorAll('input[name="top_options"]');
var botOp = document.querySelectorAll('input[name="bot_options"]');
var textDiv = document.getElementById("textDiv");
var graphDiv = document.getElementById("graphDiv");
topDiv.style.display = "block";
midDiv.style.display = "block";
botDiv.style.display = "block";
textDiv.style.display = "none";
graphDiv.style.display = "none";


function checkOpt(x){
    let selectedValue;
    for (const op of x){
        if (op.checked){
            selectedValue = op.value;
            // op.checked = true;
            break;
        }
        // op.checked = false;
    }
    return selectedValue;
    // showDateSel(selectedValue)
}

function checkTop(){
    var x = checkOpt(topOp);
    if (x == "Category" || x == "Account"){
        midDiv.style.display = "block";
    } else{
        midDiv.style.display = "none";
    }
}

function checkBot(){
    textDiv.style.display = "none";
    graphDiv.style.display = "none";
    var x = checkOpt(botOp);
    if (x == "text"){
        textDiv.style.display = "block";
        graphDiv.style.display = "none";
    } else if (x=="graph"){
        textDiv.style.display = "none";
        graphDiv.style.display = "block";
    }
}


function updateList(dataDic, yearElement, monthElement){
    // var selY = document.getElementById("year");
    // var selM = document.getElementById("month");
    var monDic = dataDic;
    var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    var selYear = parseInt(yearElement.value);
    for (var i=0; i <= monDic[selYear].length; i++){
        var option = document.createElement("option");
        if (i==0){
            option.text = "";
        }else{
            var textOp = months[monDic[selYear][i-1]-1];
            option.text = textOp;
        };
        monthElement.add(option);
    }
}
