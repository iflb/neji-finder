window.AudioContext = window.AudioContext || window.webkitAudioContext;
window.ducts.audio = window.ducts.audio || {};

let capturing = null;
const select = document.getElementById("neji_select");
const video  = document.querySelector("#camera");
const canvas = document.querySelector("#picture");
const div = document.querySelector("#captured");
const user = document.querySelector("#user");
const neji = document.querySelector("#neji");
const sync_id = find_sync_id_in_query()

function find_sync_id_in_query() {
    var queryStr = window.location.search.slice(1);
    if (!queryStr) {
	return null;
    }
    queries = {};
    queries.sync_id = null;
    queryStr.split('&').forEach(function(queryStr) {
	var queryArr = queryStr.split('=');
	queries[queryArr[0]] = queryArr[1];
	if (queryArr[0] == 'sync_id')
	    return queryArr[1];
    });
    return queries.sync_id;
}

let duct = new ducts.Duct();
duct.open("/ducts/wsd").then( (duct) => {
    console.log('opened');
    duct.setEventHandler(
	duct.EVENT.SYNC_MANAGER,
	(rid, eid, data) => {
	    console.log(data);
	    if (data.entry_type == 'ImageEntry') {
		if ('score' in data) {
		    let txt = document.createElement('div');
		    txt.textContent = data['score']
		    div.insertBefore(txt, div.firstChild);
		}
		if ('content' in data) {
		    let blob = new Blob([data.content.buffer], { type: "image/jpeg" });
		    var reader = new FileReader();
		    reader.onloadend = function() {
			let img = document.createElement('img');
			let url = window.URL || window.webkitURL;
			//img.src = url.createObjectURL(blob);
			img.src = reader.result;
			div.insertBefore(img, div.firstChild);
		    }
		    reader.readAsDataURL(blob);
		}
	    } else if (data.entry_type == 'WarningEntry') {
		let txt = document.createElement('div');
		txt.textContent = data['message']
		div.insertBefore(txt, div.firstChild);
	    } else {
		console.log('ignoring entry type:' + data.entry_type);
	    }
	});
    duct.send(
	duct.nextRid(), 
	duct.EVENT.SYNC_MANAGER,
	{'sync_id': sync_id}
    );
    $("#shutter").prop('disabled', false);
}).catch( (error) => {
    console.error(error);
});

$(function(){
    user.value = get_user_id();
    /** カメラ設定 */
    const constraints = {
	audio: false,
	video: {
	    //facingMode: "user"   // フロントカメラを利用する
	    //facingMode: { exact: "environment" }  // リアカメラを利用する場合
	    facingMode: "environment"  // リアカメラを利用する場合
	}
    };
    fetch('./neji.json')
	.then(response => response.json())
	.then(data => {
	    console.log(data);
	    let index = 0;
	    for (const elem of data) {
		let option = document.createElement("option");
		option.text = ( '000' + index ).slice( -3 ) + '_' + elem.value;
		index += 1;
		option.value = elem.value;
		option.setAttribute("url", elem.url);
		select.appendChild(option);
	    }
	    select.addEventListener("change", (event) => {
		option = event.target.selectedOptions[0];
		//alert(option.value);
		//neji.src = "./"+event.target.value;
		neji.src = option.getAttribute('url')
		neji.style.visibility = "visible";
	    });
	    setup();
	});
    navigator.mediaDevices.getUserMedia(constraints)
	.then( (stream) => {
	    video.srcObject = stream;
	    video.onloadedmetadata = (e) => {
		video.play();
		canvas.width = video.clientWidth;
		canvas.height = video.clientHeight;
	    };
	})
	.catch( (err) => {
	    console.log(err.name + ": " + err.message);
	});
    
});

function setup() {
    document.querySelector("#shutter").addEventListener("click", () => {
	if (capturing == null) {
	    capturing = true;
	    setInterval( () => {
		if (capturing) {
		    const ctx = canvas.getContext("2d");
		    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
		    canvas.toBlob(function(blob) {
			blob.arrayBuffer().then( buffer => {
			    //send this buffer to the server
			    //console.log(buffer);
			    let neji_id = select.options[select.selectedIndex].value;
			    let msgs = document.getElementById("messages");
			    let msg = document.createElement("div");
			    duct.send(
				duct.nextRid(), 
				duct.EVENT.SYNC_FILE_ADD,
				{'buf': buffer, 'sync_id': sync_id}
			    );
			});
		    }, "image/jpeg", 0.95);
		    
		    //var imgdata = canvas.toDataURL();
		    //imgdata = imgdata.replace('data:image/png;base64,', '');
		    //var img = document.createElement('img');
		    //img.src = imgdata;
		    //div.insertBefore(img, div.firstChild);
		}
	    }, 500);
	} else {
	    capturing = !capturing
	}
	document.querySelector('#shutter').textContent = capturing ? '撮影中（クリックで停止）' : 'クリックで撮影開始';
    });
    
}

function get_user_id() {
    return getParam('user', null, '')
}

/**
 * Get the URL parameter value
 *
 * @param  name {string} パラメータのキー文字列
 * @return  url {url} 対象のURL文字列（任意）
 */
function getParam(name, url, default_value) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return default_value;
    if (!results[2]) return default_value;
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
