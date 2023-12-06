let category_select = document.getElementById("category_select");
let sort_by_select = document.getElementById("sort_by_select");
let search_text = document.getElementById("search_text");

let selected_category_1 = localStorage.getItem("selected_category");
let selected_search_text_1 = localStorage.getItem("selected_search_text");
let selected_sort_by_1 = localStorage.getItem("selected_sort_by");

category_select.addEventListener("change", function(element){
    localStorage.setItem("selected_category", category_select.selectedOptions[0].value);
})
sort_by_select.addEventListener("change", function(element){
    localStorage.setItem("selected_sort_by", sort_by_select.selectedOptions[0].value);
})
search_text.addEventListener("change", function(element){
    localStorage.setItem("selected_search_text", search_text.value);
})
search_text.value = selected_search_text_1;
if (selected_category_1!=null){
    for(let i=0; i<category_select.options.length; i++){
        let op = category_select.options[i];
        op.selected = false;
        if(op.value == selected_category_1){
            op.selected = true;
        }
    }
}

if (selected_sort_by_1!=null){
    for(let i=0; i<sort_by_select.options.length; i++){
        let op = sort_by_select.options[i];
        op.selected = false;
        if(op.value == selected_sort_by_1){
            op.selected = true;
        }
    }
}
