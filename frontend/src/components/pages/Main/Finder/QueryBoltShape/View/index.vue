<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>おねじの形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-container>
                <v-row class="pb-1">
                    <v-col class="text-body-1">
                        頭部の形状を選ぶ
                    </v-col>
                </v-row>
                <v-row>
                    <v-col v-for="item in icons.head" :key="item.src" cols="4" md="2" align="center">
                        <v-card
                            @click="makeQuery(item)"
                            :color="item.backgroundColor"
                            max-width="100"
                        >
                            <v-img 
                                class="imgOpacity"
                                alt="item.name"
                                contain
                                :src="item.src" />
                        </v-card>
                        <span class="text-h8 d-flex justify-center">{{item.name}}</span>
                    </v-col>
                </v-row>
            </v-container>

            <v-slide-y-transition>
                <v-container v-if="isPicked.head">
                    <v-divider />
                    <v-row class="py-5">
                        <v-col class="text-body-1">
                            おねじ先端の形状を選ぶ
                        </v-col>
                    </v-row>
                    <carousel :per-page="3" :mouse-drag="false" pagination-color="#42A5F5">
                        <slide 
                            v-for="item in selectableTip" 
                            :key="item.src" 
                            align="center"
                        >
                            <v-card
                                @click="makeQuery(item)"
                                :color="item.backgroundColor"
                                max-width="100"
                            >
                                <v-img 
                                    class="imgOpacity"
                                    alt="item.name"
                                    contain
                                    :src="item.src" />
                            </v-card>
                            <span class="text-h8 d-flex justify-center">{{item.name}}</span>
                        </slide>
                    </carousel>
                </v-container>
            </v-slide-y-transition>
            <v-slide-y-transition>
                <v-container v-if="isPicked.tip">   
                    <v-divider />
                    <v-row class="py-5">
                        <v-col class="text-body-1">
                            頭部穴の形状を選ぶ
                        </v-col>
                    </v-row>
                    <carousel :per-page="3" :mouse-drag="false" pagination-color="#42A5F5">
                        <slide 
                            v-for="item in selectableHoleShape" 
                            :key="item.src" 
                            align="center"
                        >
                            <v-card
                                @click="makeQuery(item)"
                                :color="item.backgroundColor"
                                max-width="100"
                            >
                                <v-img 
                                    class="imgOpacity"
                                    alt="item.name"
                                    contain
                                    :src="item.src" />
                            </v-card>
                            <span class="text-h8 d-flex justify-center">{{item.name}}</span>
                        </slide>
                    </carousel>
                </v-container>
            </v-slide-y-transition>

            <v-divider />
            <v-row class="py-5"> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/finder/query-genre" 
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る    
                </v-btn>  
            </v-row>
        </v-card-text>   
        <v-snackbar
            v-model="snackbar"
            timeout="2000"
        >選択されていない項目があります
        </v-snackbar>
    </v-card>
