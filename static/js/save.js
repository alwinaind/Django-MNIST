function save(){
    var form = document.getElementById('imageform')
    var canvasObj = document.getElementById("canvas");
    var img = canvasObj.toDataURL();
    img = img.substring(22)
    var field = document.getElementById('img')
    field.value = ""
    field.value = img;
    form.submit();
}