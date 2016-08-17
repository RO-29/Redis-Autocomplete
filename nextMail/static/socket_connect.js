var socket = io.connect('http://' + document.domain + ':' + location.port);

window.bank_names = [];
window.selected_bank_name = '';

socket.on('connect', function() {
    socket.emit('get_bank_names');
    });

socket.on('bank_city_recieve', function(data_cities) {
    $("#results_append").html("");
    data_cities.forEach(function(city, index){
        $("#results_append").append($("<li>").html('<a href="#">'+city+'</a>'));
    });
    
    });


socket.on('bank_names_recieve', function(bank_names){
    var sel = document.getElementById('bank_names_list');
    var fragment = document.createDocumentFragment();
    bank_names.forEach(function(bank_name, index) {
        var opt = document.createElement('option');
        opt.innerHTML = bank_name;
        opt.value = bank_name;
        fragment.appendChild(opt);
    });
    sel.appendChild(fragment);
    window.bank_names = bank_names;
});


socket.on('bank_city_details_recieve', function(data_city_branches) {
    console.log(data_city_branches);
    data_city_branches.forEach(function(data_city, index){
        html_text = '<div class="card"><h4 class = "card-header">'+data_city['branch']+'!</h4><div class = "card-body" >IFSC: '+data_city['ifsc']+'<br>Bank:'+ window.selected_bank_name +'<br>Branch:' + data_city['branch']+'<br> City:'+ window.selected_city_name +'</div></div>';
        $('#right').append(html_text);
    });   

});
    





$( "#bank_names_list" ).change(function() {
    $("#results_append").html("");
  window.selected_bank_name = $("#bank_names_list option:selected").text();
});


$('#city_keyword').on('input', function() { 
    if (!!$(this).val()){
        socket.emit('get_city_names', window.selected_bank_name , $(this).val())
    }
    else{
        $("#results_append").html("");
    }
});

$('#results_append').on('click', 'li', function () {

    city= $(this).text();
        $("#city_keyword").val(city);
        $("#results_append").html("");
        window.selected_city_name = city
        socket.emit("get_city_details",window.selected_bank_name, city)

});



