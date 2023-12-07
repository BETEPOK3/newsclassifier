async function send() {
    let article_text_for_predict = document.getElementById("text_for_predict").value;

    if (!article_text_for_predict.empty()) {
        const response = await fetch("/article/predict", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                article_text: article_text_for_predict,
            }),
        });
        if (response.ok) {
            const json = await response.json();
            let article_text_for_predict = document.getElementById("predicted_categories");
            article_text_for_predict.value = json.categories;
        } else console.log(response);
    }
}