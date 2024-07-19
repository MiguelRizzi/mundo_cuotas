(function () {
  const modal = new bootstrap.Modal(document.getElementById("modal"))
  
  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") {
      modal.show()
    }
  })
  
  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })
  
  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
  })

  
})();

  (function () {
  const toastElement = document.getElementById("toast")
  const toastBody = document.getElementById("toast-body")
  const toast = new bootstrap.Toast(toastElement, { delay: 5000 })

  htmx.on("showMessage", (e) => {
    toastBody.innerText = e.detail.value
    toast.show()
  })
})();

function onlyOneDate(checkbox) {
  var checkboxes = document.getElementsByName('date');
  for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i] !== checkbox) {
          checkboxes[i].checked = false;
      }
  }
}
function onlyOneStatus(checkbox) {
  var checkboxes = document.getElementsByName('status');
  for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i] !== checkbox) {
          checkboxes[i].checked = false;
      }
  }
}

function onlyOneType(checkbox) {
  var checkboxes = document.getElementsByName('type');
  for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i] !== checkbox) {
          checkboxes[i].checked = false;
      }
  }
}

function collapseOthers(button) {
  var allCollapses = document.querySelectorAll('.collapse');
  allCollapses.forEach(function(collapse) {
      if (collapse !== document.querySelector(button.getAttribute('data-bs-target'))) {
          var bsCollapse = new bootstrap.Collapse(collapse, {
              toggle: false
          });
          bsCollapse.hide();
      }
  });
}