var r1 = [1064847, 1064845, 1064849, 1064850, 1064851, 1064852, 1064843, 1064846, 1064848, 1064844];

for (j = 0; j < r1.length; j++){

    setTimeout(rpc('scorers','1|'+r1[j]+'|soccer'), 1000);

    var scoretable = document.getElementsByClassName('scorertable');
    for (i = 0; i < scoretable.length; i++) { 
        console.log(scoretable[i].childNodes[0].innerText);
        console.log(scoretable[i].childNodes[1].innerText);
    }
}



var r1 = [1064847, 1064845, 1064849, 1064850, 1064851, 1064852, 1064843, 1064846, 1064848, 1064844];

for (j = 0; j < r1.length; j++){

    $('this').queue(function(){
        rpc('scorers','1|'+r1[j]+'|soccer');

        var scoretable = document.getElementsByClassName('scorertable');
        for (i = 0; i < scoretable.length; i++) { 
            console.log(scoretable[i].childNodes[0].innerText);
            console.log(scoretable[i].childNodes[1].innerText);
        }
    });
}



