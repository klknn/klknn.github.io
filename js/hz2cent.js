var cent = document.getElementById('cent');
var target = document.getElementById('target');
var source = document.getElementById('source');

function hz2cent(unused) {
    var src = parseFloat(source.value);
    var tgt = parseFloat(target.value);
    cent.innerText = 12 * Math.log2(tgt / src);
}

hz2cent();
source.addEventListener('keyup', hz2cent);
target.addEventListener('keyup', hz2cent);
