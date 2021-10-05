<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の規格を選ぶ</v-card-title>
        <v-card-text> 
            <v-row v-if="itemQuantity != 0" class="pt-5">
                <v-col>
                    <span class="text-body-1">該当商品数：{{itemQuantity}}個</span>
                </v-col>
            </v-row>
            <v-row v-else class="pt-5">
                <v-col>
                    <span class="text-body-1">該当件数が多すぎます。絞り込んでください</span>
                </v-col>
            </v-row>
            <v-row class="pt-5 pb-8"> 
                <v-btn
                    dark
                    color="primary"
                    @click="backToPreviousPage"
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る    
                </v-btn>  
                <v-spacer />
                <v-btn
                    :dark="!buttonDisabled"
                    :disabled="buttonDisabled"
                    color="primary"
                    @click="accessNextPage"
                >
                    次に進む 
                    <v-icon>mdi-arrow-right</v-icon>
                </v-btn>  
            </v-row>

            <v-btn
                @click="resetQuery"
            >
                規格をリセットする
            </v-btn>

            <carousel-button
                :headerIsOn="true"
                headerTitle="中分類"
                :inputItems="selectableMiddleClassification"
                @update-query="makeQuery"
                :labelIsOn="true"
                class="mb-6"
            />
            <v-divider />
            <card-button 
                :headerIsOn="true"
                headerTitle="材質"
                :inputItems="selectableMaterial"
                @update-query="makeQuery"
                :labelIsOn="false"
                class="mb-6"
            />
            <v-divider />
            <v-slide-y-transition>
                <card-button 
                    :headerIsOn="true"
                    headerTitle="表面処理"
                    :inputItems="selectableSurface"
                    @update-query="makeQuery"
                    :labelIsOn="false"
                    class="mb-6"
                />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                <card-button 
                    :headerIsOn="true"
                    headerTitle="構成数クラス"
                    :inputItems="selectableAmount"
                    @update-query="makeQuery"
                    :labelIsOn="false"
                    class="mb-6"
                />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                    <drop-down-menu
                        headerTitle="呼び径"
                        :imageSource="nominal.image"
                        :model="nominal.model"
                        :inputItems="selectableNominal"
                        @update-query="makeQuery"
                        class="mb-6"
                    />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                    <drop-down-menu
                        v-if="outer.isNecessary"
                        headerTitle="外径・幅"
                        :imageSource="outer.image"
                        :model="outer.model"
                        :inputItems="selectableOuter"
                        @update-query="makeQuery"
                        class="mb-6"
                    />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                    <drop-down-menu
                        v-if="thickness.isNecessary"
                        headerTitle="長さ・厚さ"
                        :imageSource="thickness.image"
                        :model="thickness.model"
                        :inputItems="selectableThickness"
                        @update-query="makeQuery"
                        class="mb-6"
                    />
            </v-slide-y-transition>
            <v-divider />
            <v-row v-if="itemQuantity != 0" class="pt-5">
                <v-col>
                    <span class="text-body-1">該当商品数：{{itemQuantity}}個</span>
                </v-col>
            </v-row>
            <v-row v-else class="pt-5">
                <v-col>
                    <span class="text-body-1">該当件数が多すぎます。絞り込んでください</span>
                </v-col>
            </v-row>
            <v-row class="pt-5"> 
                <v-btn
                    dark
                    color="primary"
                    @click="backToPreviousPage"
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る    
                </v-btn>  
                <v-spacer />
                <v-btn
                    :dark="!buttonDisabled"
                    :disabled="buttonDisabled"
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
import { icons } from '../../spec_profile.js'


