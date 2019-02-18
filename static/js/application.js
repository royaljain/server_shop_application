
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('my-image-event1', function(msg) {
        console.log("Received Link" + msg.image_link);
        document.getElementById("imageid1").src=msg.image_link;
    });

    socket.on('my-text-event1', function(msg) {
        console.log("Received Text" + msg.image_link);
        document.getElementById("textid1").innerHTML=msg.text;
    });

    socket.on('my-image-event2', function(msg) {
        console.log("Received Link" + msg.image_link);
        document.getElementById("imageid2").src=msg.image_link;
    });

    socket.on('my-text-event2', function(msg) {
        console.log("Received Text" + msg.image_link);
        document.getElementById("textid2").innerHTML=msg.text;
    });

    socket.on('my-image-event3', function(msg) {
        console.log("Received Link" + msg.image_link);
        document.getElementById("imageid3").src=msg.image_link;
    });

    socket.on('my-text-event3', function(msg) {
        console.log("Received Text" + msg.image_link);
        document.getElementById("textid3").innerHTML=msg.text;
    });

});

function FirstServed(){
    document.getElementById("imageid1").src="static/images/icons/default_female.png";
    document.getElementById("textid1").innerHTML="Default ";
    socket.emit('empty_div_1');}

function SecondServed(){
    document.getElementById("imageid2").src="static/images/icons/default_male.png";
    document.getElementById("textid2").innerHTML="Default ";
    socket.emit('empty_div_2');}

function ThirdServed(){
    document.getElementById("imageid3").src="static/images/icons/default_female.png";
    document.getElementById("textid3").innerHTML="Default ";
    socket.emit('empty_div_3');}