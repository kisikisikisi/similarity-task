var list = []
var title_name;
var page_url;
function showImage() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "opt/result.txt", true);
    xmlHttp.send(null);
    xmlHttp.onload = function () {
        var data = xmlHttp.responseText;
        list.push(data);
        console.log(data);
        if (list[list.length - 1] == list[list.length - 2] && list.length > 1) {
            return;
        }
        let ads = document.getElementById("ads-banner");
        if (ads !== null) {
            ads.remove();
        }
        data_split = data.split('');
        id_list = (data_split.slice(0, data_split.length - 1));
        id = id_list.join('');

        json_load(id, data);
    }
}

//サムネイルの要素を追加
function addElement(data) {

    console.log(page_url);

    let body = document.body;
    let div = '<div id="ads-banner" style="position: fixed; float: right; top: 30%; right: 60px; bottom: auto; width: auto; height: auto; max-width: 320px; margin: 0 0 0 110px; z-index: 2; border: 1px solid #aaa; padding: 5px; background-color: white; box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);"></div>';

    const imgURL = "opt/idata/" + data + ".jpeg";
    const img = `<img src="${imgURL}" style="width: 320px; height: 240px; background-color: lightgray;">`;

    body.insertAdjacentHTML("afterbegin", div);
    const banner = document.getElementById("ads-banner");
    const text = '<a href=' + page_url + '><font size="4">' + title_name + '</a>';

    banner.insertAdjacentHTML("afterbegin", text);
    banner.insertAdjacentHTML("afterbegin", img);

    /*
    banner.onclick = () => {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "http://localhost:8000/cgi-bin/server.py", true);
        xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.send('text=' + 'click:' + data);
    }
    */
    /*
    deleteButton = document.getElementById('delete');
    deleteButton.onclick = () => {
        console.log("delete");
        banner.remove();
    };
    */
}

//jsonファイルからタイトルを検索
function json_load(id, imgName) {
    var request = new XMLHttpRequest();
    request.open('GET', "opt/history.json", true);
    request.responseType = 'json';
    request.send();
    request.onload = function () {
        var data = request.response;
        var matchData = data.filter(function (item, index) {
            if (item.id == id) return true;
        });
        console.log(matchData);
        console.log(matchData[0].title);
        title_name = matchData[0].title;
        page_url = matchData[0].url;
        addElement(imgName);

    }
}

setInterval(showImage, 1000);



