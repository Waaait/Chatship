var socket;

$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ":" + location.port + '/chatroom');
    socket.on('connect', function () {
        socket.emit('join', {});
    });

    socket.on('status', function (data) {
        $("#chatbox").val($("#chatbox").val() + data.msg + '\n')
        $("#chatbox").scrollTop($("#chatbox").val()[0].scrollHeight);
    });

    socket.on('message', function (data) {
        $("#chatbox").val($("#chatbox").val() + data.msg + '\n');
        $("#chatbox").scrollTop($("#chatbox").val()[0].scrollHeight);
    });

    $("#send").click(function(e) {
        text = $("#text").val();
        $("#text").val('');
        socket.emit('text', {msg: text});
    });
});

function leave_room() {
    socket.emit('leave', {}, function() {
        socket.disconnect();
        window.location.href = "{{ url_for('index') }}";
    });
}