console.log("loaded")
let item = id("productTitle").textContent.trim()

let aboutList = qs("#feature-bullets > ul")

let ingredient = qs("#important-information > div").textContent.trim().substring(11).trim()

fetch("https://caaatdubhacks.pythonanywhere.com/api")
  .then(checkStatus)
  .then(JSON.parse)
  .then(displayData)
  .catch(console.log);


function checkStatus(response) {
  if (response.status >= 200 && response.status < 300 || response.status === 0) {
    return response.text();
  } else {
    return Promise.reject(new Error(response.status + ": " + response.statusText));
  }
}

function displayData(responseData) {
  responseData["total emissions with eutrophying"] = responseData["total emissions with eutrophying"].toFixed(2)
  let ecoEffect = document.createElement("li");
  if(responseData.title_used == true){
    ecoEffect.innerHTML = "<a href=\"" + "https://caaatdubhacks.pythonanywhere.com/" +
     "\"><b>EcoEats Info:</b> " + responseData["food_matched"] + " emits " +
     responseData["total emissions with eutrophying"] + "kilograms of CO-2 equivalent per kilogram of product" + "<a>"
  } else {
    ecoEffect.innerHTML = "<a href=\"" + "https://caaatdubhacks.pythonanywhere.com/" +
     "\"><b>EcoEats Info:</b> " + "Unable to find data for this specific product, but main ingredient " + responseData["food_matched"] + " emits " +
     responseData["total emissions with eutrophying"] + "kilograms of CO-2 equivalent per kilogram of product" + "<a>"
  }
  aboutList.appendChild(ecoEffect)
}

function id(idName) {
  return document.getElementById(idName);
}

function qs(query) {
  return document.querySelector(query);
}
