var collapsables = ["trace"];
var subs = {"1":"uno", "2":"dos"}
vjson.map((item, i) => makeDivsFor(item, i))

function makeSeparator(i){
    var dg = $("<div><a class='btn btn-primary' data-toggle='collapse' href='#collapseExample' role='button' aria-expanded='false' aria-controls='collapseExample'>"+
    i+
    "</a></div>");
    dg.addClass("separator");                
    return dg;
}

function makeDivsFor(item, i){
    var divitem = $("#basediv")
    divitem.addClass("basediv");
    separator = makeSeparator(i);
    divitem.append(separator);                
    for (key in item){
        if (item.hasOwnProperty(key)) {
            if (key in subs){
                key = subs[key];
            }
            var dg = $('<div/>');
            dg.addClass("item " + key);                
            dg.append(makeDiv('key ' + key,key,i))
            .append(makeDiv('value ' + key,item[key], i));
            divitem.append(dg);
        }
    }
}

function makeDiv(clazz, html, i){
    if (collapsables.includes(clazz.split(" ")[1])){
        return $('<div id="'+i+clazz.split(" ")[1]+clazz.split(" ")[0]+'" class="' + clazz + '">'+html+'</div>');   
    }
    return $('<div class="' + clazz + '">'+html+'</div>');
}