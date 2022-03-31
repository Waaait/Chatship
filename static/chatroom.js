var socket;

$(document).ready( () =>  {
    socket = io.connect('http://' + document.domain + ":" + location.port + '/chatroom');
    // socket = io.connect('https://chatship.herokuapp.com/' + '/chatroom');
    socket.on('connect', () => {
        socket.emit('join', {});
    });

    socket.on('status', (data) => {
        $("#chatbox").val($("#chatbox").val() + data.msg + '\n')
        $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    });

    socket.on('message', (data)  => {
        $("#chatbox").val($("#chatbox").val() + data.msg + '\n');
        $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    });

    $("#text").keyup( (e) => {
        if (e.keyCode === 13) {
            $("#send").click();
        }
    });

    $("#send").click( (e) => {
        text = $("#text").val();
        $("#text").val('');
        socket.emit('text', {msg: text});
    });
});

function leave_room() {
    socket.emit('leave', {}, ()  =>  {
        socket.disconnect();
        window.location.href = "";
    });
}