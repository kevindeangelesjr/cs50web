// define a variable in javascript (use let)

// Use local storage to save data for subsequent page visits
if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}

/*
function count(){
    //counter = counter + 1;
    //counter += 1;
    counter++;
    alert(counter);
}
*/

function count(){
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('h1').innerHTML = counter;

    if (counter % 10 === 0){
        // 'template literal' - back tick is equivalent of python f string
        alert(`Count is now ${counter}`);
    }

    localStorage.setItem('counter', counter);
}

// Event listener - fired when DOM is done loading (all elements loaded), second argument is function to run
document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    // set value of onlick property in JavaScript
    document.querySelector('button').onclick = count;  

    //setInterval - every 1000 ms run the count function
    setInterval(count, 1000);
})