//Stack class
Stack=function(){
    this.aStack=new Array()
}
Stack.prototype.push=function(item){
    this.aStack.push(item)
}
Stack.prototype.pop=function(){
     if(!this.isEmpty()) { return this.aStack.pop(); } 
    else {
        return false
    }
}
Stack.prototype.isEmpty = function() { return (this.aStack.length == 0); }
Stack.prototype.length=function(){
    return this.aStack.length
}
Stack.prototype.peek=function(){
    return this.aStack[this.aStack.length-1]
}
Stack.prototype.clone=function(){
    newStack=new Stack()
    for(i in this.aStack){
        newStack.push(this.aStack[i])
    }
    return newStack
}
Stack.prototype.reverse=function(){
    result=new Stack()
    for(idx=this.aStack.length-1;idx>=0;idx--){
        result.push(this.aStack[idx])
    }
    return result;
}
Stack.prototype.asArray = function() {
        // this is a method that I'm using to externally clone a stack
        // .slice(0) is a trick to return a *copy* of the array.
        return this.aStack.slice(0);
    }
 Stack.prototype.setArray = function(new_array) {
        // BE VERY CAREFUL- this replaces the contents of this stack with
        // whatever is in new_array
        this.aStack = new_array;
    }

Stack.prototype.toString = function() {
        str = "BOTTOM \n";
        for(var i=0; i<this.aStack.length; i++) {
            str += this.aStack[i] + "\n"
        }
        return str += "TOP";
    }


//Queue class
Queue=function(){
    this.aQueue=new Array()
}
Queue.prototype.enqueue=function(item){
    this.aQueue.push(item)
}
Queue.prototype.dequeue=function(){
    return this.aQueue.shift()
}
Queue.prototype.peek=function(){
    return this.aQueue[0]
}
Queue.prototype.isEmpty=function(){
    if(this.aQueue.length==0)return true;
    return false;
}

//Set class
Set=function(){
    this.aSet=new Array()
}
Set.prototype.contains=function(item){
    for(i in this.aSet)
        if(this.aSet[i]===item) return true;
    return false;
}
Set.prototype.add=function(item){
    if(!this.contains(item)) this.aSet.push(item)
}
Set.prototype.del=function(item){
    var index=this.aSet.indexOf(item)
    if(index>=0){
       return this.aSet.splice(index,1)
    }
}
Set.prototype.isEmpty=function(){
    if(this.aSet.length==0)return true;
    return false;
}

//look for a word in a particular list
contains = function(word, list) {
    for(x in list)
        if(list[x] === word)
            return true;
    return false;
}

//
adjacent = function(word, list){
    alphabets = ['a','b','c','d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    adjList = []
    if (contains(word, list)){
        for (i in word){
            for (a in alphabets){
                newStr = word.slice(0, i) + alphabets[a] + word.slice(Number(i)+1)
                if (contains(newStr, list) && newStr !== word){
                    adjList.push(newStr)
                }
            }
        }           
    }
    return adjList
}
       


function next(data, stack) {
    
    for(var i=0; i<data.dict.length; i++) {
        if(misMatch(stack.peek(), data.dict[i]) == 1) {
            if(!data.used_words.contains(data.dict[i])) { 
                var st = cloneStack(stack);
                st.push(data.dict[i]); 
                data.queue.enqueue(st);
                data.used_words.add(data.dict[i]);
            }
        }
    }
    return true;
}

function iterate(data) {

    while (!data.queue.isEmpty()) {
        var current_stack = data.queue.dequeue(); // stack containing a possible ladder
        var top_word = current_stack.peek();

        if(top_word == data.end) { return current_stack; } // found a valid ladder - we're done
        else {
            next(data, current_stack);       
        }
    }
    return false; // failed to find a ladder
}

function misMatch(word1, word2) {
    // find the number of letter differences between word1 and word2
    var d = 0;
    for(var i=0; i<word1.length; i++) {
        if (word1[i] != word2[i]) { d++; }
    }
    return d;
}

function start() {
    var data = {}

    // get form data
    data.start = document.getElementById("word1").value;
    data.end = document.getElementById("word2").value;
    data.len = parseInt(document.getElementById("length").value);
    
    // validate the inputs
    if((data.start == "") || (data.end == "")) {
        data.error = "word_empty";
        return data;
    }
    else if(data.start == data.end) {
        data.error = "same_word";
        return data;
    }
    else if ((data.start.length != data.len) || (data.end.length != data.len)) {
        data.error = "word_length";
        return data;
    }
   
    // choose the dictionary
    if(data.len == 3) { data.dict = threeLetterWords; }
    else if(data.len == 4) { data.dict = fourLetterWords; } 
    else { data.dict = fiveLetterWords; }

    // structures for algorithm
    data.queue = new Queue();
    data.used_words = new Set();

    return data;
}

function cloneStack(orig_stack) {
    var new_stack = new Stack();
    new_stack.setArray(orig_stack.asArray());
    return new_stack;
}

function ladder() {
    var data = start();

    if(data.error) {
        if(data.error == "same_word") {
            data.error = "Those are the same words!";
        }
        if(data.error == "word_length") {
            data.error = "<b>Error</b>: You chose to use " 
                          + data.len 
                          + "-letter words, but entered a starting or ending word that was not the correct length!";
        }
        if(data.error == "word_empty") {
            data.error = "<b>Error</b>: One or more of the word fields is empty. You must enter a starting and ending word";
        }
   }
    else {

        data.used_words.add(data.start); 
    
        var stack = new Stack(); 
        stack.push(data.start);

        next(data, stack);
        var ladder = iterate(data); 
        if(!ladder) { 
            data.error = "Failed to find a valid ladder between " + data.start + " and " + data.end;
        }
        else {
            data.error = undefined;
            data.ladder = ladder
        }
    }
    displayLadder(data);
}

function displayLadder(data) {
    if(data.error) {
        document.getElementById("results").innerHTML = data.error;
    }
    else {
        var ul = document.createElement("ul"); 
        while(!data.ladder.isEmpty()) {    
            var li = document.createElement("li");
            li.innerHTML = data.ladder.pop()
            ul.appendChild(li);
        }
        var li = document.createElement("li");
        ul.appendChild(li);
        document.getElementById("results").innerHTML = ""; 
        document.getElementById("results").appendChild(ul);
    }
}


//











