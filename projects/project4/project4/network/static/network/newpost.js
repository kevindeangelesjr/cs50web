document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#new-post-btn').addEventListener('click', new_post);
  });

function new_post(){

    document.querySelector('#new-post').style.display = 'block';
}