var socket = io.connect('http://' + document.domain + ':' + location.port);

window.bank_names = [];
socket.on('connect', function() {
	socket.emit('get_bank_names');
    });

socket.on('bank_names_recieve', function(data_bank){
	console.log(data_bank);
	window.bank_names = data_bank;
});

//socket.emit('get_bank_cities')