import CardButton from '../../CardButton'
import CarouselButton from '../../CarouselButton'
import DropDownMenu from '../../DropDownMenu'
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
        CardButton,
        DropDownMenu,
        CarouselButton
    },
    data: () => ({
        icons,
        currentSpecQuery:{},
        
        snackbar:false,
        initialSpec:{
            "呼び径": [],
            "表面処理": [],
            "構成数クラス": [],
            "中分類": [],
            "材質": [],
            "外径か幅": [],
            "長さか厚み": [ ],
        },
        nominal:{
            model:"",
            image:"",
        },
        outer:{
            isNecessary:true,
            model:"",
            image:"",
        },
        thickness:{
            isNecessary:true,
            model:"",
            image:"",
        },
        pickedMiddleClassification:[],
        pickedMaterial:[],
        pickedSurface:[],
        pickedAmount:[],
        pickedNominal:[],
        pickedOuter:[],
        pickedThickness:[],
        itemQuantity:0,
        buttonDisabled:true,
        currentItems:[],
        data:{}
    }),
    props:["duct","genre","shapeQuery","specQuery"],
    methods: {
        send_query() {
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.currentSpecQuery);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(item){
            if(this.icons.middle_classification.includes(item)){
                this.currentSpecQuery["中分類"] = item.name;
                changeBackgroundColor(item, this.icons.middle_classification);
            }else if(this.icons.material.includes(item)){
                this.currentSpecQuery["材質"] = item.name;
                changeBackgroundColor(item, this.icons.material);
            }else if(this.icons.surface.includes(item)){
                this.currentSpecQuery["表面処理"] = item.name;
                changeBackgroundColor(item, this.icons.surface);
            }else if(this.icons.amount.includes(item)){
                this.currentSpecQuery["構成数クラス"] = item.name;
                changeBackgroundColor(item, this.icons.amount);
            }else if(this.initialSpec["呼び径"].includes(item.val) && item.name=="呼び径" ){
                this.currentSpecQuery["呼び径"] = item.val;
                this.nominal.model = item.val; 
            }else if(this.outer.isNecessary && this.initialSpec["外径か幅"].includes(item.val) && item.name=="外径か幅" ){
                this.currentSpecQuery["外径か幅"] = item.val;
                this.outer.model = this.currentSpecQuery["外径か幅"];
            }else if(this.thickness.isNecessary && this.initialSpec["長さか厚み"].includes(item.val) && item.name=="長さか厚み"){
                this.currentSpecQuery["長さか厚み"] = item.val;
                this.thickness.model = this.currentSpecQuery["長さか厚み"]; 
            }
            this.send_query();
        },
        resetQuery(){
            this.currentSpecQuery = {};
            this.send_query();
            changeBackgroundColor({ name: "" }, this.icons.middle_classification);
            changeBackgroundColor({ name: "" }, this.icons.material);
            changeBackgroundColor({ name: "" }, this.icons.surface);
            changeBackgroundColor({ name: "" }, this.icons.amount);
            this.nominal.model="";
            this.outer.model="";
            this.thickness.model="";
        },
        accessNextPage(){
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.currentSpecQuery)
            this.$emit( 'emit-spec-query', this.currentSpecQuery );
            this.$emit( 'emit-item-list', this.currentItems );
            if(this.itemQuantity == 1){
                this.$emit( 'emit-item', this.currentItems );
                this.$emit( 'emit-component-name', 'result' );
            }else{
                this.$emit( 'emit-component-name', 'result-list' );
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },
        backToPreviousPage(){
            this.resetQuery();
            this.$emit( 'emit-shape-query', {} );
            if(['めねじ','座金'].includes(this.genre)){
                this.$emit( 'emit-component-name', 'query-nut-washer-shape' );
            }else{
                this.$emit( 'emit-component-name', 'query-bolt-shape' );
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        }
    }, 
    watch:{
        itemQuantity(){
            if (this.itemQuantity != 0){
                this.buttonDisabled = false;
            }else{
                this.buttonDisabled = true;
            }
        },
        selectableNominal(){
            console.log(this.selectableNominal);
        }
    },
    computed:{
        selectableMiddleClassification(){
            let _arr = [];
            this.icons.middle_classification.forEach((item) => {
                if(this.pickedMiddleClassification.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
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
        selectableNominal(){
            let _arr = [];
            this.initialSpec["呼び径"].forEach((item) => {
                if(this.pickedNominal.includes(item)){
                    _arr.push({ "name":"呼び径", "val": item });
                }
            });
            return _arr
        },
        selectableOuter(){
            let _arr = [];
            this.initialSpec["外径か幅"].forEach((item) => {
                console.log(item);
                if(this.pickedOuter.includes(item)){
                    _arr.push({ "name":"外径か幅", "val": item });
                }
            });
            return _arr
        },
        selectableThickness(){
            let _arr = [];
            this.initialSpec["長さか厚み"].forEach((item) => {
                if(this.pickedThickness.includes(item)){
                    _arr.push({ "name":"長さか厚み", "val": item });
                }
            });
            return _arr
        },
    },
    created(){
        this.$vuetify.goTo(0);
        if(["おねじ","めねじ"].includes(this.genre)){
            this.outer.isNecessary = false;
            if(this.genre == "めねじ"){
                this.thickness.isNecessary = false;
                this.nominal.image = this.icons.nominal[1].src;
            }else{
                this.thickness.image = this.icons.thickness[0].src;
                this.nominal.image = this.icons.nominal[0].src;
            }
        }else{
            this.thickness.image = this.icons.thickness[1].src;
            this.nominal.image = this.icons.nominal[2].src;
            this.outer.image = this.icons.outer[0].src;
        }
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {

                    if([1,3].includes(Object.keys(data.query).length)){
                        this.initialSpec = data.spec
                    }
                    if(!Object.keys(this.currentSpecQuery).includes("中分類")){
                        this.pickedMiddleClassification = data.spec["中分類"];
                    }

                    if(!Object.keys(this.currentSpecQuery).includes("材質")){
                        this.pickedMaterial = data.spec["材質"];
                    }
                    if(!Object.keys(this.currentSpecQuery).includes("表面処理")){
                        this.pickedSurface = data.spec["表面処理"];
                    }
                    if(!Object.keys(this.currentSpecQuery).includes("構成数クラス")){
                        this.pickedAmount = data.spec["構成数クラス"];
                    }
                    if(!Object.keys(this.currentSpecQuery).includes("呼び径")){
                        this.pickedNominal = data.spec["呼び径"];
                    }

                    if(["おねじ","座金"].includes(this.genre)){
                        if(!Object.keys(this.currentSpecQuery).includes("長さか厚み")){
                            this.pickedThickness = data.spec["長さか厚み"];
                        }
                    }
                    if(["座金"].includes(this.genre)){
                        if(!Object.keys(this.currentSpecQuery).includes("外径か幅")){
                            this.pickedOuter = data.spec["外径か幅"];
                        }
                    }
                    if(Object.keys(data).includes('items')){
                        this.currentItems = data.items;
                        this.itemQuantity = data.items.length;
                    }
                }
            )
            this.resetQuery();
        });
    },
    mounted(){
        this.$emit('add-step', 3);
    },
}
</script>
