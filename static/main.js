let duct = new ducts.Duct();
duct.open("/ducts/wsd").then( (duct) => {
    console.log('opened');
    duct.setEventHandler(
	duct.EVENT.SYNC_MANAGER,
	(rid, eid, data) => {
	    console.log(data);
	    if (data.entry_type == 'StateEntry') {
		vm.$set(vm, 'response', JSON.stringify(data, null, '\t'));
		if ('genres' in data) {
		    vm.update_genres(data.genres);
		}
		vm.$set(vm, 'genre', 'genre' in data ? data.genre : '');
		vm.$set(vm, 'query', 'query' in data && Object.keys(data.query).length > 0 ? JSON.stringify(data.query) : '');
		//vm.$set(vm, 'query', 'query' in data ? data.query : '');
		vm.$set(vm, 'item', 'item' in data ? JSON.stringify(data.item) : '');
		vm.$set(vm, 'spec', 'spec' in data ? JSON.stringify(data.spec) : '');
		vm.$set(vm, 'shape', 'shape' in data ? JSON.stringify(data.shape) : '');
	    } else if (data.entry_type == 'SyncStart') {
		//alert(JSON.stringify(data));
		vm.$set(vm, 'sync_id', 'sync_id' in data ? data.sync_id : '');
		vm.send_query();
	    } else if (data.entry_type == 'ImageEntry') {
		console.log('Image Received');
	    } else if (data.entry_type == 'WarningEntry') {
		console.log('Warning:' + data.message);
	    } else {
		alert('unknown entry type. ' + data.entry_type);
	    }
	});
    //vm.send_query();
    sync_id = find_sync_id_in_query();
    if (sync_id == null) {
	duct.send(
	    duct.nextRid(), 
	    duct.EVENT.SYNC_MANAGER,
	    {}
	);
    } else {
	vm.$set(vm, 'sync_id', sync_id);
	duct.send(
	    duct.nextRid(), 
	    duct.EVENT.SYNC_MANAGER,
	    {'sync_id': sync_id}
	);
    }
}).catch( (error) => {
    console.error(error);
});

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


var vm = new Vue({
    el: '#app',
    data: {
	title: 'ネジ特定アプリ',
	footer: 'Copyright ＆copy; 2021 Waseda Univ. / iflab.inc All Rights Reserved.',
	query_placeholder: 'パラメータをJSON形式で記述してください。リターンキーで送信されます。',
	genres: [],
	genre: '',
	query: '',
	shape: '',
	spec: '',
	item: '',
	response: '',
	sync_id: '',
    },
    watch: {
	genre: function(val) {
	    this.$set(vm, 'query', '');
	    this.send_query();
	},
    },
    methods: {
	update_genres: function(genres) {
	    if (this.genres.length == 0) {
		//this.genres.splice(1, this.genres.length);
		this.genres.push(...genres)
	    }
	},
	send_query: function () {
	    let query = {};
	    if (this.query != '')
		query = JSON.parse(this.query);
	    duct.send(
		duct.nextRid(), 
		duct.EVENT.SYNC_STATE_UPDATE,
		{'sync_id': this.sync_id, 'genre': this.genre, 'query': query}
	    );
	},
    },
    mounted: function() {
    },
})

Vue.config.errorHandler = (err, vm, info) => {
    console.log(`Captured in Vue.config.errorHandler: ${info}`, err);
};

function shape_icon_url(genre, key = '', value = '') {
    let index = SHAPE_ICON[genre][key][value];
    return `icon/${index}.jpg`
}

function spec_icon_url(key, value) {
    let index = SPEC_ICON[key][value];
    return `icon/${index}.jpg`
}


let SPEC_ICON = {
    '材質': {
	'アルミ':44,
	'ステンレス':45,
	'チタン':46,
	'亜鉛':47,
	'塩化ビニル（PVC）':48,
	'樹脂':49,
	'真鍮':50,
	'鉄':51,
	'銅':52,
    },
    '表面処理': {
	'装飾':53,
	'屋内用めっき':54,
	'屋外用めっき':55,
	'めっき（黒色）':56,
	'塗装':57,
	'生地':58,
    },
    '形状_表示用': {
	'半ねじ':59,
	'全ねじ':60,
    },
};
let SHAPE_ICON = {
    'ジャンル': {
	'おねじ': 1,
	'めねじ': 2,
	'座金': 3,
    },
    'おねじ': {
	'': {
	    '': 1,
	},
	'頭部': {
	    'キャップ':4,
	    'さら': 5, 
	    'ツマミ': 6,
	    'トラス・ボタン・丸': 7,
	    'なべ': 8,
	    'フレキ': 9, 
	    'ラッパ': 10, 
	    '丸さら': 11, 
	    '根角': 12, 
	    '平': 13, 
	    '無': 14, 
	    '六角': 15, 
	    '六角フランジ': 16, 
	},
	'頭部穴形状': {
	    'スクエア':17,
	    'すり割り（－）':18,
	    'トルクス':19,
	    'プラスマイナス（＋－）':20,
	    '十字穴（＋）':21,
	    '六角穴':22,
	},
	'おねじ先端': {
	    'くぼみ':23,
	    'たいら':24,
	    'とがり':25,
	    'ドリル':26,
	    '棒先':27,
	},
    },
    'おねじ': {
	'': {
	    '': 2,
	},
	'ナット形状': {
	    'クリップ':28,
	    'フランジ':29,
	    '円筒':30,
	    '鬼目':31,
	    '袋':32,
	    '長方形':33,
	    '爪付':34,
	    '輪':35,
	    '六角':36,
	    '六角・セット':37,
	},
    },
    '座金': {
	'': {
	    '': 3,
	},
	'座金形状': {
	    'U字':38,
	    'ウェーブ':39,
	    'テーパー':40,
	    '円':41,
	    '球面':42,
	    '四角':43,
	},
    },
};


