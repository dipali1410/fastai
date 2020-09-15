var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      el("result-label").innerHTML = `Result = ${response["result"]}, Probability = ${response["probability"]}`;
    }
    el("analyze-button").innerHTML = "Analyze";
  };
 
  
function img() {
  if (${response["result"]} = "Jacob Elordi or Noah"){
    url = "https://i.insider.com/5f22ebfe19182415af6d1122?width=1100&format=jpeg&auto=webp"
  }
  else if (${response["result"]} = "Joel Courtney or Lee"){
    url = "https://i.pinimg.com/originals/38/20/70/3820706a112ac32ae61f0b8f6557c6e6.jpg"
  }
  else if (${response["result"]} = "Joey King or Elle"){
    url = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/joey-king-index-social-1-1596649980.png"
  }
  else if (${response["result"]} = "Maise Richardson-sellers or Chloe"){
    url = "https://assets.popbuzz.com/2020/28/maisie-richardson-sellers-age-1594758136-view-0.jpg"
  }
  else if (${response["result"]} = "Meganne Young or Rachel"){
    url = "https://image.tmdb.org/t/p/original/fifyhHBRKYFHR1DieYysI30T3i5.jpg"
  }
  else if(${response["result"]} = "Molly Ringwald known or Sara Flynn"){
    url = "https://s.yimg.com/ny/api/res/1.2/znXmy0unC5NjdHwkxHrWvg--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9ODAw/http://media.zenfs.com/en/homerun/feed_manager_auto_publish_494/5ac89786c8bc4a636404db2f996b725c"
  }
  else if(${response["result"]} = "Taylor Zakhar Perez or Marco"){
    url = "https://scontent.fdel13-1.fna.fbcdn.net/v/t1.0-9/s960x960/118629059_125321649279929_6037148333577130362_o.jpg?_nc_cat=102&_nc_sid=110474&_nc_ohc=n-PJ7vKgsIAAX8gJ2z8&_nc_ht=scontent.fdel13-1.fna&tp=7&oh=9a4ff314e700b03456113ac8b01b04d2&oe=5F875B4B"
  }
  var img = document.createElement('img'); 
  img.src = url
  document.getElementById('body').appendChild(img); 
        }  
  
  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

