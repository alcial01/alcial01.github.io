
myFunction = function(){
	num = document.getElementById("int").value
	if (isNaN(num) === true || (num%1 !=0 ) || num <= 0 || num ===""){
		alert("You must enter an Integer")
	}
	else{
	 	myprimeFactors = new Array()
		for (var i = 2; i <= num; i++) {
      		while (num % i == 0) {
        		myprimeFactors.push(i)
        		num /= i
      		}
    	}
  		thenum = document.getElementById("int").value
  		if(thenum == 7 || thenum == 5 || thenum == 2 || thenum == 3){		
  			document.getElementById('primefactors').innerHTML= "The prime factor of"+" "+thenum+" "+ "is"+" "+myprimeFactors
  		}
  		else if(thenum == 1){
  			document.getElementById('primefactors').innerHTML= "the number 1 has no prime factor"
  		}
  		else{
  			document.getElementById('primefactors').innerHTML= "The prime factors of"+" "+thenum+" "+ "are"+" "+myprimeFactors.slice(0,-1)+" "+"and"+" "+myprimeFactors.splice(-1,1)
  		}
	}
 
}
//window.onload = myFunction