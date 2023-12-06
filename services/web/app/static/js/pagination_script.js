let selected_category = localStorage.getItem("selected_category");
let selected_sort_by = localStorage.getItem("selected_sort_by");
let selected_search_text = localStorage.getItem("selected_search_text");
let pagDiv = document.getElementById("pagination");
function setPag(acount, curPage){
    curPage = curPage + 1;
    let selected_limit1=10;
    if(selected_category == null) selected_category = -1;
    if(selected_sort_by == null) selected_sort_by = "title";
    if(selected_search_text == null) selected_search_text = "";
    acount = Number(acount);
    let c = Math.floor(acount/selected_limit1);
    let rem = acount%selected_limit1;
    if(rem>0) c++;
    if(c==0) c++;
    for(let i = 1; i <= c; i++){
        let a = document.createElement("a");
        a.textContent = i;
        if(curPage == i) a.className = "active";
        a.href = "/index" + "?category=" + selected_category + "&sort_by=" + selected_sort_by
            + "&search_text=" + selected_search_text + "&page=" + (i-1);
        if(c>10){
            let absDiv = Math.abs(i-curPage);
            let r = 0;
            let lim = 3;
            if(curPage - lim < 0) r = lim - curPage;
            if(c - curPage < lim ) r = lim - c + curPage - 1;

            if(absDiv < lim + r){
                pagDiv.appendChild(a);
            }
            else if(i == 1) {
                let ellipsis = document.createElement("span");
                ellipsis.textContent ="...";
                pagDiv.appendChild(a);
                if(!(lim + r - absDiv >= 0)) {
                    pagDiv.appendChild(ellipsis);
                }
            }
            else if(i == c) {
                let ellipsis = document.createElement("span");
                ellipsis.textContent ="...";
                if(!(lim + r - absDiv >= 0)) {
                    pagDiv.appendChild(ellipsis);
                }
                pagDiv.appendChild(a);
            }
        }
        else pagDiv.appendChild(a);
    }
}
