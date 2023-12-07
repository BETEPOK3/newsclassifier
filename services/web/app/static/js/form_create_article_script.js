async function send() {
    let title = document.getElementById("article_title").value;
    title = title == "" ? undefined : title;
    let author = document.getElementById("article_author").value;
    author = author == "" ? undefined : author;
    let categories_selected_options = document.getElementById("categories_select").selectedOptions;
    let categories_list = new Array();
    for(let i=0; i<categories_selected_options.length; i++){
        let op = categories_selected_options[i];
        categories_list.push(op.value);
    }
    const keywords = document.getElementById("tags").getElementsByTagName("li");
    const keywords_list = Array.prototype.slice.call(keywords).map((keyword_li_element) => keyword_li_element.innerText.substring(0, keyword_li_element.innerText.length - 1));
    let date = document.getElementById("article_date").value;
    date = date == "" ? null : date;
    let text = document.getElementById("article_text").value;
    text = text == "" ? undefined : text;

    let isValid = true;
    let categoriesIsValid = true;

    if (categories_list.length == 0) categoriesIsValid = false;
    for (category of categories_list) {
        if (category == "") {
            categoriesIsValid = false;
        }
    }

    if (title == undefined) {
        document.querySelector(".title-error").innerHTML = "Поле 'Название' не может быть пустым";
        document.querySelector(".title-error").style.display = "inline";
        document.querySelector(".title-error").style.fontSize = "20px";
        document.querySelector(".title-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".title-error").innerHTML = "";
    }
    if (author == undefined) {
        document.querySelector(".author-error").innerHTML = "Поле 'Автор' не может быть пустым";
        document.querySelector(".author-error").style.display = "inline";
        document.querySelector(".author-error").style.fontSize = "20px";
        document.querySelector(".author-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".author-error").innerHTML = "";
    }
    if (categoriesIsValid == false) {
        document.querySelector(".categories-error").innerHTML = "Выберите хотя бы одну категорию";
        document.querySelector(".categories-error").style.display = "inline";
        document.querySelector(".categories-error").style.fontSize = "20px";
        document.querySelector(".categories-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".categories-error").innerHTML = "";
    }
    if (text == undefined) {
        document.querySelector(".text-error").innerHTML = "Поле 'Текст' не может быть пустым";
        document.querySelector(".text-error").style.display = "inline";
        document.querySelector(".text-error").style.fontSize = "20px";
        document.querySelector(".text-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".text-error").innerHTML = "";
    }

    const title_input = document.querySelector("div input[name='article_title']");
    title_input.addEventListener('change', function() {
        document.querySelector(".title-error").innerHTML = "";
    });
    const author_input = document.querySelector("div input[name='article_author']");
    author_input.addEventListener('change', function() {
        document.querySelector(".author-error").innerHTML = "";
    });
    const categories_select = document.getElementById("categories_select");
    categories_select.addEventListener('change', function() {
        document.querySelector(".categories-error").innerHTML = "";
    });
    const text_input = document.querySelector("div input[name='article_text']");
    text_input.addEventListener('change', function() {
        document.querySelector(".text-error").innerHTML = "";
    });

    if (isValid) {
        const response = await fetch("/article/create", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                article_title: title,
                article_author: author,
                article_categories: categories_list,
                article_keywords: keywords_list,
                article_date: date,
                article_text: text,
            }),
        });
        if (response.ok) {
            const json = await response.json();
            window.location.replace("/article?article_id=" + json.id);
        } else console.log(response);
    }
}