// URL API, na kterou chcete odeslat POST požadavek
const apiURL = 'http://localhost:5123/';

// Funkce pro zobrazení odpovědi na webové stránce
function displayResponse(responseData, elementId) {
    const output = document.getElementById(elementId);
    output.innerHTML = responseData
}

// Funkce pro odeslání dat pomocí POST požadavku
function postData(url, test_name, data, ok_code = 200) {
    const newURL = apiURL + "api/mysql/" + url
    fetch(newURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            displayResponse("Correct", test_name);
            console.log(test_name + ": ", response);
            return response.data
        })
        .catch(error => {
            displayResponse(error.status === ok_code ? "Correct " : "Error", test_name);
            console.log(test_name + ": ", error);
        });
}

function deleteData(url, test_name, id, ok_code = 200) {
    const newURL = apiURL + "api/mysql/" + url
    fetch(newURL + "/" + id, {
        method: 'DELETE',
    })
        .then(response => {
            displayResponse("Correct", test_name);
            console.log(test_name + ": ", response);
            return response.data
        })
        .catch(error => {
            displayResponse(error.status === ok_code ? "Correct " : "Error", test_name);
            console.log(test_name + ": ", error);
        });
}


function getData(url, test_name, ok_code = 200) {
    const newURL = apiURL + "api/mysql/" + url
    fetch(newURL)
        .then(response => {
            displayResponse("Correct", test_name);
            console.log(test_name + ": ", response);
            return response.data
        })
        .catch(error => {
            displayResponse(error.status === ok_code ? "Correct " : "Error", test_name);
            console.log(test_name + ": ", error);
        });
}

async function userTest() {
    let user = {
        email: "test@test.cz",
        username: "test",
        first_name: "test",
        last_name: "test"
    }
    user = await postData("user", "create_user", user)
    await postData("user", "create_user_2", user, ok_code = 400)
    await deleteData("user", "delete_user", user.id)

}

getData("test", "mysql_test")
getData("users", "get_users")
getData("articles", "get_articles")

userTest()

const article = {
    title: "Article title",
    perex: "test",
    content: "test"
}
//test_post("article", "create_article", article)