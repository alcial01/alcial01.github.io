var val = 0
function getval(){
  event.preventDefault();
  val =  parseInt(document.getElementById('masterdiv').getAttribute('value'));
  console.log(val)


}



function sendComments(){
  event.preventDefault();

  //comment_nickName = document.getElementById('commName').value
  //comment = document.getElementById('userComment').value
  //$formdata = new Formdata($("#myform2")[0]);
  var cookieValue = document.querySelector('.commentModal').id
  console.log(cookieValue);
  console.log("hi")
  //console.log($formdata)

}