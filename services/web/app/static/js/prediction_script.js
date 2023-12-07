async function send() {
    let article_text_for_predict = document.getElementById("text_for_predict")

    if (article_text_for_predict.value.length > 0) {
        const response = await fetch("/article/predict", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                article_text: article_text_for_predict.value,
            }),
        });
        if (response.ok) {
            const json = await response.json();
            console.log(json.categories123)
            let article_text_for_predict = document.getElementById("predicted_categories");
            article_text_for_predict.textContent = json.categories123;
        } else console.log(response);
    }
}