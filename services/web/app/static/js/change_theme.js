function applyTheme(theme) {
	if(theme == ""){
		document.body.classList.remove("dark-theme");
	}
	else {
		document.body.classList.add("dark-theme");
	}
}


document.addEventListener("DOMContentLoaded", () => {
	const savedTheme = localStorage.getItem("theme") || "";
	applyTheme(savedTheme);
	document.querySelector('.btn-toggle').addEventListener('click', function() {
		if(localStorage.getItem("theme") == "")
		{
			localStorage.setItem("theme", "dark-theme");
		}
		else {
			localStorage.setItem("theme", "");
		}
		applyTheme(localStorage.getItem("theme"));
	});
});
