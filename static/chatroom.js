var socket;

$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ":" + location.port + '/chatroom');
    socket.on('connection', function () {
        socket.emit('join', {});
    });

    socket.on('status', function (data) {
        $("#chatbox").val($("#chatbox").val() + data.msg + '\n')
        $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    });

    socket.on('message', function (data) {
        $("#chatbox").val($("#chatbox").val() + data.msg + '\n');
        $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    });

    $("#text").keyup( function (e) {
        if (e.keyCode === 13) {
            $("#send").click();
        }
    });

    $("#send").click( function (e) {
        text = $("#text").val();
        $("#text").val('');
        socket.emit('text', {msg: text});
    });
});

function leave_room() {
    socket.emit('leave', {}, function() {
        socket.disconnect();
        window.location.href = "";
    });
}