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


<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Sustainibilty Scanner</title>
    <style>
      body {background-color: MediumSpringGreen;}
      h2   {color: white; text-align: center;}
      h3   {color: white; text-align: center;}
      div {display: flex; justify-content: center;}
      button {background-color: DeepSkyBlue; color: white; border-color: white; border-radius: 8px;  border-style: solid; text-bold: yes;}
      /* The switch - the box around the slider */
      .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
      }

      /* Hide default HTML checkbox */
      .switch input {
        opacity: 0;
        width: 0;
        height: 0;
      }

      /* The slider */
      .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        -webkit-transition: .4s;
        transition: .4s;
      }

      .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        -webkit-transition: .4s;
        transition: .4s;
      }

      input:checked + .slider {
        background-color: #2196F3;
      }

      input:focus + .slider {
        box-shadow: 0 0 1px #2196F3;
      }

      input:checked + .slider:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
      }

      /* Rounded sliders */
      .slider.round {
        border-radius: 34px;
      }

      .slider.round:before {
        border-radius: 50%;
      }
    </style>
  </head>
  <body>
      <img src="earth.png" width="100" height="100">
      <div>
      <a href="https://caaatdubhacks.pythonanywhere.com/table", target="blank">
        <button>
          <b>View Detailed Breakdown</b>
        </button>
      </a>
    </div>
    <!-- <h3>Turn On</h3>
    <div>
      <label  class="switch">
        <input type="checkbox">
        <span class="slider round"></span>
      </label>
    </div> -->
  </body>
</html>
