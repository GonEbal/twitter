document.addEventListener('DOMContentLoaded', function() {
	let likelButtons = document.querySelectorAll('.like');
	 for(let i = 0; i < likelButtons.length; i++) {
		likelButtons[i].addEventListener('click', function() {
			like_post(i+1);
		});
	}
	document.querySelector('#tweet').addEventListener('click', tweet_post);
	console.log(document.querySelectorAll('.like'));
});

function like_post(id) {
	console.log("Like was clicked! ", id);
	fetch(`/like/${id}`, {
  	method: 'PUT',
  	body: JSON.stringify({
      like: 6
  })
})
	var el = parseInt(document.getElementById(id).innerHTML);
	console.log(typeof el);
	el++;
	document.getElementById(id).innerHTML = el++;
}

function tweet_post() {

	console.log("dadad")

	fetch('/tweet', {
  	method: 'POST',
  	body: JSON.stringify({
      content: document.querySelector('#content').value
  })
})
}