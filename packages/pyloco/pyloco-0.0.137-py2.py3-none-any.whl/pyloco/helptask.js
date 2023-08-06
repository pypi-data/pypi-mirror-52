bodyHtml = "<div id='shortdesc'></div>" +
           "<div id='longdesc'></div>";

document.body.innerHTML = bodyHtml;

pyloco.onOpen(function openHandler (evt) {
    var status = document.getElementById("status")
    // status.innerHTML = "Pyloco connection open";
});

pyloco.onClose(function closeHandler (evt) {
    var status = document.getElementById("status")
    // status.innerHTML = "Pyloco connection closed";
});

pyloco.onMessage("helptask", "shortdesc", function messageHandler (msgId, ts, msg) {
    var shortdesc = document.getElementById("shortdesc")
    shortdesc.innerHTML = msg;
    // window.console.log(shortdesc.innerHTML)
});

pyloco.onMessage("helptask", "longdesc", function messageHandler (msgId, ts, msg) {
    var longdesc = document.getElementById("longdesc")
    longdesc.innerHTML = msg;
    // window.console.log(longdesc.innerHTML)
});

pyloco.onError(function errorHandler (evt) {
    var status = document.getElementById("status")
    // status.innerHTML = "Pyloco error happend";
});
