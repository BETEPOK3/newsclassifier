async function send() {
    let title = document.getElementById("article_title").value;
    title = title == "" ? undefined : title;
    let author = document.getElementById("article_author").value;
    author = author == "" ? undefined : author;
    const categories = document.getElementById("article_categories").value;
    const categories_list = categories.split(";").map((category) => category.trim());
    const keywords = document.getElementById("article_keywords").value;
    const keywords_list = keywords.split(";").map((keyword) => keyword.trim());
    let date = document.getElementById("article_date").value;
    date = date == "" ? undefined : date;
    let text = document.getElementById("article_text").value;
    text = text == "" ? undefined : text;

    let isValid = true;
    let categoriesIsValid = true;
    let keywordsIsValid = true;

    for (category of categories_list) {
        if (category == "") {
            categoriesIsValid = false;
        }
    }

    if (keywords_list.length > 1) {
        for (keyword of keywords_list) {
            if (keyword == "") {
                keywordsIsValid = false;
            }
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
        document.querySelector(".categories-error").innerHTML = "Поле 'Категории' должно быть заполнено, категории должны быть указаны через точку с запятой";
        document.querySelector(".categories-error").style.display = "inline";
        document.querySelector(".categories-error").style.fontSize = "20px";
        document.querySelector(".categories-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".categories-error").innerHTML = "";
    }
    if (keywordsIsValid == false) {
        document.querySelector(".keywords-error").innerHTML = "Ключевые слова должны быть указаны через точку с запятой";
        document.querySelector(".keywords-error").style.display = "inline";
        document.querySelector(".keywords-error").style.fontSize = "20px";
        document.querySelector(".keywords-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".keywords-error").innerHTML = "";
    }
    if (date == undefined) {
        document.querySelector(".date-error").innerHTML = "Поле 'Дата' должно быть заполнено";
        document.querySelector(".date-error").style.display = "inline";
        document.querySelector(".date-error").style.fontSize = "20px";
        document.querySelector(".date-error").style.color = "red";
        isValid = false;
    } else {
        document.querySelector(".date-error").innerHTML = "";
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
    const categories_input = document.querySelector("div input[name='article_categories']");
    categories_input.addEventListener('change', function() {
        document.querySelector(".categories-error").innerHTML = "";
    });
    const keywords_input = document.querySelector("div input[name='article_keywords']");
    keywords_input.addEventListener('change', function() {
        document.querySelector(".keywords-error").innerHTML = "";
    });
    const date_input = document.querySelector("div input[name='article_date']");
    date_input.addEventListener('change', function() {
        document.querySelector(".date-error").innerHTML = "";
    });
    const text_input = document.querySelector("div input[name='article_text']");
    text_input.addEventListener('change', function() {
        document.querySelector(".text-error").innerHTML = "";
    });

    if (isValid) {
        const response = await fetch("/article/create", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
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