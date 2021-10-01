<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の規格を選ぶ</v-card-title>
        <v-card-text> 
            <v-container>
                <v-row class="pb-1">
                    <v-col class="text-body-1">
                        材質を選ぶ
                    </v-col>
                </v-row>
                <v-row>
                    <v-col 
                        v-for="item in selectableMaterial" 
                        :key="item.src" 
                        cols="4" 
                        md="2" 
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
                        <!--<span class="text-h8 d-flex justify-center">{{item.name}}</span>-->
                    </v-col>
                </v-row>
            </v-container>
            <v-slide-y-transition>
                <v-container v-if="isPicked.material">
                    <v-divider />
                    <v-row class="pt-5">
                        <v-col class="text-body-1">
                            表面処理を選ぶ
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col 
                            v-for="item in selectableSurface" 
                            :key="item.src" 
                            cols="4" 
                            md="2" 
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
                        </v-col>
                    </v-row>
                </v-container>
            </v-slide-y-transition>
            <v-slide-y-transition>
                <v-container v-if="isPicked.surface">
                    <v-divider />
                    <v-row class="pt-5">
                        <v-col class="text-body-1">
                            構成数クラスを選ぶ
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col 
                            v-for="item in selectableAmount" 
                            :key="item.src"
                            cols="4" 
                            md="2" 
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
                        </v-col>
                    </v-row>
                </v-container>
            </v-slide-y-transition>
            <v-slide-y-transition>
                <v-container v-if="isPicked.amount">
                    <v-divider />
                    <v-row class="pt-5">
                        <v-col class="text-body-1">
                            呼び径を選ぶ
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="6">
                            <v-card>
                            <v-img
                                :src="icons.diameter[0].src"
                            />
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-menu
                                close-on-content-click
                                transition="scale-transition"
                                offset-y
                            >
                                <template v-slot:activator="{ on, attrs }">
                                    <v-text-field
                                        v-model="diameter"
                                        label="呼び径"
                                        v-bind="attrs"
                                        v-on="on"
                                        outlined
                                        readonly
                                    />
                                </template>
                                <v-container style="max-height: 200px" class="ma-0 pa-0">
                                    <v-list 
                                        dense
                                    >
                                        <v-list-item-group>
                                            <v-list-item
                                                v-for="item in selectableDiameter"
                                                :key="item.diameter"
                                                @click="makeQuery(item)"
                                            >
                                                <v-list-item-content>
                                                    <v-list-item-title>
                                                        {{item.diameter}}
                                                    </v-list-item-title>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </v-list-item-group>
                                    </v-list>
                                </v-container>
                            </v-menu>
                        </v-col>
                    </v-row>
                </v-container>
            </v-slide-y-transition>
            <v-slide-y-transition>
                <v-container v-if="isPicked.diameter">
                    <v-divider />
                    <v-row class="pt-5">
                        <v-col class="text-body-1">
                            長さ(厚さ)を選ぶ
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="6">
                            <v-card>
                            <v-img
                                :src="icons.thickness[0].src"
                            />
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-menu
                                close-on-content-click
                                transition="scale-transition"
                                offset-y
                            >
                                <template v-slot:activator="{ on, attrs }">
                                    <v-text-field
                                        v-model="thickness"
                                        label="長さ・厚さ"
                                        v-bind="attrs"
                                        v-on="on"
                                        outlined
                                        readonly
                                    />
                                </template>
                                <v-container style="max-height: 200px" class="ma-0 pa-0">
                                    <v-list 
                                        dense
                                    >
                                        <v-list-item-group>
                                            <v-list-item
                                                v-for="item in selectableThickness"
                                                :key="item.thickness"
                                                @click="makeQuery(item)"
                                            >
                                                <v-list-item-content>
                                                    <v-list-item-title>
                                                        {{item.thickness}}
                                                    </v-list-item-title>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </v-list-item-group>
                                    </v-list>
                                </v-container>
                            </v-menu>
                        </v-col>
                    </v-row>
                </v-container>
            </v-slide-y-transition>

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
function changeBackgroundColor(pickedItem, icons){
    for (let item of icons){
        if(pickedItem.name !== item.name){
            item.backgroundColor = "#FFFFFF";
        }
    }
    pickedItem.backgroundColor = "#FFCA28"
}
export default{
    data: () => ({
        icons:{
            material:[
                { 
                    name: "アルミ",
                    src: require("@/assets/icons/44_aluminum.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "ステンレス",
                    src: require("@/assets/icons/45_stainless.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "チタン",
                    src: require("@/assets/icons/46_titanium.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "亜鉛",
                    src: require("@/assets/icons/47_zinc.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "塩化ビニル",
                    src: require("@/assets/icons/48_pvc.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "樹脂",
                    src: require("@/assets/icons/49_resin.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "真鍮",
                    src: require("@/assets/icons/50_brass.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "鉄",
                    src: require("@/assets/icons/51_iron.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "銅",
                    src: require("@/assets/icons/52_copper.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            surface:[
                { 
                    name: "装飾",
                    src: require("@/assets/icons/53_decoration.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "屋内用めっき",
                    src: require("@/assets/icons/54_interiorplating.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "屋外用めっき",
                    src: require("@/assets/icons/55_exteriorplating.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "黒色めっき",
                    src: require("@/assets/icons/56_blackplating.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "塗装",
                    src: require("@/assets/icons/57_painting.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "表面処理なし",
                    src: require("@/assets/icons/58_nocoating.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            amount:[
                { 
                    name: "バラ",
                    src: require("@/assets/icons/61_bara.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "10個未満",
                    src: require("@/assets/icons/62_less10.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "10個以上25個未満",
                    src: require("@/assets/icons/63_10to25.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "25個以上50個未満",
                    src: require("@/assets/icons/64_25to50.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "50個以上100個未満",
                    src: require("@/assets/icons/65_50to100.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "100個以上500個未満",
                    src: require("@/assets/icons/66_100to500.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "500個以上1000個未満",
                    src: require("@/assets/icons/67_500to1000.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
                { 
                    name: "1000個以上",
                    src: require("@/assets/icons/68_more1000.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            diameter:[
                { 
                    name: "呼び径",
                    src: require("@/assets/icons/69_diameter.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
            thickness:[
                { 
                    name: "長さ・厚み",
                    src: require("@/assets/icons/70_thickness.jpg"), 
                    backgroundColor: "#FFFFFF" 
                },
            ],
        },
        isPicked: {
            material:false, 
            surface:false, 
            amount:false,
            diameter:false
        },
        specQuery:{},
        snackbar:false,
        initialSpec:{},
        pickedMaterial:[],
        pickedSurface:[],
        pickedAmount:[],
        pickedDiameter:[],
        pickedThickness:[],
        diameter:"",
        thickness:""
    }),
    props:["duct","genre","shapeQuery"],
    methods: {
        send_query() {
            const _query = Object.assign(this.shapeQuery,this.specQuery);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(item){
            if(this.icons.material.includes(item)){
                for (let key in this.isPicked){
                    this.isPicked[key] = false;
                }
                this.isPicked.material = true;
                this.specQuery = {};
                this.specQuery["材質"] = item.name;
                changeBackgroundColor(item, this.icons.material);
                changeBackgroundColor(item, this.icons.surface);
                changeBackgroundColor(item, this.icons.amount);
                this.send_query();
            }else if(this.icons.surface.includes(item)){
                delete this.specQuery["表面処理"]
                this.isPicked.surface = true;
                this.specQuery["表面処理"] = item.name;
                changeBackgroundColor(item, this.icons.surface);
                this.send_query();
            }else if(this.icons.amount.includes(item)){
                this.isPicked.amount = true;
                this.specQuery["構成数クラス"] = item.name;
                changeBackgroundColor(item, this.icons.amount);
                this.send_query();
            }else if(this.initialSpec["呼び径"].includes(item.diameter)){
                this.isPicked.diameter = true;
                this.specQuery["呼び径"] = item.diameter;
                this.diameter = item.diameter; 
                this.send_query();
            }else if(this.initialSpec["長さか厚み"].includes(item.thickness)){
                this.specQuery["長さか厚み"] = item.thickness;
                this.thickness = item.thickness; 
                console.log(this.specQuery);
                this.send_query();
            }
        },
        accessNextPage(){
            let _query = Object.assign(this.shapeQuery, this.specQuery)
            if(Object.keys(this.specQuery).length == Object.keys(this.initialSpec).length){
                this.$router.push({
                    name: "FinderResult",
                    params:{ 'totalQuery': _query, 'genre':this.genre }
                });
            }else{
                this.snackbar =true;
            }
        }
    }, 
    computed:{
        selectableMaterial(){
            let _arr = [];
            this.icons.material.forEach((item) => {
                if(this.pickedMaterial.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableSurface(){
            let _arr = [];
            this.icons.surface.forEach((item) => {
                if(this.pickedSurface.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableAmount(){
            let _arr = [];
            this.icons.amount.forEach((item) => {
                if(this.pickedAmount.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableDiameter(){
            let _arr = [];
            this.initialSpec["呼び径"].forEach((item) => {
                if(this.pickedDiameter.includes(item)){
                    _arr.push({ "diameter" :item});
                }
            });
            return _arr
        },
        selectableThickness(){
            let _arr = [];
            this.initialSpec["長さか厚み"].forEach((item) => {
                if(this.pickedThickness.includes(item)){
                    _arr.push({ "thickness":item });
                }
            });
            return _arr
        },
    },
    created(){
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    if(Object.keys(this.specQuery).length == 0){
                        this.initialSpec = data.spec
                        console.log(this.initialSpec)
                    }

                    if(!Object.keys(this.specQuery).includes("材質")){
                        this.pickedMaterial = data.spec["材質"];
                    }
                    if(!Object.keys(this.specQuery).includes("表面処理")){
                        this.pickedSurface = data.spec["表面処理"];
                    }
                    if(!Object.keys(this.specQuery).includes("構成数クラス")){
                        this.pickedAmount = data.spec["構成数クラス"];
                    }
                    if(!Object.keys(this.specQuery).includes("呼び径")){
                        this.pickedDiameter = data.spec["呼び径"];
                    }
                    if(!Object.keys(this.specQuery).includes("長さか厚み")){
                        this.pickedThickness = data.spec["長さか厚み"];
                    }
                    console.log(this.specQuery)
                }
            )
            this.send_query();
        });
    },
    mounted(){
        this.$emit('add-step', 3);
    }
}
</script>
