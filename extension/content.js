// The code for the EcoEats extension. Runs in Amazon product pages.
const BASE_URL = "https://caaatdubhacks.pythonanywhere.com/"

let item = encodeURI(id("productTitle").textContent.trim())
let aboutList = qs("#feature-bullets > ul")
let ingredient = encodeURI(qs("#important-information > div").textContent.trim().substring(11).trim())



fetch(BASE_URL + "endpoint")
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
  responseData["total emissions with eutrophying"] = responseData["total emissions with eutrophying"].toFixed(2);
  sessionStorage.setItem("response", responseData);
  let ecoEffect = document.createElement("li");
  ecoEffect.innerHTML = "<a href=\"" + BASE_URL + "table" + "\"><b>EcoEats Info:</b></a> ";
  if(responseData.title_used == false){
    ecoEffct.innerHTML += + "Unable to find data for this specific product, but main ingredient ";
  }
  ecoEffect.innerHTML += responseData["food_matched"] + " emits " +
     responseData["total emissions with eutrophying"] + " kilograms of CO-2 equivalent per kilogram of product";
  aboutList.appendChild(ecoEffect)
}

function id(idName) {
  return document.getElementById(idName);
}

function qs(query) {
  return document.querySelector(query);
}
