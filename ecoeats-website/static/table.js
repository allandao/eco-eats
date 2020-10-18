(function () {
      "use strict";
      let store = window.sessionStorage;

      window.addEventListener("load", initialize);

      function initialize() {
        let table = id("table");
        let food = id("food-name");
        let land = id("land");
        let feed = id("feed");
        let farm = id("farm");
        let process = id("processing");
        let transport = id("transport");
        let packaging = id("packaging");
        let retail = id("retail");
        let total = id("total");
        let dataStr = store.getItem("response");
        if (dataStr != null) {
            let data = JSON.parse(dataStr);
            food.innerText = data["Food product"];
            land.innerText = data["Land use change"];
            feed.innerText = data["Animal Feed"];
            farm.innerText = data["Farm"];
            process.innerText = data["Processing"];
            transport.innerText = data["Transport"];
            packaging.innerText = data["Packging"];
            retail.innerText = data["Retail"];
            total.innerText = data["Total_emissions"];
        }
      }

    /**
     * let obj = json object
     * let jsonString = JSON.stringify(obj)
     * store.setItem("name", jsonString)
     * let jsonObj = JSON.parse(jsonString)
     * /

    /**
        * Removes the given objects children
        * @param {Object} parent - an element object whose children are to be removed
        */
      function removeChildren(parent) {
        while (parent.hasChildNodes()) {
          parent.removeChild(parent.firstChild);
        }
      }


    /**
     * Returns the element that has the ID attribute with the specified value.
     * @param {string} idName - element ID
     * @returns {object} DOM object associated with id.
     */
    function id(idName) {
      return document.getElementById(idName);
    }
}).call(this);