<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-container>
                <carousel :per-page="3" :mouse-drag="false" pagination-color="#42A5F5">
                    <slide 
                        v-for="item in selectedItems" 
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
                <!--<v-row>
                    <v-col v-for="item in selectedItems" :key="item.src" cols="4" md="2" align="center">
                        <v-card
                            @click="makeQuery(item)"
                            :color="item.backgroundColor"
                            max-width="300"
                        >
                            <v-img 
                                class="imgOpacity"
                                alt="item.name"
                                contain
                                :src="item.src" />
                        </v-card>
                        <span class="text-h8 d-flex justify-center">{{item.name}}</span>
                    </v-col>
                </v-row>-->
            </v-container>
            <v-divider />
            <v-row class="pt-7"> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/finder/query-genre" 
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る    
                </v-btn>  
                <v-spacer />
                <v-btn
                    dark
                    color="primary"
                    @click="accessNextPage"
                >
                    次に進む 
                    <v-icon>mdi-arrow-right</v-icon>
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
function changeBackgroundColor(pickedItem, items){
    for (let item of items){
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
        items: {
            nut:[
                { 
                    name: "クリップ", 
                    src: require("@/assets/icons/28_clip.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "フランジ", 
                    src: require("@/assets/icons/29_flange.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "円筒",     
                    src: require("@/assets/icons/30_cylinder.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "鬼目",
                    src: require("@/assets/icons/31_insert.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "袋",
                    src: require("@/assets/icons/32_fukuro.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "長方形",
                    src: require("@/assets/icons/33_rectangle.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "爪付",
                    src: require("@/assets/icons/34_itotsuki.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "輪",
                    src: require("@/assets/icons/35_ring.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "六角",
                    src: require("@/assets/icons/36_hexagon.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "六角・セット",
                    src: require("@/assets/icons/37_hexagonset.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            washer:[
                { 
                    name: "U字",
                    src: require("@/assets/icons/38_u.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "ウェーブ", 
                    src: require("@/assets/icons/39_wave.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "テーパー", 
                    src: require("@/assets/icons/40_taper.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "円",
                    src: require("@/assets/icons/41_circle.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name:"球面",
                    src: require("@/assets/icons/42_ball.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name:"四角",
                    src: require("@/assets/icons/43_rectangle.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ]
        },
        isPicked: false,
        query: {},
        shape: {},
        snackbar: false
    }),
    props:["duct","genre"],
    computed:{
        selectedItems(){
            if (this.genre == "めねじ"){
                return this.items.nut
            }else if(this.genre == "座金"){
                return this.items.washer
            }else{
                return 0
            }
        }
    },
    methods: {
        send_query() {
            let _query = '';
            if (this.query){
                _query = this.query;
            }
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(item){
            if(this.items.nut.includes(item)){
                this.query = {};
                this.query["ナット形状"] = item.name;
                this.isPicked = true;
                changeBackgroundColor(item, this.items.nut);
            }else if(this.items.washer.includes(item)){
                this.query = {};
                this.query["座金形状"] = item.name;
                this.isPicked = true;
                changeBackgroundColor(item, this.items.washer);
            }
            this.send_query();
        },
        accessNextPage(){
            if(Object.keys(this.query).length == 1){
                this.$router.push({
                    name: "QuerySpec",
                    params:{ 'shapeQuery': this.query, 'genre':this.genre }
                });
            }else{
                this.snackbar =true;
            }
        }
    }, 
    created(){
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});
                    this.$set(this, 'shape', 'shape' in data ? data.shape : '');
                }
            )
            this.send_query();
        });
    },
    mounted(){
        this.$emit('add-step', 2);
    }
}
</script>
