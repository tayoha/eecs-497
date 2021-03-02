const myHeading = document.querySelector('h1');
myHeading.textContent = 'This js text replaced the old html text';

var API_KEY = '20169026-d45bc99749bd521df7aa7b5f4';
var URL = "https://pixabay.com/api/?key="+API_KEY+"&q="+encodeURIComponent('apples');
$.getJSON(URL, function(data){
if (parseInt(data.totalHits) > 0)
    $.each(data.hits, function(i, hit){ console.log(hit.pageURL); });
else
    console.log('No hits');
});