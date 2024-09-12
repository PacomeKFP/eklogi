// utils
const close_alert_icon = document.querySelector("div.alert i.fa");
if (close_alert_icon)
  close_alert_icon.addEventListener("click", (e) =>
    document.querySelector("div.alert").remove()
  );

// Pour la page de candiature
const poste_element = document.querySelector("form select#poste");
const programme_element = document.querySelector("#div-programme");
const programme_textarea_element = document.querySelector(
  "#div-programme textarea"
);

poste_element?.addEventListener("change", (e) => {
  const value = e.target.value;
  console.log(value);

  if (value === "president") {
    programme_element.classList.remove("hidden");
    programme_element.classList.remove("height-0");
    programme_textarea_element.setAttribute("required", "true");
  } else {
    programme_element.classList.add("hidden");
    programme_element.classList.add("height-0");
    programme_textarea_element.removeAttribute("required");
  }
});