</template>
<script>
import { Carousel, Slide } from 'vue-carousel'
function changeBackgroundColor(pickedItem, icons){
    for (let item of icons){
        if(pickedItem.name !== item.name){
            item.backgroundColor = "#FFFFFF";
        }
    }
    pickedItem.backgroundColor = "#FFCA28"
}
export default{
    components:{
        Carousel,
        Slide
    },
    data: () => ({
        icons: {
            head:[
                { 
                    name: "円柱",
                    src: require("@/assets/icons/4_cap.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                {
                    name: "さら",
                    src: require("@/assets/icons/5_sara.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "ツマミ",
                    src: require("@/assets/icons/6_tsumami.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "トラス・ボタン・丸",
                    src: require("@/assets/icons/7_circle.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "なべ",
                    src: require("@/assets/icons/8_nabe.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "フレキ",
                    src: require("@/assets/icons/9_flex.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "ラッパ",
                    src: require("@/assets/icons/10_horn.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "丸さら",
                    src: require("@/assets/icons/11_marusara.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "根角",
                    src: require("@/assets/icons/12_root.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "平",
                    src: require("@/assets/icons/13_plain.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "無",
                    src: require("@/assets/icons/14_none.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "六角", 
                    src: require("@/assets/icons/15_hexagon.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "六角フランジ",
                    src: require("@/assets/icons/16_hexflange.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            tip:[
                { 
                    name: "くぼみ",
                    src: require("@/assets/icons/23_dimple.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "たいら",
                    src: require("@/assets/icons/24_plain.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "とがり",
                    src: require("@/assets/icons/25_sharp.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "ドリル",
                    src: require("@/assets/icons/26_drill.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "棒先",
                    src: require("@/assets/icons/27_stick.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            hole_shape:[
                { 
                    name: "スクエア",
                    src: require("@/assets/icons/17_square.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "すり割り（ー）",
                    src: require("@/assets/icons/18_suriwari.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "トルクス",
                    src: require("@/assets/icons/19_torx.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "プラスマイナス（＋ー）",
                    src: require("@/assets/icons/20_pm.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "十字穴（＋）",
                    src: require("@/assets/icons/21_plus.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name:"六角穴",   
                    src: require("@/assets/icons/22_hexagon.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name:"無",
                    src: "",//画像がないので空白
                    backgroundColor: "#FFFFFF" 
                },
            ],
        },
        isPicked: { head:false, tip:false, hole_shape:false },
        pickedTip:[],
        pickedHoleShape:[],
        query: {},
        shape: {},
        snackbar: false,
    }),
    props:["duct","genre"],
    computed:{
        selectableTip(){
            let _arr = [];
            this.icons.tip.forEach((item) => {
                if(this.pickedTip.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableHoleShape(){
            let _arr = [];
            this.icons.hole_shape.forEach((item) => {
                if(this.pickedHoleShape.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
    },
    methods: {
        send_query() {
            let _query = '';
            if (this.query){
                _query = this.query;
            }
            console.log(_query);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(item){
            if(this.icons.head.includes(item)){
                this.query = {};
                for (let key in this.isPicked){
                    this.isPicked[key] = false;
                }
                this.query["頭部"] = item.name;
                this.isPicked.head = true;
                changeBackgroundColor(item, this.icons.hole_shape);
                changeBackgroundColor(item, this.icons.tip);
                changeBackgroundColor(item, this.icons.head);
                this.send_query();
            }else if(this.icons.tip.includes(item)){
                delete this.query["おねじ先端"]
                this.query["おねじ先端"] = item.name;
                this.isPicked.tip = true;
                changeBackgroundColor(item, this.icons.tip);

                this.send_query();
            }else if(this.icons.hole_shape.includes(item)){
                this.query["頭部穴形状"] = item.name;
                this.isPicked.hole_shape = true;
                changeBackgroundColor(item, this.icons.hole_shape);
                this.send_query();
            }
        },
        accessNextPage(){
            console.log(this.query);
            if(Object.keys(this.query).length == 3){
                this.$router.push({
                    name: "QuerySpec",
                    params: { 'shapeQuery': this.query, 'genre': this.genre }
                });
            }else{
                this.snackbar =true;
            }
        }
    }, 
    created(){
        this.duct.invokeOnOpen(async () => {
            console.log('opened');
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    console.log(data.shape);
                    this.$set(this, 'response', JSON.stringify(data, null, '\t'));
                    this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});
                    this.$set(this, 'shape', 'shape' in data ? data.shape : '');

                    if(!Object.keys(this.query).includes("おねじ先端")){
                        this.pickedTip = this.shape["おねじ先端"];
                    }
                    if(!Object.keys(this.query).includes("頭部穴形状")){
                        this.pickedHoleShape = this.shape["頭部穴形状"];
                    }
                    if(Object.keys(this.query).length == 3) this.accessNextPage();
                    this.$nextTick(() => {
                        this.$vuetify.goTo(document.body.scrollHeight);
                    });
                }
            )
            this.send_query();
        });
        console.log(this.icons);
    },
    mounted(){
        this.$emit('add-step', 2);
    }
}
</script>

