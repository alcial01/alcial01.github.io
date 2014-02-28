
MyClass = function(age,Name) {
 var ssn = 585858585
 var weight = 59
 this.ssn = ssn
 this.weight = weight
 this.age = age
 this.Name = Name
 this.foo = function(){
    console.log(this.age)
    //baz()
 }

  this.baz = function(){
    console.log(this.Name)
 }
}
MyClass.prototype.gainWeight = function(lbs){
    this.pub = this.weight+ lbs
    return this.pub


}
MyClass.prototype.getSSN = function(){
   return this.ssn
    
}

MyClass.prototype.getWeight = function(){
    return this.weight
}
MyClass.prototype.birthday = function(){
    newAge = this.age +1
    return newAge
}


x = new MyClass(23,'Alain')
x.foo()
x.baz()
console.log(x.birthday ())