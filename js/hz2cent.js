function hz2cent() {
    var src = parseFloat(source.value);
    var tgt = parseFloat(target.value);
    cent.innerText = 12 * Math.log2(tgt / src);
}

var cent = document.getElementById('cent');
var target = document.getElementById('target');
var source = document.getElementById('source');
hz2cent();
source.addEventListener('keyup', function(e) {
    hz2cent();
});
target.addEventListener('keyup', function(e) {
    hz2cent();
});
